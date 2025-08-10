# CrisisSim MCP Server - Deployment Guide

## 🚀 Complete Deployment Guide

Your CrisisSim MCP server is now ready for deployment! This guide covers all deployment options.

## 📋 Prerequisites

- ✅ Python 3.11+ installed
- ✅ Git installed
- ✅ Docker (optional, for containerized deployment)
- ✅ OpenAI API key (optional, for enhanced functionality)

## 🎯 Quick Start

### Option 1: Automated Deployment Script
```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

### Option 2: Manual Deployment
Follow the specific platform guides below.

## 🐳 Docker Deployment (Recommended)

### Local Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f crisissim
```

### Production Docker Deployment
```bash
# Build the image
docker build -t crisissim-mcp-server .

# Run with environment variables
docker run -d \
  --name crisissim-mcp \
  -e OPENAI_API_KEY="your-api-key-here" \
  -p 8000:8000 \
  crisissim-mcp-server
```

## ☁️ Cloud Deployment Options

### 1. Render Deployment

#### Step 1: Prepare Your Repository
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - CrisisSim MCP Server"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/crisissim-mcp-server.git
git push -u origin main
```

#### Step 2: Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `crisissim-mcp-server`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server_production.py`
5. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
6. Click "Create Web Service"

#### Step 3: Access Your Service
- Your service will be available at: `https://your-app-name.onrender.com`
- Render automatically provides HTTPS and custom domains

### 2. Railway Deployment

#### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

#### Step 2: Deploy
```bash
# Login to Railway
railway login

# Initialize project
railway init

# Set environment variables
railway variables set OPENAI_API_KEY="your-api-key-here"

# Deploy
railway up
```

#### Step 3: Access Your Service
- Railway provides a URL like: `https://your-app-name.railway.app`

### 3. Heroku Deployment

#### Step 1: Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-crisissim-app

# Set environment variables
heroku config:set OPENAI_API_KEY="your-api-key-here"

# Deploy
git push heroku main
```

### 4. DigitalOcean App Platform

#### Step 1: Prepare Repository
Ensure your repository is on GitHub with all files.

#### Step 2: Deploy on DigitalOcean
1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository
4. Configure:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `python server_production.py`
5. Add environment variables
6. Deploy

## 🔧 Environment Variables

### Required Variables
- `OPENAI_API_KEY`: Your OpenAI API key (optional, server works without it)

### Optional Variables
- `LOG_LEVEL`: Set to `DEBUG`, `INFO`, `WARNING`, or `ERROR` (default: `INFO`)
- `PORT`: Port to run the server on (default: 8000)

## 📊 Monitoring and Logs

### Local Monitoring
```bash
# View logs
tail -f crisissim.log

# Check server status
curl http://localhost:8000/health
```

### Cloud Platform Monitoring
- **Render**: Built-in logging and monitoring
- **Railway**: Real-time logs in dashboard
- **Heroku**: `heroku logs --tail`
- **DigitalOcean**: Built-in monitoring

## 🔒 Security Considerations

### API Key Security
- ✅ Never commit API keys to git
- ✅ Use environment variables
- ✅ Rotate keys regularly
- ✅ Use least privilege principle

### Server Security
- ✅ Production server uses non-root user
- ✅ Automatic session cleanup
- ✅ Input validation
- ✅ Error handling

## 🧪 Testing Your Deployment

### Test Script
```bash
# Test the deployed server
python test_hybrid.py
```

### Manual Testing
```bash
# Test scenario generation
curl -X POST http://your-deployed-url/generate \
  -H "Content-Type: application/json" \
  -d '{"crisis_type": "natural disaster", "location": "Mumbai", "people_count": 5000}'
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### 2. Dependencies Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 3. API Key Issues
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set API key
export OPENAI_API_KEY="your-key-here"
```

#### 4. Docker Issues
```bash
# Clean up Docker
docker system prune -a

# Rebuild image
docker build --no-cache -t crisissim-mcp-server .
```

### Getting Help
- Check logs: `tail -f crisissim.log`
- Test locally: `python server_production.py`
- Verify environment: `python -c "import mcp, openai; print('OK')"`

## 📈 Scaling Considerations

### For High Traffic
- Use Redis for session storage
- Implement rate limiting
- Add load balancing
- Use CDN for static assets

### Cost Optimization
- Use free tier platforms initially
- Monitor API usage
- Implement caching
- Use template fallback when possible

## 🎉 Success Indicators

When deployment is successful:
- ✅ Server starts without errors
- ✅ Logs show "Starting CrisisSim MCP Server"
- ✅ API endpoints respond correctly
- ✅ Health checks pass
- ✅ No memory leaks (sessions clean up automatically)

## 📞 Support

If you encounter issues:
1. Check the logs first
2. Verify all files are present
3. Test locally before deploying
4. Ensure environment variables are set correctly

## 🎊 Congratulations!

Your CrisisSim MCP server is now deployment-ready with:
- ✅ Multiple deployment options
- ✅ Production-grade security
- ✅ Automatic error handling
- ✅ Comprehensive logging
- ✅ Easy scaling capabilities

**Aapka CrisisSim MCP server ab production-ready hai!** 🚀
