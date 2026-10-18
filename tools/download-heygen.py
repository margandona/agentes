#!/usr/bin/env python3
"""
Descarga un video de HeyGen (app.heygen.com/videos/...) usando Playwright.

Por qué Playwright y no curl/yt-dlp: HeyGen sirve el MP4 por CloudFront con
una URL firmada ligada a la sesión del navegador. Desde la terminal (curl,
yt-dlp, urllib) devuelve 403. Playwright reproduce el flujo del navegador:
abre la página, captura la request del MP4 y descarga con el mismo contexto
(cookies + headers), que sí es aceptado.

Uso:
    python tools/download-heygen.py "https://app.heygen.com/videos/...-<id>"
    python tools/download-heygen.py "URL" --out "C:\\ruta\\salida.mp4"

Requisitos:
    pip install playwright
    playwright install chromium
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> int:
    parser = argparse.ArgumentParser(description="Descarga un video de HeyGen.")
    parser.add_argument("url", help="URL del video en app.heygen.com")
    parser.add_argument("--out", help="Ruta de salida (default: Downloads/heygen-<id>.mp4)")
    parser.add_argument("--headless", action="store_true", default=True, help="Ejecutar sin ventana (default)")
    parser.add_argument("--visible", action="store_true", help="Mostrar el navegador")
    args = parser.parse_args()

    headless = not args.visible

    if args.out:
        out = Path(args.out)
    else:
        vid_id = args.url.rstrip("/").split("/")[-1].split("-")[-1] or "video"
        out = Path.home() / "Downloads" / f"heygen-{vid_id}.mp4"

    captured: list[str] = []

    def on_request(req):
        u = req.url
        if "files2.heygen.ai" in u and ".mp4" in u and u not in captured:
            captured.append(u)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless, args=["--disable-blink-features=AutomationControlled"])
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
            )
            page = context.new_page()
            page.on("request", on_request)
            print("Abriendo pagina de HeyGen...")
            page.goto(args.url, wait_until="networkidle", timeout=60000)
            try:
                page.wait_for_selector('video[src*="files2.heygen.ai"]', timeout=30000)
            except Exception:
                pass
            page.wait_for_timeout(2000)

            for i in range(20):
                if captured:
                    break
                page.wait_for_timeout(1000)

            if not captured:
                print("No se capturo el MP4 en el primer intento. Recargando...")
                page.reload(wait_until="networkidle", timeout=60000)
                try:
                    page.wait_for_selector('video[src*="files2.heygen.ai"]', timeout=30000)
                except Exception:
                    pass
                page.wait_for_timeout(2000)
                for i in range(20):
                    if captured:
                        break
                    page.wait_for_timeout(1000)

            if not captured:
                browser.close()
                print("ERROR: no se encontro ninguna URL de MP4 en la pagina.", file=sys.stderr)
                return 1

            mp4_url = captured[0]
            print("URL de video capturada. Descargando...")
            resp = context.request.get(mp4_url, timeout=300000)
            if resp.status != 200:
                print(f"ERROR: descarga fallo con status {resp.status}", file=sys.stderr)
                browser.close()
                return 1
            data = resp.body()
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "wb") as f:
                f.write(data)
            browser.close()
            print(f"OK: {len(data)} bytes -> {out}")
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
