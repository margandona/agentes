#!/usr/bin/env python3
"""
Baja metadatos y subtítulos de un video (YouTube, Bilibili, etc.) y arma
videos/<slug>/metadata.json + transcript.txt.

Uso:
    python tools/transcript.py "https://www.youtube.com/watch?v=XXXX"
    python tools/transcript.py "URL" --langs "es,en"
    python tools/transcript.py "URL" --slug mi-nombre

Requiere: yt-dlp (python -m pip install --user yt-dlp)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import timedelta
from pathlib import Path

import yt_dlp

ROOT = Path(__file__).resolve().parent.parent
VIDEOS = ROOT / "videos"

HEADER_LINES = ("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE", "REGION")


def slugify(value: str, max_len: int = 60) -> str:
    value = value.lower()
    value = (
        value.replace("á", "a").replace("é", "e").replace("í", "i")
        .replace("ó", "o").replace("ú", "u").replace("ñ", "n").replace("ü", "u")
    )
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:max_len].rstrip("-") or "video"


def ts_to_seconds(value: str) -> float:
    value = value.strip().replace(",", ".")
    parts = value.split(":")
    try:
        parts = [float(p) for p in parts]
    except ValueError:
        return 0.0
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0]


def mmss(seconds: float) -> str:
    seconds = int(seconds)
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def clean_caption_line(line: str) -> str:
    line = re.sub(r"<[^>]+>", "", line)          # <c>, <00:00:01.000>, etc.
    line = re.sub(r"\{[^}]*\}", "", line)         # estilos
    line = line.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    line = line.replace("&nbsp;", " ").replace("\u200b", "")
    return re.sub(r"\s+", " ", line).strip()


def parse_vtt(path: Path) -> list[tuple[float, str]]:
    """Devuelve [(segundos, texto)] sin duplicados de captions rodantes."""
    content = path.read_text(encoding="utf-8", errors="replace")
    # YouTube auto-captions usan cues de dos líneas: la primera repite el
    # contexto anterior y la segunda trae las palabras nuevas. Los subtítulos
    # manuales no tienen tags <c> ni <00:..>.
    is_auto = "<c>" in content or "<00:" in content

    cues: list[tuple[float, str]] = []
    current_time = 0.0
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        lines = [x for x in buffer if x]
        buffer = []
        if is_auto and len(lines) > 1:
            lines = lines[-1:]
        text = " ".join(lines)
        if not text:
            return
        if cues and (text == cues[-1][1] or cues[-1][1].endswith(text)):
            return
        if cues and text.startswith(cues[-1][1]) and len(text) - len(cues[-1][1]) < 40:
            cues[-1] = (cues[-1][0], text)
            return
        cues.append((current_time, text))

    for raw in content.splitlines():
        line = raw.strip("\ufeff")
        if "-->" in line:
            flush()
            current_time = ts_to_seconds(line.split("-->")[0])
            continue
        if not line.strip():
            flush()
            continue
        if line.startswith(HEADER_LINES):
            continue
        if re.fullmatch(r"\d+", line):
            continue
        buffer.append(clean_caption_line(line))
    flush()
    return cues


def cues_to_text(cues: list[tuple[float, str]], block_seconds: int = 30) -> str:
    """Agrupa cues en bloques con timestamp para poder citar."""
    if not cues:
        return ""
    blocks: list[list] = []
    for start, text in cues:
        if not blocks or start - blocks[-1][0] >= block_seconds or len(blocks[-1][1]) > 700:
            blocks.append([start, text])
        else:
            blocks[-1][1] += " " + text
    return "\n\n".join(f"[{mmss(start)}] {text}" for start, text in blocks) + "\n"


def pick_subtitle(directory: Path, video_id: str, langs: list[str]) -> Path | None:
    candidates = sorted(directory.glob(f"{video_id}*.vtt"))
    if not candidates:
        return None

    def score(path: Path) -> tuple:
        name = path.name.lower()
        lang = "und"
        for candidate in langs:
            if f".{candidate}." in name or name.endswith(f".{candidate}.vtt"):
                lang = candidate
                break
        manual = 0 if "auto" not in name else 1
        return (manual, langs.index(lang) if lang in langs else 99, len(name))

    return sorted(candidates, key=score)[0]


def download(url: str, langs: list[str], slug_override: str | None) -> int:
    probe_opts = {"quiet": True, "no_warnings": True, "skip_download": True, "extractor_args": {"youtube": {"player_client": ["android", "web"]}}}
    try:
        with yt_dlp.YoutubeDL(probe_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] No pude leer el video: {exc}", file=sys.stderr)
        return 1

    if info.get("_type") == "playlist":
        entries = [e for e in info.get("entries") or [] if e]
        if not entries:
            print("[error] La playlist está vacía.", file=sys.stderr)
            return 1
        info = entries[0]

    video_id = info.get("id") or "video"
    title = info.get("title") or video_id
    slug = slug_override or f"{video_id}-{slugify(title)}"
    directory = VIDEOS / slug
    directory.mkdir(parents=True, exist_ok=True)

    metadata = {
        "id": video_id,
        "title": title,
        "channel": info.get("channel") or info.get("uploader"),
        "channel_url": info.get("channel_url") or info.get("uploader_url"),
        "upload_date": info.get("upload_date"),
        "duration": info.get("duration"),
        "duration_string": info.get("duration_string"),
        "webpage_url": info.get("webpage_url") or url,
        "description": info.get("description"),
        "tags": info.get("tags"),
        "chapters": info.get("chapters"),
        "subtitles_available": sorted((info.get("subtitles") or {}).keys()),
        "automatic_captions_available": sorted((info.get("automatic_captions") or {}).keys()),
    }
    (directory / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    sub_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": langs,
        "subtitlesformat": "vtt",
        "ignoreerrors": True,
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
        "outtmpl": str(directory / f"{video_id}.%(ext)s"),
    }
    try:
        with yt_dlp.YoutubeDL(sub_opts) as ydl:
            ydl.download([url])
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] Falló la descarga de subtítulos: {exc}", file=sys.stderr)

    subtitle = pick_subtitle(directory, video_id, langs)
    if subtitle is None:
        print(
            "[warn] El video no tiene subtítulos en "
            f"{', '.join(langs)}. Probá --langs con otros idiomas, "
            "o transcribí con whisper local.",
            file=sys.stderr,
        )
        return 2

    text = cues_to_text(parse_vtt(subtitle))
    if not text.strip():
        print(f"[warn] El subtítulo {subtitle.name} quedó vacío.", file=sys.stderr)
        return 2

    (directory / "transcript.txt").write_text(text, encoding="utf-8")
    words = len(text.split())
    print(f"[ok] {slug}")
    print(f"     metadata:   {directory / 'metadata.json'}")
    print(f"     transcripción: {directory / 'transcript.txt'} ({words} palabras)")
    print(f"     idioma:     {subtitle.name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Baja metadatos y transcripción de un video.")
    parser.add_argument("url", help="URL del video")
    parser.add_argument(
        "--langs", default="es,en,es-orig",
        help="Idiomas de subtítulos en orden de preferencia (default: es,en,es-orig)",
    )
    parser.add_argument("--slug", default=None, help="Nombre de carpeta manual")
    args = parser.parse_args()

    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    return download(args.url, langs, args.slug)


if __name__ == "__main__":
    raise SystemExit(main())
