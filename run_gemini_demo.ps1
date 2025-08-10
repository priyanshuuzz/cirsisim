# PowerShell script to run the CrisisSim Gemini Demo

Write-Host "Running CrisisSim Gemini Demo..." -ForegroundColor Green

# Change to the directory where this script is located
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $scriptPath

# Run the Python script with any passed arguments
python gemini_demo.py $args

Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")