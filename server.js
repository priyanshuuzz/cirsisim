const express = require('express');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Crisis scenario templates (fallback when API unavailable)
const crisisTemplates = {
    natural_disaster: {
        title: "Major Earthquake Response",
        description: "A 7.2 magnitude earthquake has struck the metropolitan area. Buildings are damaged, power is out in several districts, and emergency services are overwhelmed.",
        roles: ["Emergency Coordinator", "Medical Team Leader", "Search & Rescue Chief"],
        initial_actions: [
            "Deploy search and rescue teams to collapsed buildings",
            "Set up emergency medical stations",
            "Coordinate with utility companies for power restoration",
            "Establish communication with affected areas"
        ]
    },
    cyber_attack: {
        title: "Critical Infrastructure Cyber Attack",
        description: "A sophisticated cyber attack has targeted the city's power grid and water treatment facilities. Systems are failing and public safety is at risk.",
        roles: ["Cybersecurity Lead", "Infrastructure Manager", "Public Safety Director"],
        initial_actions: [
            "Isolate affected systems from the network",
            "Activate backup power systems",
            "Coordinate with federal cybersecurity agencies",
            "Prepare public communication strategy"
        ]
    },
    pandemic: {
        title: "Infectious Disease Outbreak",
        description: "A highly contagious respiratory illness is spreading rapidly through the population. Hospitals are reaching capacity.",
        roles: ["Public Health Director", "Hospital Administrator", "Emergency Management Coordinator"],
        initial_actions: [
            "Implement contact tracing protocols",
            "Expand hospital capacity",
            "Coordinate with state health department",
            "Prepare public health messaging"
        ]
    }
};

// Active sessions storage
const sessions = new Map();

// Generate scenario endpoint
app.post('/generate-scenario', (req, res) => {
    try {
        const { type = 'natural_disaster', complexity = 'medium' } = req.body;
        
        // Use template (since Gemini API would require external calls)
        const template = crisisTemplates[type] || crisisTemplates.natural_disaster;
        
        const scenario = {
            id: Date.now().toString(),
            type,
            complexity,
            ...template,
            status: "active",
            turn: 1,
            decisions_made: [],
            created_at: new Date().toISOString()
        };
        
        // Store session
        sessions.set(scenario.id, scenario);
        
        res.json({
            success: true,
            scenario
        });
        
    } catch (error) {
        console.error('Error generating scenario:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to generate scenario'
        });
    }
});

// Next step endpoint
app.post('/next-step', (req, res) => {
    try {
        const { scenario_id, decision, role } = req.body;
        
        if (!scenario_id || !decision) {
            return res.status(400).json({
                success: false,
                error: 'Missing required parameters'
            });
        }
        
        const scenario = sessions.get(scenario_id);
        if (!scenario) {
            return res.status(404).json({
                success: false,
                error: 'Scenario not found'
            });
        }
        
        // Update scenario with decision
        scenario.decisions_made.push({
            turn: scenario.turn,
            role: role || 'Unknown',
            decision,
            timestamp: new Date().toISOString()
        });
        
        scenario.turn += 1;
        
        // Generate consequences (simplified logic)
        const consequences = generateConsequences(decision, scenario.type);
        scenario.current_situation = consequences.situation;
        scenario.available_actions = consequences.actions;
        
        // Update session
        sessions.set(scenario_id, scenario);
        
        res.json({
            success: true,
            scenario,
            consequences: consequences.description
        });
        
    } catch (error) {
        console.error('Error processing next step:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to process decision'
        });
    }
});

// Get scenario status
app.get('/scenario/:id', (req, res) => {
    const scenario = sessions.get(req.params.id);
    if (!scenario) {
        return res.status(404).json({
            success: false,
            error: 'Scenario not found'
        });
    }
    
    res.json({
        success: true,
        scenario
    });
});

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        active_sessions: sessions.size
    });
});

// Helper function to generate consequences
function generateConsequences(decision, crisisType) {
    const consequences = {
        natural_disaster: {
            situation: "Emergency teams are responding to your decision. The situation is evolving rapidly.",
            description: "Your decision has been implemented. Resources are being deployed accordingly.",
            actions: [
                "Assess damage reports from field teams",
                "Coordinate with neighboring jurisdictions",
                "Update public safety announcements",
                "Review resource allocation"
            ]
        },
        cyber_attack: {
            situation: "Cybersecurity teams are implementing your directive. System status is being monitored.",
            description: "Security protocols have been updated based on your decision.",
            actions: [
                "Monitor system recovery progress",
                "Coordinate with law enforcement",
                "Prepare incident report",
                "Review security protocols"
            ]
        },
        pandemic: {
            situation: "Public health measures are being adjusted according to your decision.",
            description: "Health officials are implementing your recommended course of action.",
            actions: [
                "Monitor infection rates",
                "Coordinate with healthcare facilities",
                "Update public health guidelines",
                "Review resource distribution"
            ]
        }
    };
    
    return consequences[crisisType] || consequences.natural_disaster;
}

// Cleanup old sessions (run every hour)
setInterval(() => {
    const oneHourAgo = Date.now() - (60 * 60 * 1000);
    for (const [id, scenario] of sessions.entries()) {
        if (new Date(scenario.created_at).getTime() < oneHourAgo) {
            sessions.delete(id);
        }
    }
    console.log(`Cleaned up old sessions. Active sessions: ${sessions.size}`);
}, 60 * 60 * 1000);

app.listen(port, () => {
    console.log(`🚨 CrisisSim MCP Server running on port ${port}`);
    console.log(`📊 Health check: http://localhost:${port}/health`);
    console.log(`🎯 Ready to handle crisis scenarios!`);
});