# Chequeo del entorno de agent-lab
# Uso: powershell -ExecutionPolicy Bypass -File tools/doctor.ps1

$ErrorActionPreference = 'SilentlyContinue'

function Test-Tool {
    param(
        [string]$Name,
        [string]$Command,
        [string]$Hint
    )
    $output = Invoke-Expression $Command 2>$null
    if ($LASTEXITCODE -eq 0 -and $output) {
        $first = ($output | Select-Object -First 1).ToString().Trim()
        Write-Host ("[ok]   {0,-12} {1}" -f $Name, $first) -ForegroundColor Green
    } else {
        Write-Host ("[--]   {0,-12} falta" -f $Name) -ForegroundColor Yellow
        if ($Hint) { Write-Host ("       -> {0}" -f $Hint) -ForegroundColor DarkGray }
    }
}

Write-Host "agent-lab :: doctor" -ForegroundColor Cyan
Write-Host ("repo: {0}" -f (Split-Path -Parent $PSScriptRoot))
Write-Host ""

Test-Tool "python"  "python --version" "winget install Python.Python.3.13"
Test-Tool "yt-dlp"  "python -m yt_dlp --version" "python -m pip install --user yt-dlp"
Test-Tool "ffmpeg"  "ffmpeg -version" "winget install Gyan.FFmpeg (necesario para audio/whisper)"
Test-Tool "node"    "node --version" "winget install OpenJS.NodeJS.LTS"
Test-Tool "git"     "git --version" "winget install Git.Git"
Test-Tool "gh"      "gh --version" "winget install GitHub.cli"
Test-Tool "ollama"  "ollama --version" "winget install Ollama.Ollama"

Write-Host ""
$skill = Join-Path $env:USERPROFILE ".config\opencode\skills\agent-reach\SKILL.md"
if (Test-Path $skill) {
    Write-Host "[ok]   skill agent-reach instalada" -ForegroundColor Green
} else {
    Write-Host "[--]   skill agent-reach no encontrada" -ForegroundColor Yellow
    Write-Host "       -> ver README.md, seccion Skills" -ForegroundColor DarkGray
}

$whisper = Get-Command whisper -ErrorAction SilentlyContinue
if (-not $whisper) {
    Write-Host "[--]   whisper (opcional) no instalado" -ForegroundColor Yellow
    Write-Host "       -> python -m pip install --user openai-whisper (para videos sin subtitulos)" -ForegroundColor DarkGray
}
