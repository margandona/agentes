@echo off
cd /d "%~dp0"
if not exist "tmp\watermark\.venv\Scripts\pythonw.exe" (
  echo Falta el entorno Python de las skills de video. Revisar apps/video-studio/README.md
  pause
  exit /b 1
)
start "" "tmp\watermark\.venv\Scripts\pythonw.exe" "apps\video-studio\app.py"
