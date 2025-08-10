@echo off
REM CrisisSim MCP Server Deployment Script for Windows
REM This script helps deploy the server to various platforms

echo 🚨 CrisisSim MCP Server Deployment Script
echo ==========================================

REM Check if required files exist
echo [INFO] Checking required files...

set required_files=server_production.py requirements.txt manifest.json Dockerfile docker-compose.yml render.yaml .gitignore

for %%f in (%required_files%) do (
    if exist "%%f" (
        echo [SUCCESS] ✓ %%f exists
    ) else (
        echo [ERROR] ✗ %%f missing
        pause
        exit /b 1
    )
)

REM Test the server locally
echo [INFO] Testing server locally...

python -c "import mcp, openai" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] ⚠ Dependencies not installed, installing now...
    pip install -r requirements.txt
)

REM Test the production server
echo [INFO] Testing production server...
python -c "
import asyncio
import sys
import os
sys.path.insert(0, '.')
from server_production import generate_scenario, next_step

async def test():
    try:
        result = await generate_scenario({
            'crisis_type': 'test',
            'location': 'test',
            'people_count': 100
        })
        print('✓ Server test successful')
        return True
    except Exception as e:
        print(f'✗ Server test failed: {e}')
        return False

asyncio.run(test())
"

if %errorlevel% equ 0 (
    echo [SUCCESS] ✓ Server test passed
) else (
    echo [ERROR] ✗ Server test failed
    pause
    exit /b 1
)

echo.
echo 🎯 Choose deployment option:
echo 1. Test server locally
echo 2. Deploy with Docker (if Docker is installed)
echo 3. Prepare for Render deployment
echo 4. Prepare for Railway deployment
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo [INFO] Testing server locally...
    python test_hybrid.py
) else if "%choice%"=="2" (
    echo [INFO] Deploying with Docker...
    docker build -t crisissim-mcp-server .
    if %errorlevel% equ 0 (
        echo [SUCCESS] ✓ Docker image built successfully
        docker-compose up -d
        if %errorlevel% equ 0 (
            echo [SUCCESS] ✓ Docker deployment successful
            echo 🌐 Server is running at: http://localhost:8000
            echo 📊 Web interface at: http://localhost:8080
        ) else (
            echo [ERROR] ✗ Docker deployment failed
        )
    ) else (
        echo [ERROR] ✗ Docker build failed
    )
) else if "%choice%"=="3" (
    echo [INFO] Preparing for Render deployment...
    if not exist ".git" (
        echo [INFO] Initializing git repository...
        git init
        git add .
        git commit -m "Initial commit - CrisisSim MCP Server"
    )
    echo [SUCCESS] ✓ Ready for Render deployment
    echo.
    echo 📋 Next steps for Render deployment:
    echo 1. Push your code to GitHub:
    echo    git remote add origin ^<your-github-repo-url^>
    echo    git push -u origin main
    echo.
    echo 2. Go to https://render.com and create a new Web Service
    echo 3. Connect your GitHub repository
    echo 4. Set environment variables:
    echo    - OPENAI_API_KEY: your-openai-api-key
    echo 5. Deploy!
) else if "%choice%"=="4" (
    echo [INFO] Preparing for Railway deployment...
    if not exist "railway.toml" (
        echo [INFO] Creating railway.toml...
        (
            echo [build]
            echo builder = "nixpacks"
            echo.
            echo [deploy]
            echo startCommand = "python server_production.py"
            echo healthcheckPath = "/"
            echo healthcheckTimeout = 300
            echo restartPolicyType = "on_failure"
            echo.
            echo [[services]]
            echo name = "crisissim-mcp-server"
        ) > railway.toml
        echo [SUCCESS] ✓ Created railway.toml
    )
    echo [SUCCESS] ✓ Ready for Railway deployment
    echo.
    echo 📋 Next steps for Railway deployment:
    echo 1. Install Railway CLI: npm install -g @railway/cli
    echo 2. Login: railway login
    echo 3. Initialize: railway init
    echo 4. Deploy: railway up
) else if "%choice%"=="5" (
    echo [INFO] Exiting...
    exit /b 0
) else (
    echo [ERROR] Invalid choice. Please enter 1-5.
    goto :eof
)

echo.
echo [SUCCESS] 🎉 Deployment script completed!
pause
