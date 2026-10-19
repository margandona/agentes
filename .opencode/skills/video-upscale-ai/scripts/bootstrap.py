"""Descarga explícita y verificada del motor oficial para Windows, sin proxies."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request
import zipfile

from upscale import UpscaleError, project_root

URL='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip'
SHA256='abc02804e17982a3be33675e4d471e91ea374e65b70167abc09e31acb412802d'


def setup(cache,download=False):
    cache=Path(cache).resolve()
    exe=cache/'engine/realesrgan-ncnn-vulkan.exe'
    if exe.is_file() and (exe.parent/'models/realesrgan-x4plus.bin').is_file():
        return {'ok':True,'engine':str(exe),'downloaded':False}
    if not download:
        raise UpscaleError('Falta el motor local; ejecutar bootstrap.py --download o install.ps1 -DownloadEngine')
    if sys.platform!='win32':
        raise UpscaleError('Este bootstrap está probado en Windows; instalar el paquete oficial de su plataforma y usar --engine')
    cache.mkdir(parents=True,exist_ok=True)
    archive=cache/'engine.zip'
    fetched=False
    if not archive.exists():
        partial=cache/f'engine-{time.time_ns()}.partial'
        request=urllib.request.Request(URL,headers={'User-Agent':'video-upscale-ai/1.0'})
        with urllib.request.urlopen(request,timeout=300) as response,partial.open('xb') as handle:
            while chunk:=response.read(1024*1024):
                handle.write(chunk)
        if hashlib.sha256(partial.read_bytes()).hexdigest()!=SHA256:
            raise UpscaleError(f'El SHA-256 del paquete no coincide; no se ejecuta. Archivo conservado: {partial}')
        partial.rename(archive)
        fetched=True
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=SHA256:
        raise UpscaleError('El ZIP existente no coincide con el paquete verificado; conservarlo y usar una caché nueva')
    target=(cache/'engine').resolve()
    if target.exists():
        raise UpscaleError('El directorio del motor existe pero está incompleto; usar una caché nueva')
    with zipfile.ZipFile(archive) as z:
        for entry in z.infolist():
            candidate=(target/entry.filename).resolve()
            if candidate!=target and target not in candidate.parents:
                raise UpscaleError('El ZIP contiene una ruta fuera del directorio de instalación')
            if (entry.external_attr>>16)&0o170000==0o120000:
                raise UpscaleError('No se admiten enlaces simbólicos en el ZIP')
        z.extractall(target)
    if not exe.is_file():
        raise UpscaleError('El paquete no contiene el ejecutable esperado')
    return {'ok':True,'engine':str(exe),'installed':True,'downloaded':fetched,'archive_sha256':SHA256,'source':URL}


if __name__=='__main__':
    p=argparse.ArgumentParser(description='Instalar motor Real-ESRGAN oficial en caché local')
    p.add_argument('--cache',type=Path,default=project_root()/'tmp/upscale-ai')
    p.add_argument('--download',action='store_true')
    args=p.parse_args()
    try:
        print(json.dumps(setup(args.cache,args.download),ensure_ascii=True,indent=2))
    except (UpscaleError,OSError,urllib.error.URLError,zipfile.BadZipFile) as exc:
        print(f'Error de instalación: {exc}',file=sys.stderr)
        raise SystemExit(1)
