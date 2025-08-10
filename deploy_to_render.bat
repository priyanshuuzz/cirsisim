@echo off
REM CrisisSim MCP Server - Render Deployment Script for Windows

echo 🚀 Starting CrisisSim MCP Server deployment to Render...
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git is not installed. Please install Git for Windows first.
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Check if required files exist
echo 📋 Checking required files...
set MISSING_FILES=0

if not exist "server_gemini.py" (
    echo ❌ server_gemini.py is missing
    set MISSING_FILES=1
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt is missing
    set MISSING_FILES=1
)

if not exist "render.yaml" (
    echo ❌ render.yaml is missing
    set MISSING_FILES=1
)

if %MISSING_FILES% NEQ 0 (
    echo.
    echo ❌ Some required files are missing. Please check the errors above.
    pause
    exit /b 1
)

echo ✅ All required files found
echo.

REM Check if .env.local exists, create if not
if not exist ".env.local" (
    echo 📝 Creating .env.local file for local development...
    echo GEMINI_API_KEY=your-api-key-here> .env.local
    echo PORT=8000>> .env.local
    echo LOG_LEVEL=INFO>> .env.local
    echo HTTP_SERVER=true>> .env.local
    echo ✅ Created .env.local file. Please edit it with your actual API key.
    echo ℹ️ This file is in .gitignore and won't be pushed to GitHub.
    echo.
)

REM Initialize git repository if not already done
if not exist ".git" (
    echo 📁 Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit - CrisisSim MCP Server with Gemini API"
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already initialized
)

echo.
echo 📝 Please enter your GitHub repository details:
set /p GITHUB_USERNAME=Enter your GitHub username: 

REM Add remote and push to GitHub
echo.
echo 🔄 Adding GitHub remote and pushing code...
git remote add origin https://github.com/%GITHUB_USERNAME%/crisissim-mcp-server.git
git branch -M main
git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️ Failed to push to GitHub. Please check your credentials and try again.
    echo You can manually push using these commands:
    echo git remote add origin https://github.com/%GITHUB_USERNAME%/crisissim-mcp-server.git
    echo git branch -M main
    echo git push -u origin main
) else (
    echo ✅ Code pushed to GitHub successfully
)

echo.
echo 🌐 Next steps for Render deployment:
echo 1. Go to https://dashboard.render.com and sign in
echo 2. Click "New +" and select "Web Service"
echo 3. Connect your GitHub repository: %GITHUB_USERNAME%/crisissim-mcp-server
echo 4. Configure the service:
    echo    - Name: crisissim-mcp-server
    echo    - Environment: Python 3
    echo    - Build Command: pip install -r requirements.txt
    echo    - Start Command: python server_gemini.py
echo 5. Add environment variables:
    echo    - GEMINI_API_KEY: your-gemini-api-key
echo 6. Click "Create Web Service"

echo.
echo ✅ Deployment preparation completed!
echo 📝 For detailed instructions, see RENDER_WINDOWS_GUIDE.md
echo.

pause