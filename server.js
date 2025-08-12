import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const cors = require('cors');

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// In-memory storage for sessions
const sessions = new Map();
const analytics = {
  totalUsers: 0,
  activeSimulations: 0,
  completedScenarios: 0,
  popularCrises: {}
};

// Crisis scenario templates with realistic details
const crisisTemplates = {
  earthquake: {
    name: "Earthquake Emergency",
    severity: "High",
    timeLimit: "15 minutes",
    description: "Magnitude 7.2 earthquake hits your area. Buildings shaking, power out, people trapped.",
    initialActions: [
      "DROP, COVER, and HOLD ON immediately",
      "Stay away from windows and heavy objects",
      "If outdoors, move away from buildings",
      "Check for injuries - yourself first, then others"
    ],
    roles: {
      leader: "Coordinate evacuation and headcount",
      medic: "Assess injuries and provide first aid",
      communicator: "Contact emergency services and families",
      scout: "Find safe evacuation routes"
    }
  },
  fire: {
    name: "Building Fire Emergency",
    severity: "Critical",
    timeLimit: "8 minutes",
    description: "Fire detected on 3rd floor. Smoke spreading rapidly. Multiple exits blocked.",
    initialActions: [
      "Activate fire alarm immediately",
      "Stay low to avoid smoke inhalation",
      "Feel doors before opening - if hot, find alternate route",
      "Never use elevators during fire"
    ],
    roles: {
      leader: "Guide evacuation to assembly point",
      medic: "Help people with mobility issues",
      communicator: "Call fire department and building security",
      scout: "Check all rooms and find clear exits"
    }
  },
  cyberattack: {
    name: "Cyber Security Breach",
    severity: "High",
    timeLimit: "30 minutes",
    description: "Ransomware detected. All systems compromised. Data being encrypted.",
    initialActions: [
      "Disconnect from internet immediately",
      "Do not pay ransom or click any links",
      "Document what happened before shutdown",
      "Switch to backup communication methods"
    ],
    roles: {
      leader: "Coordinate response team and decisions",
      tech: "Isolate infected systems and assess damage",
      communicator: "Contact IT security and stakeholders",
      documenter: "Record incident details for investigation"
    }
  },
  flood: {
    name: "Flash Flood Warning",
    severity: "High",
    timeLimit: "20 minutes",
    description: "Heavy rainfall causing rapid flooding. Water level rising 2 feet per hour.",
    initialActions: [
      "Move to higher ground immediately",
      "Avoid walking/driving through flood water",
      "Turn off electricity and gas if safe to do so",
      "Gather emergency supplies and important documents"
    ],
    roles: {
      leader: "Organize evacuation to higher floors/areas",
      medic: "Help elderly and children first",
      communicator: "Monitor weather alerts and call for help",
      logistics: "Secure food, water, and emergency supplies"
    }
  },
  pandemic: {
    name: "Pandemic Outbreak Response",
    severity: "Medium",
    timeLimit: "45 minutes",
    description: "New virus strain detected. Rapid human-to-human transmission confirmed.",
    initialActions: [
      "Implement immediate isolation protocols",
      "Wear masks and maintain 6-foot distance",
      "Sanitize all surfaces and wash hands frequently",
      "Monitor symptoms and temperature regularly"
    ],
    roles: {
      leader: "Implement safety protocols and communication",
      medic: "Screen for symptoms and provide care guidance",
      communicator: "Update families and coordinate with health authorities",
      logistics: "Manage supplies and ensure proper sanitation"
    }
  }
};

// Generate dynamic scenario based on user input
function generateScenario(userInput) {
  const { location, buildingType, teamSize, crisisType } = userInput;
  const template = crisisTemplates[crisisType] || crisisTemplates.earthquake;
  
  // Customize scenario based on user environment
  const customizedScenario = {
    id: uuidv4(),
    ...template,
    location: location || "Your current location",
    buildingType: buildingType || "office building",
    teamSize: teamSize || 5,
    startTime: new Date().toISOString(),
    status: "active",
    currentStep: 1,
    totalSteps: 5,
    environmentFactors: generateEnvironmentFactors(location, buildingType),
    personalizedInstructions: generatePersonalizedInstructions(template, teamSize),
    progressLog: []
  };

  return customizedScenario;
}

function generateEnvironmentFactors(location, buildingType) {
  const factors = [];
  
  if (buildingType === "high-rise") {
    factors.push("Multiple floors - elevator access restricted");
    factors.push("Stairwells may be crowded");
  } else if (buildingType === "school") {
    factors.push("Large number of children present");
    factors.push("Multiple classrooms to evacuate");
  } else if (buildingType === "hospital") {
    factors.push("Patients with limited mobility");
    factors.push("Critical medical equipment to consider");
  }
  
  if (location && location.toLowerCase().includes("coastal")) {
    factors.push("Tsunami risk - move inland");
  }
  
  return factors;
}

function generatePersonalizedInstructions(template, teamSize) {
  const instructions = {};
  const availableRoles = Object.keys(template.roles);
  
  for (let i = 1; i <= teamSize; i++) {
    const roleIndex = (i - 1) % availableRoles.length;
    const role = availableRoles[roleIndex];
    instructions[`person_${i}`] = {
      role: role,
      instruction: template.roles[role],
      priority: i <= availableRoles.length ? "primary" : "support"
    };
  }
  
  return instructions;
}

// API Routes

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    uptime: process.uptime(),
    analytics: analytics
  });
});

// Get analytics for hackathon judges
app.get('/analytics', (req, res) => {
  res.json({
    ...analytics,
    activeSessions: sessions.size,
    timestamp: new Date().toISOString()
  });
});

// Generate new crisis scenario
app.post('/generate-scenario', (req, res) => {
  try {
    const userInput = req.body;
    const scenario = generateScenario(userInput);
    
    sessions.set(scenario.id, scenario);
    analytics.totalUsers++;
    analytics.activeSimulations++;
    
    const crisisType = userInput.crisisType || 'earthquake';
    analytics.popularCrises[crisisType] = (analytics.popularCrises[crisisType] || 0) + 1;
    
    res.json({
      success: true,
      scenario: scenario,
      message: `Crisis simulation started! You have ${scenario.timeLimit} to respond.`
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Process next step in simulation
app.post('/next-step', (req, res) => {
  try {
    const { scenarioId, action, roleDecisions } = req.body;
    const scenario = sessions.get(scenarioId);
    
    if (!scenario) {
      return res.status(404).json({ success: false, error: 'Scenario not found' });
    }
    
    // Process the action and generate consequences
    const consequences = processAction(scenario, action, roleDecisions);
    scenario.currentStep++;
    scenario.progressLog.push({
      step: scenario.currentStep - 1,
      action: action,
      consequences: consequences,
      timestamp: new Date().toISOString()
    });
    
    // Check if simulation is complete
    if (scenario.currentStep > scenario.totalSteps) {
      scenario.status = 'completed';
      analytics.activeSimulations--;
      analytics.completedScenarios++;
    }
    
    sessions.set(scenarioId, scenario);
    
    res.json({
      success: true,
      scenario: scenario,
      consequences: consequences,
      isComplete: scenario.status === 'completed'
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get scenario status
app.get('/scenario/:id', (req, res) => {
  const scenario = sessions.get(req.params.id);
  if (!scenario) {
    return res.status(404).json({ success: false, error: 'Scenario not found' });
  }
  res.json({ success: true, scenario });
});

// Process action and generate realistic consequences
function processAction(scenario, action, roleDecisions) {
  const consequences = [];
  const crisisType = Object.keys(crisisTemplates).find(key => 
    crisisTemplates[key].name === scenario.name
  );
  
  // Generate consequences based on action quality
  if (action && action.toLowerCase().includes('panic')) {
    consequences.push("⚠️ Panic caused confusion - 2 people injured in rush");
    consequences.push("⏱️ Evacuation delayed by 3 minutes");
  } else if (action && action.toLowerCase().includes('calm')) {
    consequences.push("✅ Calm leadership prevented panic");
    consequences.push("⏱️ Evacuation proceeding smoothly");
  }
  
  // Add crisis-specific consequences
  if (crisisType === 'fire') {
    consequences.push("🔥 Fire spreading to adjacent rooms");
    consequences.push("💨 Smoke visibility reduced to 10 feet");
  } else if (crisisType === 'earthquake') {
    consequences.push("🏢 Aftershock detected - magnitude 4.1");
    consequences.push("🚪 Main exit partially blocked by debris");
  }
  
  // Add role-based outcomes
  if (roleDecisions) {
    Object.entries(roleDecisions).forEach(([role, decision]) => {
      if (role === 'medic' && decision.includes('first aid')) {
        consequences.push("🏥 Medic successfully treated 3 minor injuries");
      }
      if (role === 'communicator' && decision.includes('emergency')) {
        consequences.push("📞 Emergency services contacted - ETA 8 minutes");
      }
    });
  }
  
  return consequences;
}

// Serve the main demo page
app.get('/', (req, res) => {
  res.sendFile(join(__dirname, 'public', 'index.html'));
});

// Demo endpoint for hackathon judges
app.get('/demo', (req, res) => {
  const demoScenario = generateScenario({
    location: "Mumbai Office Building",
    buildingType: "high-rise",
    teamSize: 8,
    crisisType: "earthquake"
  });
  
  sessions.set(demoScenario.id, demoScenario);
  analytics.totalUsers++;
  analytics.activeSimulations++;
  
  res.json({
    message: "🎯 CrisisSim Demo for Puch AI Hackathon",
    scenario: demoScenario,
    usage: "Use this scenario ID to test the simulation",
    endpoints: {
      nextStep: `POST /next-step with scenarioId: ${demoScenario.id}`,
      status: `GET /scenario/${demoScenario.id}`
    }
  });
});

// Cleanup old sessions every 30 minutes
setInterval(() => {
  const now = Date.now();
  for (const [id, scenario] of sessions.entries()) {
    const sessionAge = now - new Date(scenario.startTime).getTime();
    if (sessionAge > 30 * 60 * 1000) { // 30 minutes
      sessions.delete(id);
      if (scenario.status === 'active') {
        analytics.activeSimulations--;
      }
    }
  }
}, 30 * 60 * 1000);

app.listen(PORT, () => {
  console.log(`🚀 CrisisSim MCP Server running on port ${PORT}`);
  console.log(`🌍 Ready for Puch AI Hackathon!`);
  console.log(`📊 Analytics: http://localhost:${PORT}/analytics`);
  console.log(`🎯 Demo: http://localhost:${PORT}/demo`);
});

export default app;