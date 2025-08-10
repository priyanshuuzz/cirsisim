#!/bin/bash

# CrisisSim MCP Server Deployment Script
# This script helps deploy the server to various platforms

set -e  # Exit on any error

echo "🚨 CrisisSim MCP Server Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required files exist
check_files() {
    print_status "Checking required files..."
    
    required_files=(
        "server_gemini.py"
        "requirements.txt"
        "manifest.json"
        "Dockerfile"
        "docker-compose.yml"
        "render.yaml"
        ".gitignore"
    )
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            print_success "✓ $file exists"
        else
            print_error "✗ $file missing"
            exit 1
        fi
    done
}

# Test the server locally
test_server() {
    print_status "Testing server locally..."
    
    if python -c "import mcp, openai" 2>/dev/null; then
        print_success "✓ Dependencies are installed"
    else
        print_warning "⚠ Dependencies not installed, installing now..."
        pip install -r requirements.txt
    fi
    
    # Test the Gemini server
    if timeout 10s python -c "
import asyncio
import sys
import os
sys.path.insert(0, '.')
from server_gemini import generate_scenario, next_step

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
"; then
        print_success "✓ Server test passed"
    else
        print_error "✗ Server test failed"
        exit 1
    fi
}

# Deploy to Docker
deploy_docker() {
    print_status "Deploying with Docker..."
    
    # Build the Docker image
    docker build -t crisissim-mcp-server .
    
    if [ $? -eq 0 ]; then
        print_success "✓ Docker image built successfully"
    else
        print_error "✗ Docker build failed"
        exit 1
    fi
    
    # Run with docker-compose
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        print_success "✓ Docker deployment successful"
        echo "🌐 Server is running at: http://localhost:8000"
        echo "📊 Web interface at: http://localhost:8080"
    else
        print_error "✗ Docker deployment failed"
        exit 1
    fi
}

# Deploy to Render
deploy_render() {
    print_status "Preparing for Render deployment..."
    
    # Check if git is initialized
    if [ ! -d ".git" ]; then
        print_status "Initializing git repository..."
        git init
        git add .
        git commit -m "Initial commit - CrisisSim MCP Server"
    fi
    
    print_success "✓ Ready for Render deployment"
    echo ""
    echo "📋 Next steps for Render deployment:"
    echo "1. Push your code to GitHub:"
    echo "   git remote add origin <your-github-repo-url>"
    echo "   git push -u origin main"
    echo ""
    echo "2. Go to https://render.com and create a new Web Service"
    echo "3. Connect your GitHub repository"
    echo "4. Set environment variables:"
    echo "   - GEMINI_API_KEY: your-gemini-api-key"
    echo "5. Deploy!"
}

# Deploy to Railway
deploy_railway() {
    print_status "Preparing for Railway deployment..."
    
    # Create railway.toml if it doesn't exist
    if [ ! -f "railway.toml" ]; then
        cat > railway.toml << EOF
[build]
builder = "nixpacks"

[deploy]
startCommand = "python server_gemini.py"
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "on_failure"

[[services]]
name = "crisissim-mcp-server"
EOF
        print_success "✓ Created railway.toml"
    fi
    
    print_success "✓ Ready for Railway deployment"
    echo ""
    echo "📋 Next steps for Railway deployment:"
    echo "1. Install Railway CLI: npm install -g @railway/cli"
    echo "2. Login: railway login"
    echo "3. Initialize: railway init"
    echo "4. Deploy: railway up"
}

# Main deployment menu
main_menu() {
    echo ""
    echo "🎯 Choose deployment option:"
    echo "1. Test server locally"
    echo "2. Deploy with Docker"
    echo "3. Prepare for Render deployment"
    echo "4. Prepare for Railway deployment"
    echo "5. All-in-one deployment (Docker)"
    echo "6. Exit"
    echo ""
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            check_files
            test_server
            ;;
        2)
            check_files
            test_server
            deploy_docker
            ;;
        3)
            check_files
            test_server
            deploy_render
            ;;
        4)
            check_files
            test_server
            deploy_railway
            ;;
        5)
            check_files
            test_server
            deploy_docker
            ;;
        6)
            print_status "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please enter 1-6."
            main_menu
            ;;
    esac
}

# Check if running in interactive mode
if [ "$1" = "--non-interactive" ]; then
    check_files
    test_server
    deploy_docker
else
    main_menu
fi

print_success "🎉 Deployment script completed!"
