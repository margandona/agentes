"""CLI de inspección; el nombre coincide con un módulo estándar de Python."""
import sys
from pathlib import Path

# Evita que este archivo oculte inspect de la biblioteca estándar.
HERE = str(Path(__file__).resolve().parent)
sys.path = [p for p in sys.path if str(Path(p or '.').resolve()) != HERE]
import importlib.util
spec = importlib.util.spec_from_file_location('media_sanitizer_core', Path(HERE) / 'core.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

if __name__ == '__main__':
    raise SystemExit(core.main('inspect'))
