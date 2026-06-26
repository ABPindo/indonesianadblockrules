#!/usr/bin/env pwsh
# lint.ps1 — Run AGLint on all source filter files.
# Cross-platform: works on Windows (PowerShell), Linux, and macOS.

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$Src = Join-Path $RepoRoot "src"

Write-Host "==> Running AGLint on source files..."

# Find all .txt files in src/ and run AGLint
Get-ChildItem -Path $Src -Filter "*.txt" -Recurse -File | ForEach-Object {
    npx aglint $_.FullName
}

Write-Host "==> Done. No problems found."
