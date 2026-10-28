#!/usr/bin/env python3
"""
Prepara un paquete de borrador para convertir un video en skill.

Hace solo el trabajo mecánico: ingesta, señales del gate, nombres dudosos,
afirmaciones candidatas y fuentes de la descripción. No escribe fichas ni
skills: eso lo completa el agente después de verificar.

Uso:
    python tools/draft_pack.py "https://youtube.com/shorts/XXXX"
    python tools/draft_pack.py "URL" --langs "es,en" --slug mi-video
    python tools/draft_pack.py "URL" --force   # sobrescribe draft.md

Salida: videos/<slug>/draft.md

Códigos de salida:
    0  paquete generado
    1  error de uso, video ilegible o draft existente sin --force
    2  sin subtítulos utilizables
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transcript import download  # noqa: E402
from shorts_gate import CIFRA_PATTERNS, classify, extract_names, normalize  # noqa: E402

BLOCK_RE = re.compile(r"^\[(\d{2}:\d{2})\]\s*(.+)$")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
URL_RE = re.compile(r"https?://[^\s)\]>\"']+")

CLAIM_HINTS = (
    "estrella", "usuario", "cliente", "gratis", "ilimitad", "automatic",
    "dentro de", "plugin", "integra", "millon", "token", "veces", "por ciento",
)


def has_claim(norm_sentence: str) -> bool:
    if any(re.search(pattern, norm_sentence) for pattern in CIFRA_PATTERNS):
        return True
    return any(hint in norm_sentence for hint in CLAIM_HINTS)


def claim_type(norm_sentence: str) -> str:
    if re.search(r"gratis|precio|usd|dolar|euro|paga|suscrip", norm_sentence):
        return "precio"
    if re.search(r"licencia|agpl|\bmit\b|comercial", norm_sentence):
        return "licencia"
    if re.search(r"plugin|integra|dentro de|compatible|mcp\b|conecta", norm_sentence):
        return "integración"
    if re.search(r"\d|%|millon|mil\b|estrella|usuario|cliente|token", norm_sentence):
        return "cifra"
    return "capacidad"


def extract_claims(text: str) -> list[dict]:
    claims: list[dict] = []
    seen: set[str] = set()
    for line in text.splitlines():
        match = BLOCK_RE.match(line.strip())
        if not match:
            continue
        timestamp, body = match.groups()
        for sentence in SENTENCE_SPLIT.split(body):
            sentence = sentence.strip()
            norm = normalize(sentence)
            if len(sentence) < 25 or not has_claim(norm):
                continue
            key = re.sub(r"\W+", " ", norm).strip()
            if key in seen:
                continue
            seen.add(key)
            claims.append({
                "timestamp": timestamp,
                "text": sentence,
                "type": claim_type(norm),
                "status": "pendiente",
                "source": "",
            })
    return claims[:12]


def extract_hook(text: str) -> tuple[str, str] | None:
    for line in text.splitlines():
        match = BLOCK_RE.match(line.strip())
        if not match:
            continue
        timestamp, body = match.groups()
        sentence = SENTENCE_SPLIT.split(body.strip())[0].strip()
        if sentence:
            return timestamp, sentence
    return None


def description_urls(description: str | None) -> list[str]:
    if not description:
        return []
    found: list[str] = []
    for url in URL_RE.findall(description):
        clean = url.rstrip(".,;:")
        if clean not in found:
            found.append(clean)
    return found


def cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def collect_names(meta: dict, text: str) -> list[str]:
    return extract_names(" ".join(filter(None, [
        text,
        meta.get("title") or "",
        meta.get("description") or "",
    ])))


def format_date(value: str | None) -> str:
    if value and len(value) == 8 and value.isdigit():
        return f"{value[:4]}-{value[4:6]}-{value[6:]}"
    return value or "sin dato"


def build_markdown(meta: dict, text: str, gate: dict, claims: list[dict]) -> str:
    duration = meta.get("duration")
    names = collect_names(meta, text)
    sources = description_urls(meta.get("description"))
    hook = extract_hook(text)
    today = datetime.date.today().isoformat()

    lines: list[str] = [
        f"# Draft pack — {meta.get('title') or meta.get('id')}",
        "",
        f"> Generado por `tools/draft_pack.py` el {today}. "
        "No es una ficha ni un skill: es material para verificar y completar.",
        "",
        "## Metadatos",
        "",
        f"- **ID:** {meta.get('id')}",
        f"- **Título:** {meta.get('title')}",
        f"- **Canal:** {(meta.get('channel') or '').strip()}",
        f"- **Duración:** {duration}s" + (" (corta: usar ficha corta)" if duration and duration <= 180 else ""),
        f"- **Publicado:** {format_date(meta.get('upload_date'))}",
        f"- **URL:** {meta.get('webpage_url')}",
        "- **Archivos:** `metadata.json`, `transcript.txt`",
        "",
        "## Gate",
        "",
        f"- **Veredicto preliminar:** `{gate['verdict']}`",
        "- **Señales:** " + ", ".join(
            f"`{key}={value}`" for key, value in gate["signals"].items()
        ),
        "- **Razones:**",
        *[f"  - {reason}" for reason in gate["reasons"]],
        "",
    ]

    if hook:
        lines += [
            "## Gancho",
            "",
            f"> \"{hook[1]}\" [{hook[0]}]",
            "",
        ]

    lines += [
        "## Nombres a confirmar",
        "",
        "| Detectado | Nombre real | Fuente que lo confirma |",
        "|---|---|---|",
    ]
    if names:
        lines += [f"| {cell(name)} |  |  |" for name in names]
    else:
        lines.append("| — |  |  |")
    lines += [
        "",
        "Regla: dos candidatos por nombre y confirmación en repo, registro de paquetes o docs oficiales.",
        "",
        "## Afirmaciones candidatas",
        "",
        "| Hora | Texto | Tipo | Estado | Fuente |",
        "|---|---|---|---|---|",
    ]
    if claims:
        for claim in claims:
            lines.append(
                f"| {claim['timestamp']} | {cell(claim['text'])} | {claim['type']} | "
                f"{claim['status']} | {claim['source']} |"
            )
    else:
        lines.append("| — | sin afirmaciones detectadas | — | — | — |")
    lines += [
        "",
        "Tipos: `cifra`, `capacidad`, `precio`, `integración`, `licencia`, `procedimiento`.",
        "Estados: `verificado`, `falso`, `engañoso`, `no verificable`, `pendiente`.",
        "",
        "## Fuentes en la descripción",
        "",
    ]
    lines += [f"- {url}" for url in sources] if sources else ["- ninguna"]
    lines += [
        "",
        "## Próximos pasos",
        "",
        "- [ ] Confirmar cada nombre de la tabla contra la fuente primaria.",
        "- [ ] Verificar cada afirmación y completar estado + fuente.",
        "- [ ] Decidir el veredicto final del gate (`skill-directo`, `skill-derivado`, `solo-ficha`, `descartar`).",
        "- [ ] Completar la ficha desde `templates/ficha-short.md` (≤180 s) o `templates/ficha-video.md`.",
        "- [ ] Proponer en el chat y **esperar aprobación** antes de escribir `SKILL.md`.",
        "",
        "## Propuesta (borrador, no enviar sin verificar)",
        "",
        "```",
        "veredicto: <completar>",
        "skill: <nombre> — <una línea>",
        "plan:  <nombre> — <una línea>",
        "no:    <qué se descarta y por qué>",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Paquete de borrador para convertir un video en skill.")
    parser.add_argument("url", help="URL del video")
    parser.add_argument("--langs", default="es,en,es-orig", help="Idiomas de subtítulos (default: es,en,es-orig)")
    parser.add_argument("--slug", default=None, help="Nombre de carpeta manual")
    parser.add_argument("--force", action="store_true", help="Sobrescribe draft.md si ya existe")
    args = parser.parse_args()

    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    code, directory = download(args.url, langs, args.slug)
    if code != 0 or directory is None:
        return code or 1

    meta_path = directory / "metadata.json"
    transcript_path = directory / "transcript.txt"
    if not meta_path.exists() or not transcript_path.exists():
        print(f"[error] Faltan archivos en {directory}", file=sys.stderr)
        return 1

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    text = transcript_path.read_text(encoding="utf-8")
    gate = classify(text, meta.get("duration"))
    claims = extract_claims(text)
    markdown = build_markdown(meta, text, gate, claims)

    output = directory / "draft.md"
    if output.exists() and not args.force:
        print(
            f"[error] Ya existe {output}. Revisalo o usá --force para regenerarlo.",
            file=sys.stderr,
        )
        return 1

    output.write_text(markdown, encoding="utf-8")
    print(f"[ok] draft pack: {output}")
    print(
        f"     gate: {gate['verdict']} "
        f"(pasos={gate['signals']['pasos']}, cta={gate['signals']['cta']})"
    )
    print(f"     afirmaciones: {len(claims)} | nombres: {len(collect_names(meta, text))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
