#!/usr/bin/env python3
"""
image-lab :: servidor MCP local para generar íconos e imágenes.

- generate_icon: dibuja un PNG determinista, sin IA ni internet.
- generate_image: usa OpenAI o Gemini si hay una clave configurada.
- list_providers: dice qué claves están disponibles.

Ejecutar:
    uv run --with mcp --with pillow python tools/mcp-image/server.py

No requiere instalar nada en el repo: uv arma el entorno efímero.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("image-lab")

STYLES = [
    "video", "key", "brain", "wrench", "shield", "download", "globe", "chat",
    "sparkle", "film", "tag", "eye", "gear", "robot", "doc", "mic", "lock",
    "browser", "box", "code", "layers", "terminal", "window", "list", "plug",
    "cross", "expand", "eraser", "play", "star",
]


def _hex(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    if len(value) != 6:
        raise ValueError("color debe ser hex, por ejemplo #1F8A70")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


class _ScaledDraw:
    """Dibuja en una grilla 0..100 y escala a los píxeles reales."""

    METHODS = {"line", "polygon", "rectangle", "ellipse",
               "rounded_rectangle", "arc"}

    def __init__(self, draw, k: float):
        self._d = draw
        self._k = k

    def _xy(self, xy):
        if xy and isinstance(xy[0], (tuple, list)):
            return [(x * self._k, y * self._k) for x, y in xy]
        return [v * self._k for v in xy]

    def __getattr__(self, name):
        attr = getattr(self._d, name)
        if name not in self.METHODS:
            return attr

        def wrapper(xy, *args, **kwargs):
            if kwargs.get("width") is not None:
                kwargs["width"] = max(1, int(round(kwargs["width"] * self._k)))
            if kwargs.get("radius") is not None:
                kwargs["radius"] = int(round(kwargs["radius"] * self._k))
            return attr(self._xy(xy), *args, **kwargs)
        return wrapper


def _icon(style: str, d, col, w: float) -> None:
    if style == "video":
        d.rounded_rectangle([15, 25, 85, 75], radius=10, outline=col, width=w)
        d.polygon([(42, 38), (42, 62), (62, 50)], fill=col)
    elif style == "key":
        d.ellipse([12, 42, 42, 72], outline=col, width=w)
        d.line([38, 52, 86, 16], fill=col, width=w)
        d.line([68, 30, 80, 42], fill=col, width=w)
        d.line([78, 22, 90, 34], fill=col, width=w)
    elif style == "brain":
        d.ellipse([22, 25, 78, 78], outline=col, width=w)
        d.arc([30, 35, 66, 70], 200, 340, fill=col, width=w)
        d.arc([38, 42, 72, 76], 20, 160, fill=col, width=w)
        d.line([50, 25, 50, 78], fill=col, width=w)
    elif style == "wrench":
        d.line([18, 82, 68, 32], fill=col, width=w)
        d.arc([55, 8, 90, 43], 90, 300, fill=col, width=w)
        d.line([18, 82, 26, 74], fill=col, width=w)
    elif style == "shield":
        d.polygon([(50, 10), (82, 22), (82, 50), (50, 88), (18, 50), (18, 22)],
                  outline=col, width=w)
        d.line([36, 50, 46, 60, 66, 38], fill=col, width=w, joint="curve")
    elif style == "download":
        d.line([50, 15, 50, 65], fill=col, width=w)
        d.polygon([(32, 50), (68, 50), (50, 72)], fill=col)
        d.line([20, 82, 80, 82], fill=col, width=w)
    elif style == "globe":
        d.ellipse([18, 18, 82, 82], outline=col, width=w)
        d.ellipse([38, 18, 62, 82], outline=col, width=w)
        d.line([18, 50, 82, 50], fill=col, width=w)
    elif style == "chat":
        d.rounded_rectangle([12, 20, 88, 70], radius=12, outline=col, width=w)
        d.polygon([(28, 70), (28, 88), (46, 70)], fill=col)
        for x in (35, 50, 65):
            d.ellipse([x - 3, 42, x + 3, 48], fill=col)
    elif style == "sparkle":
        d.polygon([(50, 8), (58, 38), (88, 46), (58, 54), (50, 84),
                   (42, 54), (12, 46), (42, 38)], outline=col, width=w)
        d.polygon([(78, 60), (82, 72), (94, 76), (82, 80), (78, 92),
                   (74, 80), (62, 76), (74, 72)], fill=col)
    elif style == "film":
        d.rounded_rectangle([12, 22, 88, 78], radius=6, outline=col, width=w)
        for y in (30, 44, 58):
            d.rectangle([18, y, 26, y + 8], outline=col, width=max(1, w - 1))
            d.rectangle([74, y, 82, y + 8], outline=col, width=max(1, w - 1))
        d.line([34, 22, 34, 78], fill=col, width=w)
        d.line([66, 22, 66, 78], fill=col, width=w)
    elif style == "tag":
        d.polygon([(14, 50), (42, 18), (86, 18), (86, 82), (42, 82)],
                  outline=col, width=w)
        d.ellipse([64, 44, 76, 56], fill=col)
    elif style == "eye":
        d.ellipse([10, 32, 90, 68], outline=col, width=w)
        d.ellipse([40, 40, 60, 60], fill=col)
    elif style == "gear":
        d.ellipse([30, 30, 70, 70], outline=col, width=w)
        d.ellipse([44, 44, 56, 56], outline=col, width=w)
        for x1, y1, x2, y2 in [(50, 30, 50, 14), (50, 70, 50, 86),
                               (30, 50, 14, 50), (70, 50, 86, 50),
                               (36, 36, 24, 24), (64, 64, 76, 76),
                               (36, 64, 24, 76), (64, 36, 76, 24)]:
            d.line([x1, y1, x2, y2], fill=col, width=w)
    elif style == "robot":
        d.rounded_rectangle([18, 32, 82, 76], radius=12, outline=col, width=w)
        d.ellipse([32, 46, 42, 56], fill=col)
        d.ellipse([58, 46, 68, 56], fill=col)
        d.line([50, 32, 50, 18], fill=col, width=w)
        d.ellipse([44, 10, 56, 22], outline=col, width=w)
    elif style == "doc":
        d.rounded_rectangle([25, 12, 75, 88], radius=6, outline=col, width=w)
        for y in (34, 50, 66):
            d.line([36, y, 64, y], fill=col, width=w)
    elif style == "mic":
        d.rounded_rectangle([38, 14, 62, 58], radius=12, outline=col, width=w)
        d.line([26, 46, 26, 60], fill=col, width=w)
        d.line([74, 46, 74, 60], fill=col, width=w)
        d.arc([26, 40, 74, 80], 0, 180, fill=col, width=w)
        d.line([50, 80, 50, 90], fill=col, width=w)
    elif style == "lock":
        d.rounded_rectangle([22, 45, 78, 86], radius=6, outline=col, width=w)
        d.arc([32, 18, 68, 62], 180, 360, fill=col, width=w)
        d.ellipse([46, 60, 54, 68], fill=col)
    elif style == "browser":
        d.rounded_rectangle([12, 20, 88, 80], radius=6, outline=col, width=w)
        d.line([12, 34, 88, 34], fill=col, width=w)
        d.ellipse([18, 25, 24, 31], fill=col)
        d.ellipse([28, 25, 34, 31], fill=col)
    elif style == "box":
        d.polygon([(50, 10), (86, 30), (86, 70), (50, 90), (14, 70), (14, 30)],
                  outline=col, width=w)
        d.line([50, 10, 50, 50], fill=col, width=w)
        d.line([14, 30, 50, 50], fill=col, width=w)
        d.line([86, 30, 50, 50], fill=col, width=w)
        d.line([50, 50, 50, 90], fill=col, width=w)
    elif style == "code":
        d.line([34, 28, 14, 50, 34, 72], fill=col, width=w, joint="curve")
        d.line([66, 28, 86, 50, 66, 72], fill=col, width=w, joint="curve")
        d.line([56, 22, 44, 78], fill=col, width=w)
    elif style == "layers":
        d.polygon([(50, 14), (86, 34), (50, 54), (14, 34)], outline=col, width=w)
        d.line([14, 52, 50, 72, 86, 52], fill=col, width=w, joint="curve")
        d.line([14, 68, 50, 88, 86, 68], fill=col, width=w, joint="curve")
    elif style == "terminal":
        d.rounded_rectangle([10, 18, 90, 82], radius=6, outline=col, width=w)
        d.line([24, 38, 36, 50, 24, 62], fill=col, width=w, joint="curve")
        d.line([44, 62, 70, 62], fill=col, width=w)
    elif style == "window":
        d.rounded_rectangle([12, 18, 88, 82], radius=6, outline=col, width=w)
        d.line([12, 34, 88, 34], fill=col, width=w)
        d.line([20, 26, 60, 26], fill=col, width=max(1, w - 1))
    elif style == "list":
        for y in (28, 50, 72):
            d.ellipse([16, y - 4, 24, y + 4], fill=col)
            d.line([32, y, 84, y], fill=col, width=w)
    elif style == "plug":
        d.rounded_rectangle([22, 38, 78, 66], radius=10, outline=col, width=w)
        d.line([38, 38, 38, 20], fill=col, width=w)
        d.line([62, 38, 62, 20], fill=col, width=w)
        d.line([78, 52, 90, 52], fill=col, width=w)
    elif style == "cross":
        d.rectangle([42, 14, 58, 86], outline=col, width=w)
        d.rectangle([14, 42, 86, 58], outline=col, width=w)
    elif style == "expand":
        for x1, y1, x2, y2 in [(14, 34, 14, 14), (14, 14, 34, 14),
                               (66, 14, 86, 14), (86, 14, 86, 34),
                               (86, 66, 86, 86), (86, 86, 66, 86),
                               (34, 86, 14, 86), (14, 86, 14, 66)]:
            d.line([x1, y1, x2, y2], fill=col, width=w)
        d.line([36, 64, 64, 36], fill=col, width=w)
        d.polygon([(64, 36), (64, 50), (50, 36)], fill=col)
    elif style == "eraser":
        d.polygon([(14, 56), (44, 16), (86, 58), (56, 88)], outline=col, width=w)
        d.line([28, 70, 70, 88], fill=col, width=w)
    elif style == "play":
        d.ellipse([14, 14, 86, 86], outline=col, width=w)
        d.polygon([(40, 30), (40, 70), (72, 50)], fill=col)
    elif style == "star":
        pts = []
        for i in range(10):
            import math
            ang = -math.pi / 2 + i * math.pi / 5
            r = 40 if i % 2 == 0 else 18
            pts.append((50 + r * math.cos(ang), 50 + r * math.sin(ang)))
        d.polygon(pts, outline=col, width=w)
    else:
        d.ellipse([26, 26, 74, 74], outline=col, width=w)
        d.line([50, 38, 50, 56], fill=col, width=w)
        d.ellipse([46, 62, 54, 70], fill=col)


@mcp.tool()
def generate_icon(style: str, out_path: str, size: int = 512,
                  color: str = "#1F8A70") -> str:
    """Genera un ícono PNG determinista, sin IA ni internet.

    style: uno de video, key, brain, wrench, shield, download, globe, chat,
    sparkle, film, tag, eye, gear, robot, doc, mic, lock, browser, box, code,
    layers, terminal, window, list, plug, cross, expand, eraser, play, star.
    out_path: ruta del PNG a crear (se crean las carpetas).
    size: lado en píxeles, entre 64 y 2048.
    color: color de línea en hex, por ejemplo #1F8A70.
    """
    if style not in STYLES:
        return f"ERROR: style desconocido: {style}. Usá: {', '.join(STYLES)}"
    if not 64 <= int(size) <= 2048:
        return "ERROR: size debe estar entre 64 y 2048"
    col = _hex(color)
    out = Path(out_path).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    scale = 4
    S = int(size) * scale
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    raw = ImageDraw.Draw(img)
    # fondo circular suave
    raw.ellipse([2 * scale, 2 * scale, S - 2 * scale, S - 2 * scale],
                fill=(238, 247, 243, 255))
    d = _ScaledDraw(raw, S / 100.0)
    _icon(style, d, col, 1.9)
    img = img.resize((int(size), int(size)), Image.LANCZOS)
    img.save(out)
    return f"OK {out.resolve()} ({size}x{size}, estilo {style})"


def _post_json(url: str, payload: dict, headers: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json", **headers}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _save(raw: bytes, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)


@mcp.tool()
def generate_image(prompt: str, out_path: str, provider: str = "auto",
                   size: str = "1024x1024") -> str:
    """Genera una imagen con IA y la guarda en out_path.

    Requiere OPENAI_API_KEY o GEMINI_API_KEY en el entorno del servidor.
    provider: auto | openai | gemini.
    size: 1024x1024, 1024x1536 o 1536x1024 (OpenAI); Gemini usa su formato.
    """
    if not prompt.strip():
        return "ERROR: prompt vacío"
    out = Path(out_path).expanduser()
    prov = provider.lower().strip()
    if prov == "auto":
        if os.getenv("OPENAI_API_KEY"):
            prov = "openai"
        elif os.getenv("GEMINI_API_KEY"):
            prov = "gemini"
        else:
            return (
                "ERROR: no hay clave de imagen. Definí OPENAI_API_KEY o "
                "GEMINI_API_KEY en el entorno de OpenCode. Mientras tanto, "
                "generate_icon funciona sin internet."
            )

    if prov == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            return "ERROR: falta OPENAI_API_KEY"
        model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
        data = _post_json(
            "https://api.openai.com/v1/images/generations",
            {"model": model, "prompt": prompt, "size": size, "n": 1},
            {"Authorization": f"Bearer {key}"},
        )
        item = data["data"][0]
        if item.get("b64_json"):
            raw = base64.b64decode(item["b64_json"])
        elif item.get("url"):
            with urllib.request.urlopen(item["url"], timeout=180) as r:
                raw = r.read()
        else:
            raise ValueError("OpenAI no devolvió imagen")
        _save(raw, out)
        return f"OK {out.resolve()} (openai/{model})"

    if prov == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            return "ERROR: falta GEMINI_API_KEY"
        model = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image-preview")
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{model}:generateContent?key={key}")
        data = _post_json(url, {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"]},
        }, {})
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        inline = next((p.get("inlineData") for p in parts if p.get("inlineData")), None)
        if not inline:
            raise ValueError("Gemini no devolvió imagen; revisá el modelo y la clave")
        _save(base64.b64decode(inline["data"]), out)
        return f"OK {out.resolve()} (gemini/{model})"

    return "ERROR: provider debe ser auto, openai o gemini"


@mcp.tool()
def list_providers() -> str:
    """Indica qué proveedores de imagen tienen clave configurada."""
    return json.dumps({
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "icons_offline": True,
        "styles": STYLES,
    }, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
