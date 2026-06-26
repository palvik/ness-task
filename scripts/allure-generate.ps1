# Generates a self-contained HTML Allure report in reports/html.
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

$Results = Join-Path $Root "reports\allure-results"
$Output = Join-Path $Root "reports\html"

if (-not (Test-Path $Results)) {
    Write-Error "No Allure results at $Results. Run 'pytest' first."
}

$AllureBat = Join-Path $Root "tools\allure\bin\allure.bat"
if (-not (Test-Path $AllureBat)) {
    & (Join-Path $PSScriptRoot "install-allure.ps1")
}

& $AllureBat generate $Results --clean --single-file -o $Output
Write-Host "Report written to $Output\index.html"
