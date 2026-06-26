# Downloads Allure CLI into tools/allure (project-local; not committed).
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

$ToolsDir = Join-Path $Root "tools\allure"
$AllureBat = Join-Path $ToolsDir "bin\allure.bat"

if (Test-Path $AllureBat) {
    Write-Host "Allure CLI already installed at $ToolsDir"
    & $AllureBat --version
    exit 0
}

$Version = "2.32.2"
$Zip = Join-Path $env:TEMP "allure-$Version.zip"
$Url = "https://github.com/allure-framework/allure2/releases/download/$Version/allure-$Version.zip"

Write-Host "Downloading Allure $Version..."
New-Item -ItemType Directory -Force -Path $ToolsDir | Out-Null
Invoke-WebRequest -Uri $Url -OutFile $Zip
Expand-Archive -Path $Zip -DestinationPath $ToolsDir -Force
Move-Item -Path (Join-Path $ToolsDir "allure-$Version\*") -Destination $ToolsDir -Force
Remove-Item (Join-Path $ToolsDir "allure-$Version") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $Zip -Force -ErrorAction SilentlyContinue

& $AllureBat --version
