"""Pruebas de integración locales: ejecutar desde PowerShell con el entorno de video."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
import tkinter as tk
from types import SimpleNamespace
from PIL import ImageGrab
from app import Studio
from worker import ROOT, execute, tool


def main():
    with tempfile.TemporaryDirectory(dir=ROOT / 'tmp', prefix='studio-test-') as scratch:
        base = Path(scratch)
        video = base / 'entrada.mp4'
        subprocess.run([tool('ffmpeg'), '-v', 'error', '-n', '-f', 'lavfi', '-i', 'testsrc2=size=180x320:rate=25:duration=0.32', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=0.32', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-metadata', 'comment=private-test', video], check=True)
        digest = hashlib.sha256(video.read_bytes()).hexdigest()
        job = dict(inputs=[{'path': str(video)}], output=str(base/'salida'), sample=True, compare=False, restore=False, upscale=True, metadata=True, mode='fast', sharpness='0')
        assert execute(job), 'Fallo de integración escalado + metadatos'
        report = json.loads((base/'salida/resumen.json').read_text(encoding='utf-8'))
        assert report[0]['ok'] and Path(report[0]['output']).is_file()
        assert hashlib.sha256(video.read_bytes()).hexdigest() == digest
        data = json.loads(subprocess.check_output([tool('ffprobe'), '-v', 'error', '-show_streams', '-of', 'json', report[0]['output']]))
        track = next(s for s in data['streams'] if s['codec_type'] == 'video')
        assert (track['width'], track['height'], track['pix_fmt']) == (1080, 1920, 'yuv420p')
        root = tk.Tk()
        app = Studio(root)
        app.files = [str(video)]
        app.list.insert('end', video.name)
        app.list.selection_set(0)
        app.select()
        deadline = time.monotonic() + 15
        while app.frame is None and time.monotonic() < deadline:
            root.update()
            time.sleep(.05)
        assert app.frame is not None, 'No carga la vista previa'
        root.update()
        x, y = app.offset
        app.paint(SimpleNamespace(x=x+30, y=y+30))
        assert app.mask.getbbox(), 'El pincel no modifica la máscara'
        app.clear_mask()
        assert app.mask.getbbox() is None, 'Limpiar máscara falló'
        app.output.set(str(base/'desde-interfaz'))
        app.start(sample=True)
        deadline = time.monotonic() + 30
        while app.busy and time.monotonic() < deadline:
            root.update()
            time.sleep(.05)
        assert not app.busy and (app.last_output/'resumen.json').is_file(), 'El trabajo desde la interfaz no termina'
        assert json.loads((app.last_output/'resumen.json').read_text(encoding='utf-8'))[0]['ok']
        capture = ROOT/'tmp/video-studio'
        capture.mkdir(exist_ok=True)
        root.attributes('-topmost', True)
        root.lift()
        root.update()
        time.sleep(.5)
        root.update()
        ImageGrab.grab(bbox=(root.winfo_rootx(), root.winfo_rooty(), root.winfo_rootx()+root.winfo_width(), root.winfo_rooty()+root.winfo_height())).save(capture/'interfaz.png')
        root.destroy()
        print('OK: integración real, salida 1080p, original intacto, ventana, vista previa y máscara.')


if __name__ == '__main__':
    main()
