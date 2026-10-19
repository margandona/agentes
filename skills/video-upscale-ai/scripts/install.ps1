param(
    [ValidateSet('Both','Codex','OpenCode')][string]$Target = 'Both',
    [string]$Python = '',
    [switch]$DownloadEngine
)
$ErrorActionPreference = 'Stop'
try {
    $source = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
    $repo = (Resolve-Path (Join-Path $source '../..')).Path
    if (-not (Test-Path -LiteralPath (Join-Path $repo 'AGENTS.md'))) {
        throw 'Ejecutar el instalador desde la fuente skills/video-upscale-ai de este proyecto.'
    }
    $runtime = Join-Path $repo 'tmp/upscale-ai'
    $runtimePython = Join-Path $runtime '.venv/Scripts/python.exe'
    $env:UV_CACHE_DIR = Join-Path $repo 'tmp/uv-cache'
    $env:UV_PYTHON_INSTALL_DIR = Join-Path $repo 'tmp/python'
    $uv = Get-Command uv -ErrorAction SilentlyContinue
    if (-not (Test-Path -LiteralPath $runtimePython)) {
        New-Item -ItemType Directory -Path $runtime -Force | Out-Null
        if ($Python) {
            & $Python -m venv (Join-Path $runtime '.venv')
        } elseif ($uv) {
            & $uv.Source python install 3.11
            if ($LASTEXITCODE -ne 0) { throw 'No se pudo preparar Python 3.11.' }
            & $uv.Source venv --python 3.11 (Join-Path $runtime '.venv')
        } else {
            throw 'Falta Python: instalar Python >=3.11 y pasar -Python RUTA_PYTHON, o instalar uv.'
        }
        if ($LASTEXITCODE -ne 0) { throw 'Falló la creación del entorno Python.' }
    }
    & $runtimePython -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)'
    if ($LASTEXITCODE -ne 0) { throw 'El entorno requiere Python 3.11 o superior.' }
    & $runtimePython -c 'from PIL import Image'
    if ($LASTEXITCODE -ne 0) {
        if ($uv) { & $uv.Source pip install --python $runtimePython 'Pillow>=10' }
        else { & $runtimePython -m pip install 'Pillow>=10' }
        if ($LASTEXITCODE -ne 0) { throw 'No se pudo instalar Pillow.' }
    }
    $bootstrapArgs = @((Join-Path $PSScriptRoot 'bootstrap.py'))
    if ($DownloadEngine) { $bootstrapArgs += '--download' }
    & $runtimePython @bootstrapArgs
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo preparar el motor Real-ESRGAN.' }
    & $runtimePython (Join-Path $PSScriptRoot 'upscale.py') doctor --test-engine
    if ($LASTEXITCODE -ne 0) { throw 'Falló la comprobación de herramientas o del motor.' }
    $parents = @()
    if ($Target -in @('Both','Codex')) { $parents += '.agents/skills' }
    if ($Target -in @('Both','OpenCode')) { $parents += '.opencode/skills' }
    $files = @(Get-ChildItem -LiteralPath $source -Recurse -File | Where-Object {
        $_.FullName -notmatch '[\\/]__pycache__[\\/]' -and $_.Extension -ne '.pyc'
    })
    foreach ($parent in $parents) {
        $destination = [IO.Path]::GetFullPath((Join-Path (Join-Path $repo $parent) 'video-upscale-ai'))
        if (-not $destination.StartsWith($repo + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
            throw 'La ruta de instalación sale del proyecto.'
        }
        if (Test-Path -LiteralPath $destination) {
            foreach ($file in $files) {
                $relative = $file.FullName.Substring($source.Length + 1)
                $existing = Join-Path $destination $relative
                if (-not (Test-Path -LiteralPath $existing) -or (Get-FileHash -LiteralPath $file.FullName).Hash -ne (Get-FileHash -LiteralPath $existing).Hash) {
                    throw "La instalación existente difiere: $existing. No se sobrescribe."
                }
            }
            Write-Output "Ya instalada e idéntica: $destination"
            continue
        }
        foreach ($file in $files) {
            $relative = $file.FullName.Substring($source.Length + 1)
            $destFile = Join-Path $destination $relative
            New-Item -ItemType Directory -Path (Split-Path -Parent $destFile) -Force | Out-Null
            Copy-Item -LiteralPath $file.FullName -Destination $destFile
        }
        Write-Output "Instalada: $destination"
    }
    Write-Output 'Invocación: $video-upscale-ai compará este clip para YouTube Shorts a 1080p.'
} catch {
    Write-Error "No se pudo instalar video-upscale-ai: $_"
    exit 1
}
