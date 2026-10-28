"""Ejecutor local por ventanas para ProPainter; requiere Pillow, NumPy y backend instalado."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from PIL import Image, ImageFilter


def run(cmd, cwd=None, log=None):
    result = subprocess.run([str(a) for a in cmd], cwd=cwd, capture_output=True,
                            encoding='utf-8', errors='replace', timeout=1800, shell=False)
    if log:
        log.write_text(result.stdout+'\n'+result.stderr, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'Falló {cmd[0]}: {result.stderr[-2000:]}')
    return result.stdout


def restore(args):
    source, output = args.input.resolve(strict=True), args.output.absolute()
    model = args.model.resolve(strict=True)
    mask_path = args.mask.resolve(strict=True)
    work = args.work.absolute()
    if output.exists() or output.is_symlink() or output.resolve()==source:
        raise ValueError('La salida debe ser nueva y distinta al original')
    if not (model/'inference_propainter.py').is_file():
        raise ValueError('Falta inference_propainter.py en --model')
    if args.chunk_frames<4 or args.width<128 or args.height<128 or args.width%8 or args.height%8:
        raise ValueError('Usá al menos 4 cuadros y dimensiones >=128 múltiplos de 8')
    if work.exists():
        raise ValueError('El directorio de trabajo debe ser nuevo para evitar mezclar resultados')
    work.mkdir(parents=True)
    # Caché persistente y escribible: evita reconstruir fuentes en cada proceso.
    os.environ['MPLCONFIGDIR']=str(work/'mpl-cache')
    originals, restored = work/'originals',work/'restored'
    originals.mkdir()
    restored.mkdir()
    probe=json.loads(run([args.ffprobe,'-v','error','-show_streams','-show_format','-of','json',source]))
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    fps=video['avg_frame_rate']
    fps_float=eval_fraction(fps)
    if abs(fps_float-round(fps_float))>1e-6:
        raise ValueError('Este ejecutor admite FPS enteros constantes; requiere adaptación para VFR/fraccional')
    if video.get('r_frame_rate')!=fps:
        raise ValueError('Posible video VFR: revisar timestamps antes de reconstruir')
    extraction=[args.ffmpeg,'-v','error','-n','-i',source]
    if args.limit_frames:
        extraction += ['-frames:v',args.limit_frames]
    extraction += ['-fps_mode','passthrough',originals/'%06d.png']
    run(extraction)
    frames=sorted(originals.glob('*.png'))
    if not frames:
        raise ValueError('No se extrajeron cuadros')
    size=(int(video['width']),int(video['height']))
    mask=Image.open(mask_path).convert('L')
    if mask.size!=size:
        raise ValueError('La máscara debe tener las dimensiones del video')
    small=(args.width,args.height)
    mask.resize(small,Image.Resampling.NEAREST).save(work/'mask-small.png')
    # Cubrir también la dilatación aplicada por ProPainter; desvanecer el borde.
    blend_mask=mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1))
    start=time.monotonic()
    for index, offset in enumerate(range(0,len(frames),args.chunk_frames)):
        batch=frames[offset:offset+args.chunk_frames]
        if len(batch)==1:
            batch=[frames[offset-1],*batch]
            skip=1
        else:
            skip=0
        chunk=work/f'chunk-{index:04d}'
        inputs=chunk/'input'
        inputs.mkdir(parents=True)
        for n,path in enumerate(batch):
            with Image.open(path) as image:
                image.convert('RGB').resize(small,Image.Resampling.LANCZOS).save(inputs/f'{n:05d}.png')
        run([sys.executable,model/'inference_propainter.py','--video',inputs,'--mask',work/'mask-small.png',
             '--output',chunk/'output','--save_fps',round(fps_float),'--fp16',
             '--neighbor_length','4','--subvideo_length','20','--ref_stride','10',
             '--raft_iter','12','--mask_dilation','2','--save_frames'],cwd=model,log=chunk/'inference.log')
        results=sorted((chunk/'output/input/frames').glob('*.png'))
        if len(results)!=len(batch):
            raise RuntimeError(f'Cantidad de cuadros inesperada en {chunk}')
        for path,result in zip(batch[skip:],results[skip:]):
            with Image.open(path) as original, Image.open(result) as pred:
                pred=pred.convert('RGB').resize(size,Image.Resampling.LANCZOS)
                Image.composite(pred,original.convert('RGB'),blend_mask).save(restored/path.name)
        print(f'Cuadros {min(offset+args.chunk_frames,len(frames))}/{len(frames)}; {time.monotonic()-start:.1f}s',flush=True)
    candidate=work/'candidate.mp4'
    cmd=[args.ffmpeg,'-v','error','-n','-copyts','-itsoffset',video.get('start_time','0'),
         '-framerate',fps,'-i',restored/'%06d.png','-i',source,
         '-map','0:v:0','-map','1:a?','-c:v','libx264','-preset','fast','-crf','18',
         '-pix_fmt','yuv420p','-profile:v','high','-c:a','copy']
    if args.limit_frames:
        cmd+=['-t',str(len(frames)/fps_float+float(video.get('start_time','0')))]
    run([*cmd,'-movflags','+faststart',candidate])
    run([args.ffmpeg,'-v','error','-xerror','-i',candidate,'-f','null','-'])
    after=json.loads(run([args.ffprobe,'-v','error','-show_streams','-show_format','-of','json',candidate]))
    outvideo=next(s for s in after['streams'] if s['codec_type']=='video')
    if outvideo.get('codec_name')!='h264' or outvideo.get('pix_fmt')!='yuv420p':
        raise RuntimeError('La salida debe ser H.264 yuv420p para reproducción compatible')
    if int(outvideo.get('nb_frames',-1))!=len(frames) or (outvideo['width'],outvideo['height'])!=size:
        raise RuntimeError('La verificación de resolución/cuadros falló')
    if not args.limit_frames:
        if abs(float(probe['format']['duration'])-float(after['format']['duration']))>0.1:
            raise RuntimeError('La duración cambió más de 0,1 segundos')
        audio_hashes=[]
        for p in (source,candidate):
            audio_hashes.append(run([args.ffmpeg,'-v','error','-xerror','-i',p,'-map','0:a?',
                                     '-vn','-f','streamhash','-hash','sha256','-']))
        if audio_hashes[0]!=audio_hashes[1]:
            raise RuntimeError('El hash de audio decodificado cambió')
    with output.open('xb') as dest,candidate.open('rb') as src:
        shutil.copyfileobj(src,dest)
    report={'output':str(output),'frames':len(frames),'processing_size':small,'original_size':size,
            'elapsed_seconds':time.monotonic()-start,'backend':'ProPainter','visual_review_required':True,
            'note':'Reconstrucción inferida en regiones enmascaradas; no recupera píxeles originales.'}
    (work/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report


def eval_fraction(value):
    n,d=value.split('/')
    return float(n)/float(d)


def main():
    parser=argparse.ArgumentParser(description='Restauración visual local por ventanas con ProPainter')
    for name in ('input','output','mask','model','work'):
        parser.add_argument('--'+name,required=True,type=Path)
    parser.add_argument('--ffmpeg',default='ffmpeg')
    parser.add_argument('--ffprobe',default='ffprobe')
    parser.add_argument('--chunk-frames',type=int,default=25)
    parser.add_argument('--width',type=int,default=384)
    parser.add_argument('--height',type=int,default=680)
    parser.add_argument('--limit-frames',type=int)
    args=parser.parse_args()
    try:
        print(json.dumps(restore(args),ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as exc:
        print(f'Error: {exc}',file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
