# Backends evaluados

## Fuentes y versiones inspeccionadas

- [Skill FFmpeg](https://github.com/OzzyLennon/ffmpeg-video-watermark-remover-v2), commit `b491714a84279e6a1187b5f487e402630483b3f3`: pipeline extracción → visión → delogo → verificación. Su SKILL.md excluye marcas semitransparentes complejas. Su script usa `-y`, tiene un formato de segmentos distinto al ejemplo del README y rutas `/tmp`; no ejecutarlo sin adaptar esos detalles.
- [Wrapper ProPainter](https://github.com/nftmoondogs/ProPainter-Watermark-Remover), commit `a2928c72e70927e2d78f17a0647d851a045e3b9a`: GUI y ROI de caja envolvente. `setup.bat` apunta a un disco P: del autor. El wrapper puede guardar un video sin audio si falla la mezcla; comprobarlo explícitamente o mezclar audio con FFmpeg de manera controlada.
- [ProPainter oficial](https://github.com/sczhou/ProPainter), commit `e870e79321c31b733e2031af5aa2fb1fe3ac7eec`: inferencia temporal, máscaras y pesos oficiales de release v0.1.0. [Licencia S-Lab](https://github.com/sczhou/ProPainter/blob/main/LICENSE): uso no comercial; uso comercial requiere autorización de sus autores.

## Entorno de esta prueba

Windows, RTX 4050 Laptop 6 GB. Python 3.11.15, torch 2.5.1+cu121, torchvision 0.20.1+cu121. CUDA detectada correctamente. Mantener NumPy <2 para esta combinación; OpenCV 4.10.0.84. Las dependencias se instalan con uv en `tmp/watermark/.venv/`, caché en `tmp/uv-cache/` y Python en `tmp/python/`.

Las rutas temporales son un entorno de ejecución del proyecto, no una dependencia garantizada en instalaciones nuevas. Descargar e inspeccionar ProPainter y preparar Python/FFmpeg/pesos antes de invocar. No se incluye ningún peso ni código upstream en esta skill.

## Máscaras y límites

Una marca repetida puede estimarse comparando parches alineados espacial y temporalmente. Esa técnica solo sirve si las posiciones y formas son estables; revisar la máscara con visión. Máscaras excesivas pueden borrar rasgos faciales. Los píxeles reconstruidos no son evidencia de cómo era la imagen antes de la superposición.

Una muestra no demuestra la calidad de todo el video. Revisar comienzo, centro, final y transiciones, además de reproducción y audio. Si el material queda deformado, entregar la muestra como fallida y documentar qué impide una salida aceptable.
