#!/usr/bin/env python3
"""
Gate rápido para videos cortos (Shorts, Reels, TikToks).

No decide: mide señales en la transcripción y devuelve un veredicto
preliminar que el agente debe confirmar con la ficha corta.

Uso:
    python tools/shorts_gate.py "https://youtube.com/shorts/XXXX"
    python tools/shorts_gate.py "URL1" "URL2" --json

Salida humana por defecto; con --json, una línea JSON por video.

Códigos de salida:
    0  procesó al menos un video
    1  error de uso o fallo inesperado
    2  no pudo obtener subtítulos para ningún video
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

import yt_dlp

ROOT = Path(__file__).resolve().parent.parent
GATE_DIR = ROOT / "tmp" / "gate"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transcript import cues_to_text, parse_vtt, pick_subtitle  # noqa: E402

PROBE_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
}

SUB_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "noprogress": True,
    "skip_download": True,
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitlesformat": "vtt",
    "ignoreerrors": True,
}

# Se comparan contra el texto normalizado: minúsculas y sin acentos.
CTA_PATTERNS = (
    r"\bcomenta",
    r"\blink en (la )?bio\b",
    r"\blink\b.{0,20}\bbio\b",
    r"\bboveda\b",
    r"\bsigueme\b",
    r"\bseguime\b",
    r"\bmanda(me)? (un )?dm\b",
    r"\btelegram\b",
    r"\bwhatsapp\b",
)

CIFRA_PATTERNS = (
    r"\d[\d.,]*\s*%",
    r"\b\d{1,3}(?:[.,]\d{3})+\b",
    r"\d[\d.,]*\s*(millones?|mil|k)\b",
    r"\b\d[\d.,]*\s*(usd|dolares|euros)\b",
    r"\bgratis\b",
    r"\bgratuit[oa]s?\b",
    r"\bilimitad[oa]s?\b",
    r"\bde por vida\b",
)

PASO_PATTERNS = (
    r"\binstala\b",
    r"\binstalalo\b",
    r"\binstalala\b",
    r"\babre\b",
    r"\babri\b",
    r"\bejecuta",
    r"\bcorre\b",
    r"\bconfigura",
    r"\bcopia\b",
    r"\bpega\b",
    r"\bagrega",
    r"\banadi",
    r"\banade\b",
    r"\bcrea\b",
    r"\bentra\b",
)

FUENTE_PATTERNS = (
    r"https?://",
    r"\bgithub\.com\b",
    r"\bnpm install\b",
    r"\bpip install\b",
    r"\bdocs\.",
    r"\b[a-z0-9-]+\.(dev|ai|io|com)/",
)

VERDICT_NEXT = {
    "prometedor": "Abrir ficha corta, recuperar nombres del ASR y verificar cada cifra.",
    "revisar": "Abrir ficha corta; sin procedimiento claro, a lo sumo skill-derivado.",
    "descartar": "Una fila en videos/INDEX.md con el motivo; no escribir skill.",
}


def normalize(text: str) -> str:
    """Minúsculas, sin acentos, espacios colapsados."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text)


def hits(text: str, patterns: tuple[str, ...]) -> list[str]:
    found = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            found.append(match.group(0).strip())
    return sorted(set(found))


STOPWORDS_PRIMERA = {
    "entonces", "ademas", "pero", "aunque", "cuando", "donde", "porque",
    "mientras", "luego", "despues", "ahora", "asi", "tambien", "todo",
    "todos", "cada", "este", "esta", "estos", "estas", "ese", "esa", "eso",
    "claro", "bueno", "vale", "nada", "alguien", "nadie", "menos",
}


def extract_names(text: str) -> list[str]:
    """Nombres a confirmar: CamelCase y pares de palabras capitalizadas."""
    camel = re.findall(r"\b[A-Za-z]*[a-z][A-Z][A-Za-z0-9]*\b", text)
    bigrams = [
        pair for pair in re.findall(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b", text)
        if pair.split()[0].lower() not in STOPWORDS_PRIMERA
    ]
    seen: list[str] = []
    for name in camel + bigrams:
        if name not in seen:
            seen.append(name)
    return seen[:10]


def classify(text: str, duration: int | None) -> dict:
    """Calcula señales y veredicto preliminar. Función pura: no toca la red."""
    norm = normalize(text)
    cta = hits(norm, CTA_PATTERNS)
    cifras = hits(norm, CIFRA_PATTERNS)
    pasos = hits(norm, PASO_PATTERNS)
    fuentes = hits(norm, FUENTE_PATTERNS)
    nombres = extract_names(text)

    signals = {
        "duracion_corta": duration is not None and duration <= 180,
        "cta": bool(cta),
        "cifras": bool(cifras),
        "pasos": bool(pasos),
        "fuentes": bool(fuentes),
        "nombres_raros": len(nombres),
    }

    reasons: list[str] = []
    if duration is not None and duration > 180:
        reasons.append("duración > 180 s: corresponde video-a-skill, no ficha corta")
    if cta and not pasos:
        reasons.append("CTA sin procedimiento")
    if cifras and not fuentes:
        reasons.append("cifras sin fuente en el video")
    if not fuentes:
        reasons.append("sin URL ni repo en el video: verificar por fuera")
    if nombres:
        reasons.append("nombres en CamelCase: confirmar contra la fuente (el ASR puede deformarlos)")
    if not pasos:
        reasons.append("sin pasos reproducibles")

    if not pasos and not fuentes and not cifras:
        verdict = "descartar"
    elif pasos and (fuentes or nombres):
        verdict = "prometedor"
    else:
        verdict = "revisar"

    if duration is not None and duration > 180:
        verdict = "revisar"

    return {
        "signals": signals,
        "details": {
            "cta": cta,
            "cifras": cifras,
            "pasos": pasos,
            "fuentes": fuentes,
            "nombres_raros": nombres,
        },
        "verdict": verdict,
        "reasons": reasons or ["sin señales negativas; confirmar en la ficha"],
        "next": VERDICT_NEXT[verdict],
    }


def probe(url: str) -> dict:
    with yt_dlp.YoutubeDL(PROBE_OPTS) as ydl:
        info = ydl.extract_info(url, download=False)
    if info.get("_type") == "playlist":
        entries = [e for e in (info.get("entries") or []) if e]
        if not entries:
            raise ValueError("La playlist está vacía.")
        info = entries[0]
    return info


def fetch_text(url: str, video_id: str, langs: list[str]) -> str | None:
    directory = GATE_DIR / video_id
    directory.mkdir(parents=True, exist_ok=True)
    opts = dict(SUB_OPTS)
    opts["subtitleslangs"] = langs
    opts["outtmpl"] = str(directory / f"{video_id}.%(ext)s")
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as exc:  # noqa: BLE001
        # Un idioma puede fallar (429, formato) y otro haber bajado igual.
        print(f"[warn] {video_id}: descarga de subtítulos incompleta: {exc}", file=sys.stderr)
    subtitle = pick_subtitle(directory, video_id, langs)
    if subtitle is None:
        return None
    text = cues_to_text(parse_vtt(subtitle))
    return text if text.strip() else None


def analyse(url: str, langs: list[str]) -> dict | None:
    info = probe(url)
    video_id = info.get("id") or "video"
    duration = info.get("duration")
    text = fetch_text(url, video_id, langs)
    if text is None:
        print(
            f"[warn] {video_id}: sin subtítulos en {', '.join(langs)}. "
            "Probá --langs o transcribí con whisper local.",
            file=sys.stderr,
        )
        return None
    result = classify(text, duration)
    return {
        "id": video_id,
        "title": info.get("title"),
        "channel": info.get("channel") or info.get("uploader"),
        "duration": duration,
        "words": len(text.split()),
        "signals": result["signals"],
        "details": result["details"],
        "verdict": result["verdict"],
        "reasons": result["reasons"],
        "next": result["next"],
    }


def print_human(result: dict) -> None:
    flags = [name for name, value in result["signals"].items() if value is True]
    print(f"[{result['verdict']}] {result['id']} — {result['title']}")
    print(f"  canal: {result['channel']} | duración: {result['duration']}s | palabras: {result['words']}")
    print(f"  señales: {', '.join(flags) or 'ninguna'}")
    for reason in result["reasons"]:
        print(f"  - {reason}")
    if result["details"]["nombres_raros"]:
        print(f"  nombres a confirmar: {', '.join(result['details']['nombres_raros'][:8])}")
    print(f"  siguiente: {result['next']}")
    print()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Gate de señales para videos cortos.")
    parser.add_argument("urls", nargs="+", help="URLs a analizar")
    parser.add_argument("--langs", default="es,en,es-orig", help="Idiomas de subtítulos (default: es,en,es-orig)")
    parser.add_argument("--json", action="store_true", help="Una línea JSON por video")
    try:
        args = parser.parse_args()
    except SystemExit as exc:  # argparse usa 2 para errores de uso
        return 0 if exc.code == 0 else 1

    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    ok = 0
    for url in args.urls:
        try:
            result = analyse(url, langs)
        except Exception as exc:  # noqa: BLE001
            print(f"[error] {url}: {exc}", file=sys.stderr)
            continue
        if result is None:
            continue
        ok += 1
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print_human(result)

    if ok == 0:
        print("[error] No se pudo analizar ningún video.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
