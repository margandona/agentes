# Descargar videos de HeyGen

- **Herramienta:** `tools/download-heygen.py`
- **Fecha:** 2026-10-18

## Uso

```powershell
python tools/download-heygen.py "https://app.heygen.com/videos/...-<id>"
python tools/download-heygen.py "URL" --out "C:\ruta\salida.mp4"
python tools/download-heygen.py "URL" --visible   # muestra el navegador
```

Salida por defecto: `Downloads/heygen-<id>.mp4`.

## Cómo funciona

1. Abre la página del video en Chromium (headless, con anti-detección).
2. Espera a que el reproductor cargue el `src` del MP4.
3. Intercepta la request de red a `files2.heygen.ai/*.mp4`.
4. Descarga el archivo con el contexto del navegador (cookies + headers), que es lo que evita el 403 de CloudFront.

## Requisitos

- Python 3.11+ (ya instalado).
- `pip install playwright`
- `playwright install chromium`

## Limitaciones

- La URL firmada caduca en ~7 días. Si el script falla con 403, reintentar (se obtiene una nueva firma al recargar la página).
- Solo videos públicos o compartidos. Videos privados de la cuenta requieren login (no implementado).
- El script no maneja marca de agua: en el plan gratuito de HeyGen, el video descargado puede tener watermark.
- No es un extractor genérico: solo HeyGen.

## Por qué no yt-dlp

yt-dlp no tiene extractor para HeyGen. La única forma confiable es reproducir el flujo del navegador, que es lo que hace este script.
