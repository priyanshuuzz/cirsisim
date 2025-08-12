# 🌍 CrisisSim - AI-Powered Real-World Crisis Simulator

## 🏆 Puch AI Hackathon Project

**Problem:** Governments, schools, companies need emergency drills (fire, earthquake, cyberattack, flood), but real drills are costly, time-consuming, and impractical.

**Solution:** A real-time AI crisis simulation generator that creates personalized, environment-adaptive emergency scenarios with role-based instructions.

## 🚀 Live Demo

**Server URL:** `https://your-render-url.com` or `https://your-netlify-url.com`

### Quick Test:
```bash
curl -X POST https://your-server-url.com/generate-scenario \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Mumbai Office Building",
    "buildingType": "high-rise",
    "teamSize": 8,
    "crisisType": "earthquake"
  }'
```

## 🎯 Key Features

### 1. Environment-Adaptive Scenarios
- User provides location + building type + available resources
- AI generates hyper-realistic scenarios based on environment
- Real-time adaptation to user's specific situation

### 2. Multi-Person Role Assignment
- Each team member gets unique instructions (leader, medic, communicator, scout)
- Role-based decision making with consequences
- Scalable from 2 to 50+ people

### 3. Dynamic Crisis Evolution
- Scenarios evolve in real-time based on decisions
- Realistic consequences and complications
- Live instruction updates as situation changes

### 4. Multiple Crisis Types
- 🏢 **Earthquake** - Building collapse, aftershocks, debris
- 🔥 **Fire Emergency** - Smoke, blocked exits, evacuation
- 🌊 **Flash Flood** - Rising water, evacuation routes
- 💻 **Cyber Attack** - Ransomware, data breach response
- 🦠 **Pandemic** - Isolation protocols, health screening

## 📊 Analytics Dashboard

Real-time usage statistics for hackathon ranking:
- Total users who started simulations
- Active simulations running
- Completed scenarios
- Popular crisis types

**Analytics Endpoint:** `GET /analytics`

## 🔧 API Endpoints

### Generate New Scenario
```http
POST /generate-scenario
Content-Type: application/json

{
  "location": "Delhi School Building",
  "buildingType": "school",
  "teamSize": 12,
  "crisisType": "fire"
}
```

### Process Next Step
```http
POST /next-step
Content-Type: application/json

{
  "scenarioId": "uuid-here",
  "action": "Evacuate through east stairwell",
  "roleDecisions": {
    "leader": "Guide students to assembly point",
    "medic": "Check for injuries during evacuation"
  }
}
```

### Check Scenario Status
```http
GET /scenario/{scenarioId}
```

### Health Check
```http
GET /health
```

## 🏗️ Deployment

### Option 1: Render
1. Connect GitHub repo to Render
2. Set build command: `npm install`
3. Set start command: `npm start`
4. Deploy automatically

### Option 2: Netlify
1. Build command: `npm run build`
2. Publish directory: `public`
3. Functions directory: `netlify/functions`

### Environment Variables
```
PORT=3000
NODE_ENV=production
```

## 🎮 Usage Examples

### For Schools
```javascript
{
  "location": "Delhi Public School, 3-story building",
  "buildingType": "school",
  "teamSize": 15,
  "crisisType": "earthquake"
}
```

### For Offices
```javascript
{
  "location": "Gurgaon IT Park, Tower B",
  "buildingType": "high-rise",
  "teamSize": 25,
  "crisisType": "fire"
}
```

### For Hospitals
```javascript
{
  "location": "AIIMS Delhi, Emergency Wing",
  "buildingType": "hospital",
  "teamSize": 30,
  "crisisType": "pandemic"
}
```

## 🏆 Why Judges Will Love It

1. **Live Interactive Demo** - Real crisis simulation on stage
2. **Social Impact** - Improves disaster preparedness
3. **AI Innovation** - Beyond text generation, real situational intelligence
4. **Scalability** - Schools, corporates, military, government contracts
5. **Revenue Model** - SaaS + government contracts

## 📈 Market Opportunity

- **Schools:** 1.5M schools in India need regular drills
- **Corporates:** 40M+ employees need emergency training
- **Government:** Disaster management agencies
- **International:** Global emergency preparedness market

## 🔥 Competitive Advantage

- First AI-driven, fully personalized crisis simulator
- Real-time scenario evolution (not pre-scripted)
- Multi-crisis, multi-environment support
- Role-based team coordination
- Instant deployment and scaling

## 🚀 Getting Started

1. **Clone & Install:**
```bash
git clone <repo-url>
cd crisissim
npm install
npm start
```

2. **Test Locally:**
Visit `http://localhost:3000`

3. **Deploy:**
Push to GitHub → Connect to Render/Netlify → Auto-deploy

4. **Share:**
Share your deployment URL for maximum hackathon usage!

## 📞 Support

For hackathon support or questions:
- Demo: `/demo` endpoint
- Analytics: `/analytics` endpoint
- Health: `/health` endpoint

**Built for Puch AI Hackathon 2024** 🏆