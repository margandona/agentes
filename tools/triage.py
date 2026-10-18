#!/usr/bin/env python3
"""
Triage rápido de videos: baja solo metadatos (sin transcripción ni subtítulos).

Uso:
    python tools/triage.py "URL1" "URL2" ...
    python tools/triage.py --file urls.txt

Salida: una línea JSON por video, con id, título, canal, duración, fecha y
descripción recortada. Pensado para decidir cuáles merecen ficha antes de
transcribir.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yt_dlp

PROBE_OPTS = {"quiet": True, "no_warnings": True, "skip_download": True}


def probe(url: str) -> dict:
    try:
        with yt_dlp.YoutubeDL(PROBE_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:  # noqa: BLE001
        return {"url": url, "error": str(exc)}

    if info.get("_type") == "playlist":
        entries = [e for e in (info.get("entries") or []) if e]
        info = entries[0] if entries else info

    title = info.get("title") or ""
    description = (info.get("description") or "").strip()
    description = " ".join(description.split())[:280]

    return {
        "id": info.get("id"),
        "url": info.get("webpage_url") or url,
        "title": title,
        "channel": info.get("channel") or info.get("uploader"),
        "duration": info.get("duration"),
        "duration_string": info.get("duration_string"),
        "upload_date": info.get("upload_date"),
        "tags": (info.get("tags") or [])[:8],
        "description": description,
    }


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Triage de metadatos de videos.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("urls", nargs="*", help="URLs a triar")
    group.add_argument("--file", help="Archivo con una URL por línea")
    args = parser.parse_args()

    urls: list[str] = []
    if args.file:
        urls = [line.strip() for line in Path(args.file).read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        urls = args.urls

    for url in urls:
        result = probe(url)
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
