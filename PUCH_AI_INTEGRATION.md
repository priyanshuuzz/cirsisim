# CrisisSim MCP Server - Puch AI Integration Guide

This guide explains how to integrate the CrisisSim MCP server with Puch AI's MCP client.

## Quick Start

### 1. Install and Setup

```bash
# Install dependencies
python setup.py

# Or manually
pip install -r requirements.txt
```

### 2. Configure Puch AI MCP Client

In your Puch AI MCP client configuration, add the CrisisSim server:

```json
{
  "mcpServers": {
    "crisissim": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/cirsisim"
    }
  }
}
```

### 3. Available Tools

Once connected, you'll have access to two tools:

#### `generateScenario`
Creates a new crisis simulation scenario.

**Parameters:**
- `crisis_type` (string): Type of crisis (e.g., "natural disaster", "terrorist attack", "pandemic")
- `location` (string): Location where crisis occurs (e.g., "New York City", "London Underground")
- `people_count` (integer): Number of people affected

**Example Puch AI prompt:**
```
Generate a crisis scenario for a terrorist attack in London with 1000 people affected.
```

#### `nextStep`
Advances the scenario based on a decision.

**Parameters:**
- `session_id` (string): Session ID from previous scenario
- `decision` (string): The decision made by the user

**Example Puch AI prompt:**
```
Given the session ID [SESSION_ID], what happens if I decide to evacuate all buildings?
```

## Usage Examples

### Scenario 1: Natural Disaster Response

1. **Generate Scenario:**
   ```
   Generate a natural disaster scenario in Tokyo affecting 50,000 people
   ```

2. **Make Decision:**
   ```
   Based on session [SESSION_ID], what if I order immediate evacuation of coastal areas?
   ```

3. **Continue Simulation:**
   ```
   Given the updated scenario, what if I deploy emergency medical teams to the affected areas?
   ```

### Scenario 2: Pandemic Crisis

1. **Generate Scenario:**
   ```
   Create a pandemic scenario in New York City affecting 100,000 people
   ```

2. **Make Decision:**
   ```
   For session [SESSION_ID], what happens if I implement a city-wide lockdown?
   ```

## Integration Tips

### 1. Session Management
- Always save the session ID returned from `generateScenario`
- Use the same session ID for subsequent `nextStep` calls
- Sessions persist until the server is restarted

### 2. Decision Making
- Be specific in your decisions for more realistic outcomes
- Consider the context of the current scenario
- Decisions can have both positive and negative consequences

### 3. Scenario Types
The simulator supports various crisis types:
- Natural disasters (earthquakes, hurricanes, floods)
- Terrorist attacks
- Pandemics and health emergencies
- Industrial accidents
- Transportation disasters
- Civil unrest

## Troubleshooting

### Common Issues

1. **Server Connection Failed**
   - Ensure Python is in your PATH
   - Check that all dependencies are installed
   - Verify the server.py file is executable

2. **OpenAI API Errors**
   - Check your API key is valid
   - Ensure you have sufficient credits
   - Verify network connectivity

3. **Session Not Found**
   - Make sure you're using the correct session ID
   - Check that the server hasn't been restarted
   - Generate a new scenario if needed

### Debug Mode

To run the server in debug mode:

```bash
python -u server.py
```

This will show detailed error messages and API responses.

## Advanced Usage

### Custom Crisis Types
You can create custom crisis scenarios by specifying unique crisis types:

```
Generate a cyber attack scenario in a financial district affecting 10,000 people
```

### Complex Decisions
Make multi-faceted decisions for more realistic outcomes:

```
For session [SESSION_ID], what if I simultaneously evacuate the area, deploy emergency medical teams, and establish a command center?
```

## API Response Format

The server returns responses in MCP format:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Session ID: [UUID]\n\nScenario: [Detailed scenario description]"
      }
    ]
  }
}
```

## Performance Notes

- Each API call to OpenAI takes 1-3 seconds
- The server uses in-memory storage (sessions lost on restart)
- GPT-4o-mini provides good balance of speed and quality
- Temperature is set to 0.7 for creative but consistent responses

## Support

For issues or questions:
1. Check the main README.md for detailed documentation
2. Run the demo script: `python demo.py`
3. Test the server: `python test_server.py`

The CrisisSim MCP server is designed to be hackathon-ready and production-capable for crisis simulation training scenarios.
