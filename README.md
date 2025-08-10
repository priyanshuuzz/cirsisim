# CrisisSim MCP Server

An AI-driven crisis scenario simulator built as a Model Context Protocol (MCP) server. CrisisSim allows users to simulate real-world crisis situations and make decisions to see updated outcomes using OpenAI's GPT-4o-mini model.

## Features

- **generateScenario**: Create realistic crisis scenarios with assigned roles and initial actions
- **nextStep**: Get updated scenarios based on user decisions with realistic consequences
- **In-memory session management**: Track scenario progression across multiple steps
- **OpenAI GPT-4o-mini integration**: Generate dynamic, realistic crisis simulations

## Project Structure

```
cirsisim/
├── manifest.json      # MCP server manifest with tool definitions
├── server.py          # Main MCP server implementation
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

Set your OpenAI API key as an environment variable:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="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"

# Windows Command Prompt
set OPENAI_API_KEY=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

# Linux/Mac
export OPENAI_API_KEY="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"
```

### 3. Run the MCP Server

```bash
python server.py
```

The server will start and listen for MCP client connections via stdio.

## Tool Usage Examples

### 1. generateScenario Tool

**Purpose**: Generate a new crisis scenario with roles and initial actions.

**Parameters**:
- `crisis_type` (string): Type of crisis (e.g., natural disaster, terrorist attack, pandemic)
- `location` (string): Location where the crisis occurs
- `people_count` (integer): Number of people affected

**Example Request**:
```json
{
  "crisis_type": "natural disaster",
  "location": "New York City",
  "people_count": 50000
}
```

**Example Response**:
```
Session ID: 550e8400-e29b-41d4-a716-446655440000

Scenario:
A massive earthquake measuring 7.2 on the Richter scale has struck New York City, causing widespread destruction across Manhattan and Brooklyn. The earthquake has collapsed several buildings, triggered fires, and left approximately 50,000 people displaced or in need of immediate assistance. Emergency services are overwhelmed, and communication systems are partially down.

Assigned Roles:
1. Incident Commander - Coordinate overall emergency response and resource allocation
2. Medical Team Lead - Oversee triage, medical treatment, and casualty management
3. Communications Officer - Manage public information, media relations, and inter-agency communication

Recommended Actions:
1. Establish emergency command center and activate incident command system
2. Deploy search and rescue teams to collapsed structures
3. Set up emergency shelters and medical triage centers
```

### 2. nextStep Tool

**Purpose**: Get the next step in the crisis scenario based on a decision.

**Parameters**:
- `session_id` (string): Session ID from the previous scenario
- `decision` (string): The decision made by the user

**Example Request**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "decision": "Evacuate all buildings within a 2-mile radius of the epicenter"
}
```

**Example Response**:
```
Updated Scenario (Step 2):
The evacuation order has been successfully implemented, with emergency personnel systematically clearing buildings and directing residents to designated safe zones. However, the evacuation has created new challenges: traffic gridlock is preventing emergency vehicles from reaching critical areas, and some residents are refusing to leave their homes, requiring law enforcement intervention. The evacuation has also revealed that several underground gas lines have ruptured, creating additional fire hazards.

Current Status: Approximately 35,000 people have been evacuated, but 15,000 remain in the affected area. Emergency shelters are at 80% capacity, and medical teams are treating injuries from the evacuation process itself.

Updated Recommended Actions:
1. Implement traffic control measures and establish emergency vehicle corridors
2. Conduct door-to-door evacuation with law enforcement support
3. Deploy gas line repair teams and establish safety perimeters around ruptured lines
```

## Testing with MCP Clients

### Using Puch AI's MCP Client

1. Configure your MCP client to connect to the CrisisSim server
2. The server will be available via stdio protocol
3. Use the tool names `generateScenario` and `nextStep` to interact with the server

### Manual Testing

You can test the server manually by running it and sending JSON requests through stdin:

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | python server.py
```

## Crisis Types Supported

The simulator supports various crisis types including:
- Natural disasters (earthquakes, hurricanes, floods, wildfires)
- Terrorist attacks
- Pandemics and health emergencies
- Industrial accidents
- Transportation disasters
- Civil unrest and riots

## Session Management

- Each scenario gets a unique session ID (UUID)
- Scenarios are stored in memory during the server session
- Session data includes crisis type, location, people count, current scenario, and step number
- Sessions persist until the server is restarted

## Error Handling

The server includes comprehensive error handling for:
- Invalid session IDs
- OpenAI API errors
- Malformed requests
- Missing required parameters

## Development Notes

- The server uses in-memory storage for simplicity in this hackathon version
- For production use, consider implementing persistent storage
- The OpenAI API key is hardcoded as a fallback but should be set via environment variable
- Temperature is set to 0.7 for creative but consistent scenario generation

## License

This project is created for hackathon purposes. Feel free to modify and extend for your needs.
