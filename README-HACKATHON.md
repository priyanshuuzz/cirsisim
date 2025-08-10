# 🚨 CrisisSim - Puch AI Hackathon Ready!

## ⚡ Quick Demo (5 minutes!)

### 🎯 What is CrisisSim?
AI-powered crisis management simulator for emergency response training.

### 🚀 Features
- **Real-time scenario generation** 
- **Multi-role decision making**
- **Consequence simulation**
- **Performance tracking**

### 📱 Quick Test
```bash
# Start server
node hackathon-demo.js

# Test scenario generation
curl -X POST http://localhost:3000/api/scenario -H "Content-Type: application/json" -d '{"type":"earthquake"}'

# Make decision  
curl -X POST http://localhost:3000/api/decision -H "Content-Type: application/json" -d '{"sessionId":"123","decision":"Deploy rescue teams","role":"Commander"}'
```

### 🎪 Demo Scenarios
1. **🌍 Earthquake** - Natural disaster response
2. **💻 Cyber Attack** - Digital infrastructure crisis  
3. **🦠 Pandemic** - Health emergency management

### 🏆 Hackathon Pitch
"CrisisSim transforms crisis management training through AI-powered realistic simulations, helping emergency responders make better decisions under pressure."

### ⚡ Ready in 30 seconds!
```bash
node hackathon-demo.js
# Visit: http://localhost:3000/demo
```

## 🎯 Puch AI Integration
```json
{
  "mcpServers": {
    "crisissim": {
      "command": "node", 
      "args": ["hackathon-demo.js"]
    }
  }
}
```

**Status: ✅ HACKATHON READY!**