"""Trabajador aislado; las skills son responsables de sus validaciones."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import hashlib

ROOT = Path(__file__).resolve().parents[2]
PYTHON = ROOT / 'tmp/watermark/.venv/Scripts/python.exe'
UPSCALE = ROOT / 'skills/video-upscale-ai/scripts/upscale.py'


def tool(name):
    paths = sorted((ROOT / 'tmp/media-tools').rglob(name + '.exe'))
    result = shutil.which(name) or (str(paths[0]) if paths else None)
    if not result:
        raise RuntimeError(f'No se encontró {name}. Revisar instalación de las skills.')
    return result


def call(args):
    print('Ejecutando: ' + ' '.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), check=True, env=os.environ.copy())


def execute(job):
    destination = Path(job['output'])
    destination.mkdir(parents=True, exist_ok=False)
    ffmpeg, ffprobe = tool('ffmpeg'), tool('ffprobe')
    os.environ['PATH'] = os.pathsep.join([str(Path(ffmpeg).parent), str(Path(tool('exiftool')).parent), os.environ.get('PATH', '')])
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    results = []
    for number, item in enumerate(job['inputs'], 1):
        source = Path(item['path']).resolve(strict=True)
        directory = destination / f'{number:03d}-{source.stem}'
        directory.mkdir()
        row = {'input': str(source), 'ok': False}
        try:
            print(f'VIDEO {number}/{len(job["inputs"])}: {source.name}', flush=True)
            original = directory / ('original' + source.suffix)
            shutil.copy2(source, original)
            with original.open('rb') as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            current = original
            if job.get('sample'):
                current = directory / 'muestra.mp4'
                call([ffmpeg, '-v', 'error', '-n', '-i', original, '-t', '2', '-map', '0:v:0', '-map', '0:a?', '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', current])
            if job.get('restore'):
                mask = Path(item.get('mask') or '')
                if not mask.is_file():
                    raise ValueError('Falta la máscara de este video. Dibujar o importar antes de procesar.')
                target = directory / 'restaurado.mp4'
                call([PYTHON, '-u', ROOT / 'skills/video-watermark-restoration/scripts/restore.py', '--input', current,
                      '--output', target, '--mask', mask, '--model', ROOT / 'tmp/watermark/ProPainter',
                      '--work', directory / 'restauracion', '--ffmpeg', ffmpeg, '--ffprobe', ffprobe,
                      '--chunk-frames', '48'])
                current = target
            if job.get('compare'):
                call([PYTHON, '-u', UPSCALE, 'compare', current, '--output-dir', directory / 'comparacion', '--seconds', '2', '--sharpness', job['sharpness']])
            if job.get('upscale') and not job.get('compare'):
                target = directory / '1080p.mp4'
                call([PYTHON, '-u', UPSCALE, 'run', current, '--output', target, '--mode', job['mode'], '--sharpness', job['sharpness']])
                current = target
            if job.get('metadata'):
                target = directory / 'final.mp4'
                call([PYTHON, '-u', ROOT / 'skills/media-metadata-sanitizer/scripts/sanitize.py', current, '--output', target])
                current = target
            with source.open('rb') as stream:
                if hashlib.file_digest(stream, 'sha256').hexdigest() != digest:
                    raise ValueError('El archivo de entrada cambió durante el trabajo.')
            row.update(ok=True, output=str(current), original_sha256=digest)
            print(f'LISTO: {current}', flush=True)
        except Exception as exc:
            row['error'] = str(exc)
            print(f'ERROR: {exc}', flush=True)
        results.append(row)
        (destination / 'resumen.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    return all(row['ok'] for row in results)


if __name__ == '__main__':
    try:
        success = execute(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')))
        raise SystemExit(0 if success else 1)
    except Exception as exc:
        print(f'ERROR: {exc}', flush=True)
        raise SystemExit(1)
