"""Procesamiento local de metadatos. Python 3.11+, sin dependencias Python."""
from __future__ import annotations

import sys
from pathlib import Path

# inspect.py es una CLI requerida, no el módulo estándar inspect.
_scripts = Path(__file__).resolve().parent
sys.path = [p for p in sys.path if Path(p or '.').resolve() != _scripts]

import argparse
import hashlib
import json
import logging
import os
import re
import shutil
import struct
import subprocess
import tempfile


class MediaError(Exception):
    pass


FORMATS = {"MP4": {".mp4"}, "MOV": {".mov"}, "MKV": {".mkv"},
           "WEBM": {".webm"}, "JPEG": {".jpg", ".jpeg"},
           "PNG": {".png"}, "WEBP": {".webp"}}
IMAGES = {"JPEG", "PNG", "WEBP"}
CATEGORIES = {"personal", "location", "software", "dates"}
FIELDS = {
    "personal": {"artist", "author", "creator", "ownername", "cameraownername", "serialnumber", "bodyserialnumber", "lensserialnumber", "email", "byline"},
    "location": {"location", "locationiso6709", "gpscoordinates", "gpslatitude", "gpslongitude", "gpsaltitude", "gpsposition", "gpslatituderef", "gpslongituderef", "gpsaltituderef", "city", "country", "state", "sublocation"},
    "software": {"software", "encoder", "encodingtool", "writingapp", "muxingapp", "creatortool", "producer"},
    "dates": {"creationtime", "createdate", "modifydate", "datetimeoriginal", "datetime", "date", "datecreated", "mediacreatedate", "mediamodifydate", "trackcreatedate", "trackmodifydate"},
}


def normalized(key):
    return re.sub(r"[^a-z0-9]", "", key.lower())


def category(key):
    group, _, tag = key.rpartition(":")
    n = normalized(tag or key)
    if any(t in normalized(key) for t in ("c2pa", "jumbf", "manifest", "contentcredential", "ingredients", "digitalsignature", "assertion")) or n in {"copyright", "rights", "usageterms", "attribution"}:
        return "provenance"
    if group in {"File", "System", "ExifTool", "Composite"}:
        return "structural"
    for kind, names in FIELDS.items():
        if n in names or (kind == "location" and n.startswith("gps")):
            return kind
    return "other"


def run(args):
    exe = shutil.which(args[0])
    if not exe:
        raise MediaError(f"Falta {args[0]} en PATH. Consultá references/metadata-fields.md para instalarlo.")
    logging.debug("Ejecutando %r", args)
    try:
        result = subprocess.run([exe, *map(str, args[1:])], capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=300,
                                stdin=subprocess.DEVNULL, shell=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MediaError(f"No se pudo ejecutar {args[0]}: {exc}") from exc
    if result.returncode:
        raise MediaError(f"{args[0]} falló: {result.stderr.strip()[-3000:]}")
    return result.stdout


def source_path(value):
    path = Path(value).resolve(strict=True)
    if not path.is_file():
        raise MediaError(f"No es un archivo: {path}")
    return path


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def provenance_ranges(path):
    """En BMFF válido, escanear cajas de metadatos, no muestras comprimidas mdat."""
    total=path.stat().st_size
    fallback=[(0,total)]
    ranges=[]
    with path.open('rb') as handle:
        head=handle.read(8)
        if len(head)!=8 or head[4:]!=b'ftyp':
            return fallback
        offset=0
        while offset<total:
            handle.seek(offset)
            header=handle.read(8)
            if len(header)!=8:
                return fallback
            size,kind=struct.unpack('>I4s',header)
            minimum=8
            if size==1:
                extended=handle.read(8)
                if len(extended)!=8:
                    return fallback
                size=struct.unpack('>Q',extended)[0]
                minimum=16
            elif size==0:
                size=total-offset
            if size<minimum or offset+size>total:
                return fallback
            if kind!=b'mdat':
                ranges.append((offset,size))
            offset+=size
    return ranges


def provenance_markers(path):
    # Escaneo incremental complementario: deliberadamente conservador, no valida firmas.
    markers = set()
    with path.open("rb") as handle:
        for offset,length in provenance_ranges(path):
            handle.seek(offset)
            remaining=length
            tail=b''
            while remaining:
                chunk=handle.read(min(remaining,1024*1024))
                if not chunk:
                    raise MediaError('El archivo cambió durante el escaneo de procedencia')
                remaining-=len(chunk)
                raw=tail+chunk
                if bytes.fromhex('d8fec3d61b0e483c92975828877ec481') in raw:
                    markers.add('c2pa_uuid')
                block=raw.lower()
                for token in (b"c2pa", b"jumb", b"contentcredentials", b"content credentials", b"dcterms:provenance", b"digitalsignature"):
                    if token in block:
                        markers.add(token.decode())
                tail=raw[-64:]
    return sorted(markers)


def inspect_media(value):
    path = source_path(value)
    exif = json.loads(run(["exiftool", "-j", "-G1", "-s", "-a", path]))[0]
    fmt = str(exif.get("File:FileType", "")).upper()
    if fmt == "EXTENDED WEBP":
        fmt = "WEBP"
    if fmt not in FORMATS:
        raise MediaError(f"Formato real incompatible: {fmt or 'desconocido'}")
    if exif.get("ExifTool:Error"):
        raise MediaError(f"Archivo dañado: {exif['ExifTool:Error']}")
    probe = json.loads(run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-show_format", "-show_streams", "-show_chapters", "-of", "json", path]))
    if not probe.get("streams"):
        raise MediaError("Archivo sin flujos legibles")
    fields = {k: {"value": v, "category": category(k)} for k, v in exif.items() if k != "SourceFile"}
    for scope, obj in [("format", probe.get("format", {})), *[(f"stream:{i}", s) for i, s in enumerate(probe["streams"])], *[(f"chapter:{i}", c) for i, c in enumerate(probe.get("chapters", []))]]:
        for k, v in obj.get("tags", {}).items():
            fields[f"ffprobe:{scope}:{k}"] = {"value": v, "category": category(k)}
    markers = provenance_markers(path)
    protected = markers or [k for k, v in fields.items() if v["category"] == "provenance"]
    return {"schema_version": 1, "path": str(path), "format": fmt, "sha256": sha256(path),
            "metadata": fields, "probe": probe, "protected_indicators": protected,
            "warnings": ["La ausencia de campos no demuestra origen humano. La detección de credenciales no es exhaustiva."]}


def media_signature(report):
    return [{k: s.get(k) for k in ("codec_type", "codec_name", "width", "height", "sample_rate", "channels", "disposition")} for s in report["probe"]["streams"]]


def decoded_hashes(path):
    # Comprueba contenido audiovisual decodificado, independientemente del contenedor.
    return run(["ffmpeg", "-v", "error", "-xerror", "-nostdin", "-protocol_whitelist", "file,pipe", "-i", path,
                "-map", "0:v?", "-map", "0:a?", "-f", "streamhash", "-hash", "sha256", "-"]).splitlines()


def compare(before, after):
    a, b = before["metadata"], after["metadata"]
    removed = {k: v for k, v in a.items() if k not in b}
    changed = {k: {"before": a[k], "after": b[k]} for k in a.keys() & b.keys() if a[k] != b[k]}
    durations = [float(r["probe"].get("format", {}).get("duration", 0)) for r in (before, after)]
    checks = {"same_format": before["format"] == after["format"],
              "provenance_indicators": before["protected_indicators"] == after["protected_indicators"],
              "same_streams": media_signature(before) == media_signature(after),
              "duration": abs(durations[0] - durations[1]) <= 0.1,
              "decoded_content": decoded_hashes(before["path"]) == decoded_hashes(after["path"])}
    return {"schema_version": 1, "ok": all(checks.values()), "checks": checks,
            "sha256_before": before["sha256"], "sha256_after": after["sha256"],
            "removed": removed, "changed": changed, "remaining": b,
            "warnings": before["warnings"]}


def sanitize(value, output, categories, dry_run=False):
    before = inspect_media(value)
    src, dst = Path(before["path"]), Path(output).absolute()
    if not categories or not set(categories) <= CATEGORIES:
        raise MediaError("Elegí categorías válidas: personal, location, software, dates")
    if dst.exists() or dst.is_symlink() or dst.resolve() == src:
        raise MediaError(f"La salida ya existe o coincide con el original: {dst}")
    if not dst.parent.is_dir():
        raise MediaError("El directorio de salida no existe")
    if dst.suffix.lower() not in FORMATS[before["format"]]:
        raise MediaError("La extensión de salida debe corresponder al formato real; no se convierte el contenedor")
    if before["protected_indicators"]:
        raise MediaError("Se detectó autoría/procedencia protegida. Editar o remuxear podría invalidar credenciales; no se modifica el archivo.")
    selected = {k: v for k, v in before["metadata"].items() if v["category"] in categories}
    if dry_run:
        return {"schema_version": 1, "dry_run": True, "output": str(dst), "selected": selected, "warnings": before["warnings"]}
    with tempfile.TemporaryDirectory(prefix="metadata-", dir=dst.parent) as tmp:
        work = Path(tmp) / ("output" + dst.suffix)
        if before["format"] in IMAGES:
            shutil.copyfile(src, work)
            tags = [f"-{k}=" for k in selected if not k.startswith("ffprobe:")]
            if tags:
                run(["exiftool", "-overwrite_original", *tags, work])
        else:
            cmd = ["ffmpeg", "-v", "error", "-xerror", "-nostdin", "-n", "-copyts", "-protocol_whitelist", "file,pipe", "-i", src,
                   "-map", "0", "-map_metadata", "0", "-map_chapters", "0", "-c", "copy"]
            for k in selected:
                if k.startswith("ffprobe:"):
                    parts = k.split(":")
                    if parts[1] == "format":
                        cmd += ["-metadata", f"{parts[2]}="]
                    elif parts[1] == "stream":
                        cmd += [f"-metadata:s:{parts[2]}", f"{parts[3]}="]
                    elif parts[1] == "chapter":
                        cmd += [f"-metadata:c:{parts[2]}", f"{parts[3]}="]
            if "software" in categories:
                cmd += ["-fflags", "+bitexact", "-metadata", "encoder="]
            run([*cmd, work])
        after = inspect_media(work)
        result = compare(before, after)
        preserved = {k: v for k, v in before["metadata"].items()
                     if v["category"] in CATEGORIES - set(categories) | {"provenance"}}
        result["checks"]["unselected_metadata"] = all(after["metadata"].get(k) == v for k, v in preserved.items())
        result["ok"] = all(result["checks"].values())
        # No se publica si el contenedor conserva campos seleccionados no vacíos.
        residual = {k: v for k, v in after["metadata"].items() if v["category"] in categories and v["value"] not in ("", None, "0000:00:00 00:00:00")}
        result["residual_selected"] = residual
        if not result["ok"] or residual:
            raise MediaError("Verificación fallida; salida descartada: " + json.dumps({"checks": result["checks"], "residual_selected": residual}, ensure_ascii=False))
        if sha256(src) != before["sha256"]:
            raise MediaError("El original cambió durante el procesamiento; salida descartada")
        # O_EXCL evita incluso carreras con otro proceso creando el destino.
        created = False
        try:
            with dst.open("xb") as target, work.open("rb") as data:
                created = True
                shutil.copyfileobj(data, target)
        except Exception:
            if created:
                dst.unlink(missing_ok=True)
            raise
        result["output"] = str(dst)
        return result


def batch(directory, output, categories, dry_run=False):
    src, dst = Path(directory).resolve(strict=True), Path(output).resolve()
    if not src.is_dir() or dst == src or src in dst.parents or dst in src.parents:
        raise MediaError("Entrada y salida deben ser directorios separados, sin anidamiento")
    files = sorted(p for p in src.rglob("*") if p.is_file())
    results = []
    for path in files:
        target = dst / path.relative_to(src)
        try:
            if path.is_symlink():
                raise MediaError("Se omite enlace simbólico")
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
            # En dry-run no se exige que exista el directorio futuro.
            if dry_run and not target.parent.exists():
                report = inspect_media(path)
                if report["protected_indicators"]:
                    raise MediaError("Procedencia protegida detectada")
                result = {"dry_run": True, "output": str(target)}
            else:
                result = sanitize(path, target, categories, dry_run)
            results.append({"input": str(path), "ok": True, "result": result})
        except (MediaError, OSError, ValueError) as exc:
            results.append({"input": str(path), "ok": False, "error": str(exc)})
    return {"schema_version": 1, "ok": all(r["ok"] for r in results), "total": len(results),
            "succeeded": sum(r["ok"] for r in results), "results": results}


def main(operation):
    parser = argparse.ArgumentParser(description=f"{operation}: metadatos multimedia locales autorizados")
    parser.add_argument("input", help="Archivo original o directorio para batch")
    parser.add_argument("--verbose", action="store_true", help="Diagnósticos en stderr")
    if operation == "verify":
        parser.add_argument("output", help="Archivo procesado")
    if operation in {"sanitize", "batch"}:
        parser.add_argument("--output", required=True, help="Salida nueva; nunca sobrescribe")
        parser.add_argument("--categories", nargs="+", choices=sorted(CATEGORIES), default=sorted(CATEGORIES), help="Categorías a eliminar (predeterminado: todas las ordinarias)")
        parser.add_argument("--dry-run", action="store_true", help="Inspeccionar sin escribir")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)
    try:
        if sys.version_info < (3, 11):
            raise MediaError("Se requiere Python 3.11 o superior")
        if operation == "inspect":
            result = inspect_media(args.input)
        elif operation == "verify":
            result = compare(inspect_media(args.input), inspect_media(args.output))
        elif operation == "batch":
            result = batch(args.input, args.output, args.categories, args.dry_run)
        else:
            result = sanitize(args.input, args.output, args.categories, args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok", True) else 1
    except (MediaError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"schema_version": 1, "ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
