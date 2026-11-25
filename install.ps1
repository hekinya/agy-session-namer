$ErrorActionPreference = 'Stop'

$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = Join-Path $env:USERPROFILE ".gemini\config\plugins\agy-session-namer"

New-Item -ItemType Directory -Path (Join-Path $TargetDir "scripts") -Force | Out-Null

Copy-Item -Path (Join-Path $SourceDir "plugin.json") -Destination $TargetDir -Force
Copy-Item -Path (Join-Path $SourceDir "hooks.json") -Destination $TargetDir -Force
Copy-Item -Path (Join-Path $SourceDir "README.md") -Destination $TargetDir -Force
Copy-Item -Path (Join-Path $SourceDir "scripts\session_start_namer.py") -Destination (Join-Path $TargetDir "scripts") -Force

Write-Host "Installed agy-session-namer to: $TargetDir" -ForegroundColor Green
Write-Host "Open a new Antigravity conversation to activate the SessionStart hook."
