# CrisisSim MCP Server - Render Deployment Script for Windows (PowerShell)

# Function to display colored output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Success($message) {
    Write-ColorOutput Green "✅ $message"
}

function Write-Info($message) {
    Write-ColorOutput Cyan "ℹ️ $message"
}

function Write-Warning($message) {
    Write-ColorOutput Yellow "⚠️ $message"
}

function Write-Error($message) {
    Write-ColorOutput Red "❌ $message"
}

# Display header
Write-Host ""
Write-Host "🚀 CrisisSim MCP Server - Render Deployment Script" -ForegroundColor Magenta
Write-Host "=================================================" -ForegroundColor Magenta
Write-Host ""

# Check if git is installed
Write-Info "Checking if Git is installed..."
try {
    $gitVersion = git --version
    Write-Success "Git is installed: $gitVersion"
}
catch {
    Write-Error "Git is not installed. Please install Git for Windows first."
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required files exist
Write-Info "Checking required files..."
$missingFiles = $false

$requiredFiles = @(
    "server_gemini.py",
    "requirements.txt",
    "render.yaml"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Error "$file is missing"
        $missingFiles = $true
    }
    else {
        Write-Success "$file exists"
    }
}

if ($missingFiles) {
    Write-Error "Some required files are missing. Please check the errors above."
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if .env.local exists, create if not
Write-Info "Checking for .env.local file..."
if (-not (Test-Path ".env.local")) {
    Write-Info "Creating .env.local file for local development..."
    @"
GEMINI_API_KEY=your-api-key-here
PORT=8000
LOG_LEVEL=INFO
HTTP_SERVER=true
"@ | Out-File -FilePath ".env.local" -Encoding utf8
    Write-Success "Created .env.local file. Please edit it with your actual API key."
    Write-Info "This file is in .gitignore and won't be pushed to GitHub."
    Write-Host ""
}
else {
    Write-Success ".env.local file already exists"
}

# Initialize git repository if not already done
if (-not (Test-Path ".git")) {
    Write-Info "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - CrisisSim MCP Server with Gemini API"
    Write-Success "Git repository initialized"
}
else {
    Write-Success "Git repository already initialized"
}

# Get GitHub username
Write-Host ""
Write-Info "Please enter your GitHub repository details:"
$githubUsername = Read-Host "Enter your GitHub username"

# Add remote and push to GitHub
Write-Host ""
Write-Info "Adding GitHub remote and pushing code..."

try {
    # Check if remote already exists
    $remotes = git remote
    if ($remotes -contains "origin") {
        Write-Warning "Remote 'origin' already exists. Updating it..."
        git remote set-url origin "https://github.com/$githubUsername/crisissim-mcp-server.git"
    }
    else {
        git remote add origin "https://github.com/$githubUsername/crisissim-mcp-server.git"
    }
    
    git branch -M main
    git push -u origin main
    Write-Success "Code pushed to GitHub successfully"
}
catch {
    Write-Warning "Failed to push to GitHub. Please check your credentials and try again."
    Write-Host "You can manually push using these commands:" -ForegroundColor Yellow
    Write-Host "git remote add origin https://github.com/$githubUsername/crisissim-mcp-server.git" -ForegroundColor Yellow
    Write-Host "git branch -M main" -ForegroundColor Yellow
    Write-Host "git push -u origin main" -ForegroundColor Yellow
}

# Display next steps
Write-Host ""
Write-Info "Next steps for Render deployment:"
Write-Host "1. Go to https://dashboard.render.com and sign in" -ForegroundColor Yellow
Write-Host "2. Click 'New +' and select 'Web Service'" -ForegroundColor Yellow
Write-Host "3. Connect your GitHub repository: $githubUsername/crisissim-mcp-server" -ForegroundColor Yellow
Write-Host "4. Configure the service:" -ForegroundColor Yellow
Write-Host "   - Name: crisissim-mcp-server" -ForegroundColor Yellow
Write-Host "   - Environment: Python 3" -ForegroundColor Yellow
Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor Yellow
Write-Host "   - Start Command: python server_gemini.py" -ForegroundColor Yellow
Write-Host "5. Add environment variables:" -ForegroundColor Yellow
Write-Host "   - GEMINI_API_KEY: your-gemini-api-key" -ForegroundColor Yellow
Write-Host "6. Click 'Create Web Service'" -ForegroundColor Yellow

Write-Host ""
Write-Success "Deployment preparation completed!"
Write-Info "For detailed instructions, see RENDER_WINDOWS_GUIDE.md"
Write-Host ""

Read-Host "Press Enter to exit"