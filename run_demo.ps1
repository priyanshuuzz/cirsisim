# CrisisSim Demo PowerShell Script
Write-Host "Running CrisisSim Demo..." -ForegroundColor Green

# Get the directory of this script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to the script directory
Set-Location -Path $scriptPath

# Run the Python script
python demo_script.py

Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")