param([ValidateSet('OpenCode', 'Codex')][string]$Target = 'OpenCode')
$ErrorActionPreference = 'Stop'
try {
    $source = Split-Path -Parent $PSScriptRoot
    $repo = (Resolve-Path (Join-Path $source '../..')).Path
    $relative = if ($Target -eq 'OpenCode') { '.opencode/skills' } else { '.agents/skills' }
    $parent = Join-Path $repo $relative
    $destination = Join-Path $parent 'media-metadata-sanitizer'
    if (Test-Path -LiteralPath $destination) { throw "El destino ya existe: $destination" }
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    New-Item -ItemType Directory -Path $destination | Out-Null
    Get-ChildItem -LiteralPath $source -Recurse -File | Where-Object {
        $_.FullName -notmatch '[\\/]__pycache__[\\/]' -and $_.Extension -ne '.pyc'
    } | ForEach-Object {
        $relativeFile = $_.FullName.Substring($source.Length + 1)
        $targetFile = Join-Path $destination $relativeFile
        New-Item -ItemType Directory -Path (Split-Path -Parent $targetFile) -Force | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $targetFile
    }
    Write-Output "Skill instalada: $destination"
} catch {
    Write-Error "No se pudo instalar la skill: $_"
    exit 1
}
