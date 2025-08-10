# CrisisSim MCP Server

## 🚨 AI-Driven Crisis Scenario Simulator

CrisisSim is a Model Context Protocol (MCP) server that simulates real-world crisis situations and allows users to make decisions to see updated outcomes. Perfect for emergency response training, hackathon projects, and AI integration.

## ✨ Features

- 🎯 **Realistic Crisis Scenarios**: Generate detailed crisis situations with roles and actions
- 🔄 **Interactive Decision Making**: Make decisions and see realistic consequences
- 🤖 **AI-Powered**: Uses OpenAI GPT-4o-mini for dynamic scenario generation
- 🛡️ **Fallback System**: Works even without API access using template generation
- 📊 **Session Management**: Track scenarios and decisions across sessions
- 🔧 **MCP Protocol**: Full Model Context Protocol compliance
- 🚀 **Production Ready**: Docker, cloud deployment, and monitoring support

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key (optional, for enhanced functionality)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/crisissim-mcp-server.git
cd crisissim-mcp-server

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key (optional)
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Run the Server
```bash
# Production version (recommended)
python server_production.py

# Hybrid version (tries API first, falls back to template)
python server_hybrid.py

# Fallback version (no API needed)
python server_fallback.py
```

### Test the Server
```bash
# Test all functionality
python test_hybrid.py

# Interactive demo
python hybrid_demo.py
```

## 🎯 Usage

### Generate a Crisis Scenario
```json
{
  "crisis_type": "natural disaster",
  "location": "Mumbai",
  "people_count": 5000
}
```

### Make a Decision
```json
{
  "session_id": "uuid-from-previous-call",
  "decision": "Evacuate all buildings in the affected area"
}
```

## 🐳 Docker Deployment

### Quick Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f crisissim
```

### Manual Docker Build
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

## ☁️ Cloud Deployment

### Render (Recommended)
1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Create new Web Service
4. Connect your repository
5. Set environment variables
6. Deploy!

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway variables set OPENAI_API_KEY="your-api-key-here"
railway up
```

### Other Platforms
- **Heroku**: `git push heroku main`
- **DigitalOcean App Platform**: Connect GitHub repo
- **AWS/GCP**: Use Docker deployment

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (optional)
- `LOG_LEVEL`: Set to `DEBUG`, `INFO`, `WARNING`, or `ERROR` (default: `INFO`)
- `PORT`: Port to run the server on (default: 8000)

### MCP Integration
```json
{
  "mcpServers": {
    "crisissim": {
      "command": "python",
      "args": ["server_production.py"],
      "cwd": "/path/to/crisissim"
    }
  }
}
```

## 📁 Project Structure

```
crisissim-mcp-server/
├── server_production.py      # Production server (recommended)
├── server_hybrid.py          # Hybrid server (API + fallback)
├── server_fallback.py        # Fallback server (no API needed)
├── server.py                 # Full API server
├── manifest.json             # MCP manifest
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── render.yaml              # Render deployment config
├── deploy.sh                # Linux/Mac deployment script
├── deploy.bat               # Windows deployment script
├── test_hybrid.py           # Test script
├── hybrid_demo.py           # Interactive demo
├── README.md                # This file
├── DEPLOYMENT_GUIDE.md      # Detailed deployment guide
├── FINAL_SETUP.md           # Setup guide
└── .gitignore               # Git ignore rules
```

## 🧪 Testing

### Automated Tests
```bash
# Test hybrid functionality
python test_hybrid.py

# Test fallback functionality
python test_fallback.py

# Test OpenAI integration
python test_openai.py
```

### Manual Testing
```bash
# Interactive demo
python hybrid_demo.py

# Simple demo
python simple_demo.py
```

## 📊 Monitoring

### Local Monitoring
```bash
# View logs
tail -f crisissim.log

# Check server status
curl http://localhost:8000/health
```

### Cloud Monitoring
- **Render**: Built-in logging and monitoring
- **Railway**: Real-time logs in dashboard
- **Heroku**: `heroku logs --tail`

## 🔒 Security

- ✅ API keys stored in environment variables
- ✅ Non-root user in Docker containers
- ✅ Input validation and sanitization
- ✅ Automatic session cleanup
- ✅ Error handling and logging

## 🚨 Troubleshooting

### Common Issues

#### API Key Problems
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set API key
export OPENAI_API_KEY="your-key-here"
```

#### Dependencies Issues
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Port Conflicts
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Getting Help
- Check logs: `tail -f crisissim.log`
- Test locally: `python server_production.py`
- Verify environment: `python -c "import mcp, openai; print('OK')"`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

- Built with the Model Context Protocol (MCP)
- Powered by OpenAI GPT-4o-mini
- Designed for emergency response training

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the guides in this repository
- **Deployment**: See `DEPLOYMENT_GUIDE.md`

## 🎊 Success Story

**"Aapka CrisisSim MCP server ab production-ready hai!"** 🚀

Your CrisisSim server is now:
- ✅ **Fully functional** with OpenAI API integration
- ✅ **Always working** with fallback system
- ✅ **Production ready** with Docker and cloud deployment
- ✅ **MCP compliant** for AI integration
- ✅ **Hackathon ready** for demos and presentations

---

**Made with ❤️ for emergency response training and AI innovation**
