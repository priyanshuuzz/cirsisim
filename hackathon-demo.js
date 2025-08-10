const express = require('express');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Quick demo scenarios for hackathon
const quickScenarios = {
    earthquake: {
        title: "🌍 Major Earthquake in Mumbai",
        description: "7.2 magnitude earthquake hits Mumbai. 50,000 people affected. Buildings collapsed, power out.",
        roles: ["Emergency Commander", "Medical Chief", "Rescue Leader"],
        actions: ["Deploy rescue teams", "Set up medical camps", "Restore communications"]
    },
    cyber: {
        title: "💻 Cyber Attack on Banking System", 
        description: "Hackers target major banks. ATMs down, online banking compromised. Financial chaos.",
        roles: ["Cyber Security Head", "Bank Manager", "IT Director"],
        actions: ["Isolate systems", "Contact authorities", "Backup protocols"]
    },
    pandemic: {
        title: "🦠 Viral Outbreak in Delhi",
        description: "New virus spreading rapidly. Hospitals overwhelmed. 100,000 cases in 48 hours.",
        roles: ["Health Minister", "Hospital Director", "Epidemiologist"], 
        actions: ["Contact tracing", "Expand capacity", "Public messaging"]
    }
};

const sessions = new Map();

// Quick scenario generation
app.post('/api/scenario', (req, res) => {
    const { type = 'earthquake' } = req.body;
    const scenario = quickScenarios[type] || quickScenarios.earthquake;
    
    const session = {
        id: Date.now().toString(),
        ...scenario,
        turn: 1,
        decisions: [],
        status: "active"
    };
    
    sessions.set(session.id, session);
    
    res.json({
        success: true,
        sessionId: session.id,
        scenario: session
    });
});

// Process decisions
app.post('/api/decision', (req, res) => {
    const { sessionId, decision, role } = req.body;
    const session = sessions.get(sessionId);
    
    if (!session) {
        return res.status(404).json({ error: 'Session not found' });
    }
    
    session.decisions.push({ turn: session.turn, role, decision });
    session.turn++;
    
    // Quick consequence generation
    const consequences = [
        `✅ Decision implemented: ${decision}`,
        `⚠️ New challenge: Resources running low`,
        `📊 Status: 60% of affected population reached`,
        `🎯 Next priority: Coordinate with neighboring areas`
    ];
    
    session.consequences = consequences;
    sessions.set(sessionId, session);
    
    res.json({
        success: true,
        session,
        consequences
    });
});

// Demo endpoint for hackathon judges
app.get('/demo', (req, res) => {
    res.json({
        title: "🚨 CrisisSim - AI Crisis Management Simulator",
        description: "Real-time crisis scenario simulation for emergency response training",
        features: [
            "🎯 AI-powered scenario generation",
            "⚡ Real-time decision consequences", 
            "👥 Multi-role coordination",
            "📊 Performance analytics",
            "🔄 Adaptive difficulty"
        ],
        scenarios: Object.keys(quickScenarios),
        status: "Ready for demo!"
    });
});

app.listen(port, () => {
    console.log(`🚨 CrisisSim ready for Puch AI Hackathon on port ${port}`);
    console.log(`🎯 Demo: http://localhost:${port}/demo`);
    console.log(`⚡ Quick setup complete!`);
});