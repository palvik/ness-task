# Opens an interactive Allure report from reports/allure-results.
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

$Results = Join-Path $Root "reports\allure-results"
if (-not (Test-Path $Results)) {
    Write-Error "No Allure results at $Results. Run 'pytest' first."
}

$AllureBat = Join-Path $Root "tools\allure\bin\allure.bat"
if (-not (Test-Path $AllureBat)) {
    & (Join-Path $PSScriptRoot "install-allure.ps1")
}

Write-Host "Serving Allure report from $Results (Ctrl+C to stop)..."
& $AllureBat serve $Results
