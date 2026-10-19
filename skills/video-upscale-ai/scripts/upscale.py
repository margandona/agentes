"""Adaptación Windows/Python del pipeline MIT de pangpang778/real-esrgan-skill.

Extracción → Real-ESRGAN ncnn/Vulkan → mezcla/redimensión → H.264/AAC.
No requiere Bash, PyTorch ni restauradores faciales.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import ctypes
import ctypes.util
from fractions import Fraction
import hashlib
import json
import logging
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


class UpscaleError(Exception):
    pass


def project_root():
    for p in Path(__file__).resolve().parents:
        if (p/'AGENTS.md').is_file():
            return p
    return Path.cwd()


def find_tool(name, explicit=None):
    value=explicit or os.environ.get({'ffmpeg':'FFMPEG_BIN','ffprobe':'FFPROBE_BIN',
                                     'realesrgan-ncnn-vulkan':'REALESRGAN_BIN'}[name])
    if value:
        p=Path(value).expanduser().resolve()
        if not p.is_file():
            raise UpscaleError(f'No existe {name}: {p}')
        return str(p)
    found=shutil.which(name)
    if found:
        return found
    root=project_root()
    pattern='tmp/upscale-ai/engine/**/realesrgan-ncnn-vulkan*' if name.startswith('real') else f'tmp/media-tools/ffmpeg/**/{name}.exe'
    found=sorted(p for p in root.glob(pattern) if p.is_file() and p.suffix in {'.exe',''})
    if found:
        return str(found[0])
    raise UpscaleError(f'Falta {name}. Usá PATH, variable de entorno o su opción CLI; ver references/usage.md.')


def execute(cmd, log=None, timeout=600):
    logging.info('Ejecutando %r',cmd)
    try:
        p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True,
                         encoding='utf-8',errors='replace',timeout=timeout,
                         stdin=subprocess.DEVNULL,shell=False)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise UpscaleError(f'No se pudo ejecutar {cmd[0]}: {exc}') from exc
    if log:
        with Path(log).open('a',encoding='utf-8') as handle:
            handle.write(json.dumps({'command':list(map(str,cmd)),'returncode':p.returncode},ensure_ascii=False)+'\n')
            handle.write(p.stdout+'\n'+p.stderr+'\n')
    if p.returncode:
        raise UpscaleError(f'{Path(cmd[0]).name} falló ({p.returncode}): {p.stderr[-2500:]}')
    return p.stdout


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as handle:
        for b in iter(lambda:handle.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()


def write_json(path,data):
    Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')


def vulkan_devices():
    """Enumeración real mediante el loader; una DLL presente sola no prueba GPU."""
    libname='vulkan-1.dll' if os.name=='nt' else ctypes.util.find_library('vulkan')
    if not libname:
        return {'available':False,'devices':[],'error':'No se encontró el loader Vulkan'}
    try:
        lib=ctypes.CDLL(libname)
        U=ctypes.c_uint32
        P=ctypes.c_void_p
        class CreateInfo(ctypes.Structure):
            _fields_=[('sType',U),('pNext',P),('flags',U),('pApplicationInfo',P),
                      ('enabledLayerCount',U),('ppEnabledLayerNames',P),
                      ('enabledExtensionCount',U),('ppEnabledExtensionNames',P)]
        lib.vkCreateInstance.argtypes=[ctypes.POINTER(CreateInfo),P,ctypes.POINTER(P)]
        lib.vkCreateInstance.restype=ctypes.c_int32
        lib.vkEnumeratePhysicalDevices.argtypes=[P,ctypes.POINTER(U),ctypes.POINTER(P)]
        lib.vkEnumeratePhysicalDevices.restype=ctypes.c_int32
        lib.vkGetPhysicalDeviceProperties.argtypes=[P,P]
        lib.vkDestroyInstance.argtypes=[P,P]
        instance=P()
        if lib.vkCreateInstance(ctypes.byref(CreateInfo(sType=1)),None,ctypes.byref(instance))!=0:
            raise UpscaleError('Vulkan no pudo crear una instancia')
        try:
            count=U()
            if lib.vkEnumeratePhysicalDevices(instance,ctypes.byref(count),None)!=0 or not 0<count.value<=64:
                raise UpscaleError('No se encontraron dispositivos Vulkan utilizables')
            handles=(P*count.value)()
            if lib.vkEnumeratePhysicalDevices(instance,ctypes.byref(count),handles)!=0:
                raise UpscaleError('Falló la enumeración de GPU Vulkan')
            devices=[]
            for index,handle in enumerate(handles):
                # VkPhysicalDeviceProperties completo cabe en este buffer; no pasar
                # una estructura parcial porque el driver escribe también limits.
                buf=ctypes.create_string_buffer(4096)
                lib.vkGetPhysicalDeviceProperties(handle,buf)
                devices.append({'index':index,'name':buf.raw[20:276].split(b'\0')[0].decode('utf-8','replace'),
                                'device_type':int.from_bytes(buf.raw[16:20],'little')})
            return {'available':bool(devices),'devices':devices}
        finally:
            lib.vkDestroyInstance(instance,None)
    except (OSError,AttributeError,UpscaleError) as exc:
        return {'available':False,'devices':[],'error':str(exc)}


def choose_gpu(devices,requested=None):
    if not devices:
        raise UpscaleError('El modo quality requiere una GPU Vulkan; fast funciona sin ella')
    if requested is not None:
        if requested not in [d['index'] for d in devices]:
            raise UpscaleError(f'Índice de GPU Vulkan inválido: {requested}')
        return requested
    return next((d['index'] for d in devices if 'NVIDIA' in d['name'].upper()),
                next((d['index'] for d in devices if d['device_type']==2),devices[0]['index']))


def probe(path,ffprobe,frames=True):
    path=Path(path).resolve(strict=True)
    if not path.is_file():
        raise UpscaleError(f'No es un archivo: {path}')
    raw=json.loads(execute([ffprobe,'-v','error','-show_streams','-show_format','-of','json',path]))
    videos=[s for s in raw.get('streams',[]) if s['codec_type']=='video' and not s.get('disposition',{}).get('attached_pic')]
    if len(videos)!=1:
        raise UpscaleError('Se admite exactamente una pista de video principal; no se eligen pistas silenciosamente')
    v=videos[0]
    fps=Fraction(v.get('avg_frame_rate','0/1'))
    if fps<=0:
        raise UpscaleError('FPS inválido; no se adivina la cadencia')
    rotation=next((float(s['rotation']) for s in v.get('side_data_list',[]) if 'rotation' in s),0)
    width,height=int(v['width']),int(v['height'])
    if round(rotation)%180:
        width,height=height,width
    pts=[]
    if frames:
        timing=json.loads(execute([ffprobe,'-v','error','-select_streams',str(v['index']),'-show_frames',
                                  '-show_entries','frame=best_effort_timestamp_time','-of','json',path]))
        pts=[float(f['best_effort_timestamp_time']) for f in timing['frames'] if 'best_effort_timestamp_time' in f]
    cfr=all(abs((b-a)-float(1/fps))<0.0005 for a,b in zip(pts,pts[1:]))
    return {'path':str(path),'width':width,'height':height,'orientation':'vertical' if height>width else 'horizontal',
            'fps':str(fps),'cfr':cfr,'rotation':rotation,'frames':len(pts) if frames else int(v.get('nb_frames',0)),
            'start':float(v.get('start_time',raw['format'].get('start_time',0))),
            'duration':float(raw['format'].get('duration',v.get('duration',0))),
            'video':v,'audio':[s for s in raw['streams'] if s['codec_type']=='audio'],'raw':raw}


def bitrate(fps):
    return '12M' if Fraction(fps)>=48 else '8M'


def geometry_filter(width=1080,height=1920,color=None,rng=None):
    matrix=f':out_color_matrix={color}' if color in {'bt709','bt470bg','smpte170m','bt2020nc'} else ''
    if rng in {'tv','pc'}:
        matrix+=f':out_range={rng}'
    return f'scale={width}:{height}:flags=lanczos:force_original_aspect_ratio=decrease:force_divisible_by=2{matrix},setsar=1,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2'


def sharp_filter(amount):
    return f',unsharp=5:5:{amount}:5:5:0' if amount else ''


@contextmanager
def scratch(root,keep=False):
    root=Path(root).resolve()
    root.mkdir(parents=True,exist_ok=True)
    work=Path(tempfile.mkdtemp(prefix='upscale-',dir=root)).resolve()
    if work.parent!=root:
        raise UpscaleError('Directorio temporal fuera de la raíz esperada')
    try:
        yield work
    finally:
        if not keep:
            # Verificar el destino absoluto antes de cualquier borrado recursivo.
            if work.parent!=root or not work.name.startswith('upscale-'):
                raise UpscaleError('Se rechazó la limpieza de una ruta inesperada')
            shutil.rmtree(work)


def backup_source(source,parent,digest):
    parent=Path(parent).resolve()
    parent.mkdir(parents=True,exist_ok=True)
    target=parent/(digest[:16]+'-'+source.name)
    if target.exists():
        if sha256(target)!=digest:
            raise UpscaleError(f'El respaldo existente no coincide: {target}')
    else:
        with source.open('rb') as src,target.open('xb') as dest:
            shutil.copyfileobj(src,dest)
        if sha256(target)!=digest:
            raise UpscaleError('El hash del respaldo no coincide')
    return str(target)


def audio_options(info):
    opts=[]
    for index,stream in enumerate(info['audio']):
        copy=stream['codec_name']=='aac' and stream.get('profile')=='LC'
        opts.extend([f'-c:a:{index}','copy' if copy else 'aac'])
        if not copy:
            opts.extend([f'-b:a:{index}','192k',f'-profile:a:{index}','aac_low'])
    return opts


def color_options(info):
    opts=[]
    for key,flag in [('color_range','-color_range'),('color_space','-colorspace'),
                     ('color_transfer','-color_trc'),('color_primaries','-color_primaries')]:
        value=info['video'].get(key)
        if value and value not in {'unknown','unspecified','reserved'}:
            opts.extend([flag,value])
    return opts


def color_filter(info):
    values=[]
    for key,flag in [('color_space','colorspace'),('color_transfer','color_trc'),('color_primaries','color_primaries')]:
        value=info['video'].get(key)
        if value and value not in {'unknown','unspecified','reserved'}:
            values.append(f'{flag}={value}')
    rng={'tv':'limited','pc':'full'}.get(info['video'].get('color_range'))
    if rng:
        values.append(f'range={rng}')
    return ',setparams='+':'.join(values) if values else ''


def validate(info,output,ffmpeg,ffprobe,expected_frames,seconds=None,log=None):
    after=probe(output,ffprobe)
    v=after['video']
    checks={'resolution':(after['width'],after['height'])==(1080,1920),
            'codec':v['codec_name']=='h264','pixel_format':v['pix_fmt']=='yuv420p',
            'frames':after['frames']==expected_frames,'fps':Fraction(after['fps'])==Fraction(info['fps']),
            'audio_count':len(after['audio'])==len(info['audio']),
            'audio_codec':all(a['codec_name']=='aac' for a in after['audio']),
            'duration':abs(after['duration']-(info['duration'] if seconds is None else expected_frames/float(Fraction(info['fps']))+info['start']))<=0.1,
            'video_start':abs(after['start']-info['start'])<0.002}
    for key in ('color_range','color_space','color_transfer','color_primaries'):
        old=info['video'].get(key)
        if old and old not in {'unknown','unspecified','reserved'}:
            checks[key]=v.get(key)==old
    for old,new in zip(info['audio'],after['audio']):
        checks[f'audio_start_{old["index"]}']=abs(float(old.get('start_time',0))-float(new.get('start_time',0)))<0.03
        checks[f'audio_rate_channels_{old["index"]}']=(old.get('sample_rate'),old.get('channels'))==(new.get('sample_rate'),new.get('channels'))
    execute([ffmpeg,'-v','error','-xerror','-nostdin','-i',output,'-f','null','-'],log)
    checks['decode']=True
    if not all(checks.values()):
        raise UpscaleError('Validación fallida: '+json.dumps(checks))
    return after,checks


def run_job(args):
    source=Path(args.input).resolve(strict=True)
    output=Path(args.output).absolute()
    if output.suffix.lower()!='.mp4':
        raise UpscaleError('La salida debe tener extensión .mp4')
    if output.exists() or output.is_symlink() or output.resolve()==source:
        raise UpscaleError('La salida ya existe o coincide con el original')
    if not 0<=args.sharpness<=1 or not 0<args.ai_strength<=1 or (args.seconds is not None and (not math.isfinite(args.seconds) or args.seconds<=0)):
        raise UpscaleError('Nitidez: 0–1; mezcla IA: >0–1; duración de muestra: >0')
    ffmpeg=find_tool('ffmpeg',args.ffmpeg)
    ffprobe=find_tool('ffprobe',args.ffprobe)
    info=probe(source,ffprobe)
    if info['video'].get('color_transfer') in {'smpte2084','arib-std-b67'}:
        raise UpscaleError('HDR requiere un flujo de color específico; no se convierte silenciosamente a SDR')
    if info['video'].get('sample_aspect_ratio','1:1') not in {'1:1','0:1','N/A'}:
        raise UpscaleError('Píxel no cuadrado: normalizar SAR antes de este preset')
    if args.mode=='quality' and not info['cfr']:
        raise UpscaleError('El modo quality no admite VFR sin adaptar los tiempos; usar fast conserva timestamps')
    # El preset conserva contenido: una entrada horizontal tendrá bandas, no recorte.
    fps=Fraction(info['fps'])
    expected=info['frames'] if args.seconds is None else min(info['frames'],max(1,math.floor(args.seconds*float(fps))))
    if not expected:
        raise UpscaleError('No se pudieron contar cuadros')
    engine=None
    gpu=None
    if args.mode=='quality':
        engine=find_tool('realesrgan-ncnn-vulkan',args.engine)
        gpu=choose_gpu(vulkan_devices()['devices'],args.gpu)
        models=Path(engine).parent/'models'
        if not all((models/f'realesrgan-x4plus.{suffix}').is_file() for suffix in ('bin','param')):
            raise UpscaleError('Faltan los modelos realesrgan-x4plus junto al ejecutable')
    output.parent.mkdir(parents=True,exist_ok=True)
    estimate=int(info['width']*info['height']*3*17*expected*1.1) if engine else source.stat().st_size*3
    if shutil.disk_usage(output.parent).free<estimate:
        raise UpscaleError(f'Espacio insuficiente: estimación conservadora de trabajo {estimate/1024**3:.1f} GiB')
    report_path=output.with_suffix('.json')
    log=output.with_suffix('.log')
    if report_path.exists() or log.exists():
        raise UpscaleError('Ya existen informe/log para esa salida; elegí un nombre nuevo')
    log.touch(exist_ok=False)
    digest=sha256(source)
    backup=backup_source(source,output.parent/'originals',digest)
    start=time.monotonic()
    with scratch(args.work_dir or output.parent/'.upscale-work',args.keep_work) as work:
        try:
            candidate=work/'candidate.mp4'
            g=geometry_filter(color=info['video'].get('color_space'),rng=info['video'].get('color_range'))
            s=sharp_filter(args.sharpness)+color_filter(info)
            if args.mode=='fast':
                cmd=[ffmpeg,'-v','error','-xerror','-nostdin','-n','-copyts','-i',source,
                     '-map',f'0:{info["video"]["index"]}','-map','0:a?','-map_metadata','0','-vf',g+s]
            else:
                inputs,ups=work/'input',work/'ai'
                inputs.mkdir()
                ups.mkdir()
                execute([ffmpeg,'-v','error','-xerror','-nostdin','-n','-i',source,
                         '-map',f'0:{info["video"]["index"]}','-frames:v',expected,'-fps_mode','passthrough',inputs/'%08d.png'],log)
                if len(list(inputs.glob('*.png')))!=expected:
                    raise UpscaleError('La extracción perdió cuadros')
                # x4plus es ×4 nativo: no pasar -s 2 o 1.5 a ese modelo.
                print(f'IA: {expected} cuadros, GPU Vulkan {gpu}; modelo x4plus ×4',file=sys.stderr,flush=True)
                execute([engine,'-i',inputs,'-o',ups,'-m',Path(engine).parent/'models',
                         '-n','realesrgan-x4plus','-s','4','-t',args.tile,'-g',gpu,'-j','1:1:1','-f','png'],log,timeout=86400)
                if len(list(ups.glob('*.png')))!=expected:
                    raise UpscaleError('Real-ESRGAN perdió cuadros; revisar el log y espacio libre')
                cmd=[ffmpeg,'-v','error','-xerror','-nostdin','-n','-copyts','-itsoffset',str(info['start']),
                     '-framerate',info['fps'],'-i',ups/'%08d.png','-i',source]
                graph=f'[0:v]{g},format=yuv420p[ai];[1:{info["video"]["index"]}]{g},format=yuv420p[lz];[lz][ai]blend=all_expr=A*{1-args.ai_strength}+B*{args.ai_strength}{s}[v]'
                cmd+=['-filter_complex',graph,'-map','[v]','-map','1:a?','-map_metadata','1']
            cmd+=['-c:v','libx264','-preset','medium','-pix_fmt','yuv420p','-fps_mode','passthrough',
                  '-enc_time_base:v',info['video']['time_base'],'-b:v',bitrate(info['fps']),
                  '-maxrate',bitrate(info['fps']),'-bufsize','24M',*audio_options(info),*color_options(info)]
            if args.seconds is not None:
                cmd+=['-frames:v',expected,'-t',str(expected/float(fps)+info['start'])]
            cmd+=['-movflags','+faststart',candidate]
            execute(cmd,log)
            after,checks=validate(info,candidate,ffmpeg,ffprobe,expected,args.seconds,log)
            if sha256(source)!=digest:
                raise UpscaleError('El original cambió durante el trabajo; no se publica la salida')
            with output.open('xb') as dest,candidate.open('rb') as src:
                shutil.copyfileobj(src,dest)
            after['path']=str(output)
            after['raw']['format']['filename']=str(output)
            report={'schema_version':1,'ok':True,'mode':args.mode,'preset':args.preset,'input':str(source),
                    'output':str(output),'backup':backup,'input_sha256':digest,'output_sha256':sha256(output),
                    'input_info':info,'output_info':after,'checks':checks,'seconds':args.seconds,
                         'frames':expected,'sharpness':args.sharpness,'ai_strength':args.ai_strength if engine else 0,
                    'gpu':gpu,'model':'realesrgan-x4plus' if engine else None,'bitrate_reference':bitrate(info['fps']),
                    'elapsed_seconds':time.monotonic()-start,'work_dir':str(work) if args.keep_work else None,
                    'visual_improvement_claimed':False,
                    'notes':['La IA estima detalle; revisar rostro, texto y estabilidad temporal. No se usa GFPGAN, grano ni interpolación.']}
            write_json(report_path,report)
            return report
        except Exception as exc:
            with log.open('a',encoding='utf-8') as handle:
                handle.write(f'ERROR: {exc}\n')
            raise


def preview(source,fast,quality,outdir,ffmpeg,ffprobe):
    try:
        from PIL import Image,ImageDraw,ImageFont
    except ImportError as exc:
        raise UpscaleError('La comparación requiere Pillow: python -m pip install Pillow') from exc
    outdir=Path(outdir).absolute()
    outdir.mkdir(parents=True,exist_ok=True)
    if (outdir/'comparison.json').exists():
        raise UpscaleError('Ya existe una comparación en ese directorio')
    q=probe(quality,ffprobe)
    f=probe(fast,ffprobe)
    original=probe(source,ffprobe)
    if f['frames']!=q['frames'] or Fraction(f['fps'])!=Fraction(q['fps']) or Fraction(q['fps'])!=Fraction(original['fps']):
        raise UpscaleError('Los clips comparativos no tienen los mismos cuadros/FPS que la muestra de origen')
    indices=sorted({0,q['frames']//2,max(0,q['frames']-1)})
    files=[]
    for index in indices:
        columns=[]
        for label,path in [('Original (visualización 1080p)',source),('Lanczos',fast),('Real-ESRGAN + Lanczos',quality)]:
            with scratch(outdir/'.preview-work') as work:
                png=work/'frame.png'
                execute([ffmpeg,'-v','error','-n','-i',path,'-vf',f"select='eq(n,{index})'",
                         '-frames:v','1','-fps_mode','passthrough',png])
                with Image.open(png) as im:
                    im=im.convert('RGB')
                    if im.size!=(1080,1920):
                        # El original se muestra ampliado, no se afirma detalle nuevo.
                        from PIL import ImageOps
                        im=ImageOps.pad(im,(1080,1920),method=Image.Resampling.NEAREST,color='black')
                    columns.append((label,im.copy()))
        for kind,box in [('full',None),('detail',(270,160,810,800))]:
            tiles=[(label,im.crop(box) if box else im) for label,im in columns]
            w,h=tiles[0][1].size
            sheet=Image.new('RGB',(w*3,h+54),'#161616')
            draw=ImageDraw.Draw(sheet)
            try:
                font=ImageFont.truetype('arial.ttf',24)
            except OSError:
                font=ImageFont.load_default()
            for n,(label,im) in enumerate(tiles):
                sheet.paste(im,(n*w,54))
                draw.text((n*w+10,12),label,font=font,fill='white')
            target=outdir/f'{kind}-{index:06d}.png'
            if target.exists():
                raise UpscaleError(f'La comparación ya existe: {target}')
            sheet.save(target)
            files.append(str(target))
    data={'source':str(Path(source).resolve()),'source_sha256':sha256(source),
          'fast':str(fast),'quality':str(quality),'frames':indices,'images':files,
          'selection':None,'reason':None,'instruction':'Revisar al 100 % y en movimiento; registrar selection/reason antes de afirmar una mejoría.'}
    write_json(outdir/'comparison.json',data)
    return data


def doctor(args):
    result={'vulkan':vulkan_devices()}
    for name,explicit in [('ffmpeg',args.ffmpeg),('ffprobe',args.ffprobe),('realesrgan-ncnn-vulkan',args.engine)]:
        try:
            exe=find_tool(name,explicit)
            result[name]={'path':exe}
            if not name.startswith('real'):
                result[name]['version']=execute([exe,'-version']).splitlines()[0]
        except UpscaleError as exc:
            result[name]={'error':str(exc)}
    if args.test_engine:
        try:
            from PIL import Image
        except ImportError as exc:
            raise UpscaleError('La prueba del motor requiere Pillow: python -m pip install Pillow') from exc
        exe=find_tool('realesrgan-ncnn-vulkan',args.engine)
        gpu=choose_gpu(result['vulkan']['devices'],args.gpu)
        with scratch(project_root()/'tmp/upscale-ai/doctor') as work:
            Image.new('RGB',(16,16),(120,80,60)).save(work/'in.png')
            execute([exe,'-i',work/'in.png','-o',work/'out.png','-m',Path(exe).parent/'models',
                     '-n','realesrgan-x4plus','-s','4','-t','128','-g',gpu,'-j','1:1:1'],timeout=120)
            with Image.open(work/'out.png') as im:
                if im.size!=(64,64):
                    raise UpscaleError('La prueba del motor no produjo ×4 real')
            result['engine_test']={'ok':True,'gpu':gpu,'input':[16,16],'output':[64,64]}
    result['fast_ready']=all('error' not in result[n] for n in ('ffmpeg','ffprobe'))
    result['quality_ready']=result['fast_ready'] and result['vulkan']['available'] and 'error' not in result['realesrgan-ncnn-vulkan']
    result['ok']=result['fast_ready'] and (not args.test_engine or result['quality_ready'])
    return result


def parser():
    p=argparse.ArgumentParser(description='Superresolución local de video: Lanczos y Real-ESRGAN')
    sub=p.add_subparsers(dest='operation',required=True)
    for operation in ('doctor','probe','run','compare','preview','batch'):
        s=sub.add_parser(operation)
        s.add_argument('--ffmpeg')
        s.add_argument('--ffprobe')
        s.add_argument('--engine')
        s.add_argument('--verbose',action='store_true')
        if operation=='doctor':
            s.add_argument('--test-engine',action='store_true')
            s.add_argument('--gpu',type=int)
        else:
            s.add_argument('input',type=Path)
        if operation in {'run','compare','batch'}:
            s.add_argument('--mode',choices=['fast','quality'],default='quality')
            s.add_argument('--preset',choices=['youtube-shorts-1080p'],default='youtube-shorts-1080p')
            s.add_argument('--sharpness',type=float,default=0)
            s.add_argument('--ai-strength',type=float,default=0.35)
            s.add_argument('--tile',type=int,choices=[32,64,128,256],default=128)
            s.add_argument('--gpu',type=int)
            s.add_argument('--seconds',type=float,default=1 if operation=='compare' else None)
            s.add_argument('--work-dir',type=Path)
            s.add_argument('--keep-work',action='store_true')
        if operation=='run':
            s.add_argument('--output',type=Path,required=True)
        if operation in {'compare','preview','batch'}:
            s.add_argument('--output-dir',type=Path,required=True)
        if operation=='preview':
            s.add_argument('--fast',type=Path,required=True)
            s.add_argument('--quality',type=Path,required=True)
    return p


def main():
    if hasattr(sys.stdout,'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    args=parser().parse_args()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
    try:
        if sys.version_info<(3,11):
            raise UpscaleError('Se requiere Python 3.11 o superior')
        if args.operation=='doctor':
            result=doctor(args)
        elif args.operation=='probe':
            result=probe(args.input,find_tool('ffprobe',args.ffprobe))
        elif args.operation=='run':
            result=run_job(args)
        elif args.operation=='compare':
            args.output_dir.mkdir(parents=True,exist_ok=True)
            reports={}
            for mode in ('fast','quality'):
                options=argparse.Namespace(**vars(args))
                options.mode=mode
                options.output=args.output_dir/f'{mode}.mp4'
                reports[mode]=run_job(options)
            result=preview(args.input,reports['fast']['output'],reports['quality']['output'],
                           args.output_dir/'preview',find_tool('ffmpeg',args.ffmpeg),find_tool('ffprobe',args.ffprobe))
        elif args.operation=='preview':
            result=preview(args.input,args.fast,args.quality,args.output_dir,
                           find_tool('ffmpeg',args.ffmpeg),find_tool('ffprobe',args.ffprobe))
        else:
            source=args.input.resolve(strict=True)
            dest=args.output_dir.resolve()
            if not source.is_dir() or source==dest or source in dest.parents or dest in source.parents:
                raise UpscaleError('Entrada y salida del lote deben ser directorios separados sin anidamiento')
            files=sorted(p for p in source.rglob('*') if p.is_file() and p.suffix.lower() in {'.mp4','.mov','.mkv','.webm'})
            rows=[]
            for path in files:
                opts=argparse.Namespace(**vars(args))
                opts.input=path
                relative=path.relative_to(source)
                opts.output=dest/relative.parent/(relative.name+'.1080p.mp4')
                try:
                    if path.is_symlink():
                        raise UpscaleError('Se omite enlace simbólico')
                    rows.append({'input':str(path),'ok':True,'report':run_job(opts)})
                except (UpscaleError,OSError,ValueError) as exc:
                    rows.append({'input':str(path),'ok':False,'error':str(exc)})
            result={'ok':all(r['ok'] for r in rows),'total':len(rows),'results':rows}
            dest.mkdir(parents=True,exist_ok=True)
            summary=dest/f'batch-{time.time_ns()}.json'
            write_json(summary,result)
        shown=result
        if args.operation=='run':
            shown={k:result[k] for k in ('ok','mode','output','backup','frames','checks','elapsed_seconds')}
            shown['report']=str(Path(args.output).with_suffix('.json'))
        print(json.dumps(shown,ensure_ascii=False,indent=2))
        return 0 if result.get('ok',True) else 1
    except (UpscaleError,OSError,ValueError,KeyError,ZeroDivisionError) as exc:
        print(json.dumps({'ok':False,'error':str(exc)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
