#!/usr/bin/env python3
"""
CrisisSim MCP Server - Gemini Version
Optimized for deployment with Gemini API integration.
"""

import asyncio
import json
import os
import uuid
import logging
from typing import Any, Dict, List
import google.generativeai as genai
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Load environment variables from .env.local if it exists
try:
    from dotenv import load_dotenv
    # Try to load from .env.local first, then fall back to .env
    if os.path.exists(".env.local"):
        load_dotenv(".env.local")
        print("Loaded environment variables from .env.local")
    else:
        load_dotenv()
        print("Loaded environment variables from .env")
except ImportError:
    print("python-dotenv not installed, skipping .env file loading")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crisissim.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Get Gemini API key from environment variable or use provided key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDyNSC5hJfPrVDp4bW8HaAHN1T8zHu2xrU")
logger.info(f"Gemini API Key available: {'Yes' if GEMINI_API_KEY else 'No'}")

# Get other configuration from environment variables
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Update logging level from environment variable
logging.getLogger().setLevel(getattr(logging, LOG_LEVEL))
logger.info(f"Log level set to {LOG_LEVEL}")
logger.info(f"Server will run on port {PORT}")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# In-memory storage for scenarios (in production, consider using Redis or database)
scenarios: Dict[str, Dict[str, Any]] = {}

# Create MCP server instance
server = Server("CrisisSim")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools."""
    logger.info("Listing available tools")
    return ListToolsResult(
        tools=[
            Tool(
                name="generateScenario",
                description="Generate a new crisis scenario with roles and initial actions",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "crisis_type": {
                            "type": "string",
                            "description": "Type of crisis (e.g., natural disaster, terrorist attack, pandemic, etc.)"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location where the Crisis occurs"
                        },
                        "people_count": {
                            "type": "integer",
                            "description": "Number of people affected by the crisis"
                        }
                    },
                    "required": ["crisis_type", "location", "people_count"]
                }
            ),
            Tool(
                name="nextStep",
                description="Get the next step in the crisis scenario based on a decision",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Session ID from the previous scenario"
                        },
                        "decision": {
                            "type": "string",
                            "description": "The decision made by the user"
                        }
                    },
                    "required": ["session_id", "decision"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    logger.info(f"Tool call: {name} with arguments: {arguments}")
    if name == "generateScenario":
        return await generate_scenario(arguments)
    elif name == "nextStep":
        return await next_step(arguments)
    else:
        logger.error(f"Unknown tool: {name}")
        raise ValueError(f"Unknown tool: {name}")

def generate_template_scenario(crisis_type: str, location: str, people_count: int) -> str:
    """Generate a scenario using template if API fails."""
    return f"""A {crisis_type} has occurred in {location}, affecting approximately {people_count} people. The situation requires immediate emergency response coordination and has overwhelmed local resources.

Assigned Roles:
1. Incident Commander - Coordinate overall emergency response and resource allocation across all affected areas
2. Medical Team Lead - Oversee triage, medical treatment, and casualty management for {people_count} affected individuals
3. Communications Officer - Manage public information, media relations, and inter-agency communication during the crisis

Recommended Actions:
1. Establish emergency command center and activate incident command system to coordinate response efforts
2. Deploy emergency response teams to the affected area and set up triage stations
3. Set up emergency shelters and medical triage centers to accommodate displaced residents"""

def generate_template_next_step(decision: str) -> str:
    """Generate next step using template if API fails."""
    return f"""Based on the decision to {decision}, the situation has evolved significantly. The emergency response has been implemented with both positive outcomes and new challenges that require immediate attention.

Current Status: The decision has been executed, but new complications have arisen including resource shortages, communication breakdowns, and coordination challenges between multiple agencies. Approximately 60% of the affected population has been reached, but 40% still require assistance.

Updated Recommended Actions:
1. Assess the effectiveness of the implemented decision and identify gaps in the response
2. Address new challenges that have emerged and coordinate with additional emergency services
3. Establish backup communication systems and resource distribution networks"""

async def generate_scenario(arguments: Dict[str, Any]) -> CallToolResult:
    """
    Generate a new crisis scenario - tries Gemini API first, falls back to template.
    """
    crisis_type = arguments["crisis_type"]
    location = arguments["location"]
    people_count = arguments["people_count"]
    
    logger.info(f"Generating scenario: {crisis_type} in {location} affecting {people_count} people")
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    # Try Gemini API first if key is available
    if GEMINI_API_KEY:
        try:
            # Configure the model
            generation_config = {
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 500,
            }
            
            # Create the model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                generation_config=generation_config
            )
            
            # Create the prompt
            prompt = f"""Generate a realistic Crisis scenario with the following details:
- Crisis Type: {crisis_type}
- Location: {location}
- People Affected: {people_count}

Please provide a 4-6 sentence scenario that includes:
1. Brief situation description
2. 3 assigned roles for responders (e.g., Incident Commander, Medical Team Lead, Communications Officer)
3. First 3 recommended actions

Make it realistic and engaging for crisis simulation training."""
            
            # Generate content
            system_instruction = "You are a Crisis simulation expert. Generate realistic, detailed Crisis scenarios for training purposes."
            response = model.generate_content(
                [
                    {"role": "user", "parts": [system_instruction, prompt]}
                ]
            )
            
            scenario = response.text.strip()
            logger.info("✅ Generated scenario using Gemini API")
            
        except Exception as e:
            # Fall back to template generation
            scenario = generate_template_scenario(crisis_type, location, people_count)
            logger.warning(f"⚠️ Gemini API failed, using template generation: {str(e)}")
    else:
        # No API key available, use template
        scenario = generate_template_scenario(crisis_type, location, people_count)
        logger.info("ℹ️ No Gemini API key available, using template generation")
    
    # Store scenario in memory
    scenarios[session_id] = {
        "crisis_type": crisis_type,
        "location": location,
        "people_count": people_count,
        "scenario": scenario,
        "step": 1,
        "created_at": asyncio.get_event_loop().time()
    }
    
    logger.info(f"Scenario stored with session ID: {session_id}")
    
    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"Session ID: {session_id}\n\nScenario:\n{scenario}"
            )
        ]
    )

async def next_step(arguments: Dict[str, Any]) -> CallToolResult:
    """
    Get the next step in the crisis scenario - tries Gemini API first, falls back to template.
    """
    session_id = arguments["session_id"]
    decision = arguments["decision"]
    
    logger.info(f"Processing next step for session {session_id} with decision: {decision}")
    
    # Retrieve previous scenario
    if session_id not in scenarios:
        logger.error(f"Session ID {session_id} not found")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: Session ID {session_id} not found. Please generate a new scenario first."
                )
            ]
        )
    
    previous_scenario = scenarios[session_id]
    
    # Try Gemini API first if key is available
    if GEMINI_API_KEY:
        try:
            # Configure the model
            generation_config = {
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 500,
            }
            
            # Create the model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                generation_config=generation_config
            )
            
            # Create the prompt
            prompt = f"""Previous Crisis Scenario:
{previous_scenario['scenario']}

User Decision: {decision}

Based on this decision, provide an updated scenario that includes:
1. Realistic consequences of the decision
2. New challenges or complications that arise
3. Updated recommended actions for the next phase
4. Current status of the crisis

Keep it realistic and maintain the same level of detail (4-6 sentences)."""
            
            # Generate content
            system_instruction = "You are a Crisis simulation expert. Provide realistic consequences and next steps based on user decisions."
            response = model.generate_content(
                [
                    {"role": "user", "parts": [system_instruction, prompt]}
                ]
            )
            
            updated_scenario = response.text.strip()
            logger.info("✅ Generated next step using Gemini API")
            
        except Exception as e:
            # Fall back to template generation
            updated_scenario = generate_template_next_step(decision)
            logger.warning(f"⚠️ Gemini API failed, using template generation: {str(e)}")
    else:
        # No API key available, use template
        updated_scenario = generate_template_next_step(decision)
        logger.info("ℹ️ No Gemini API key available, using template generation")
    
    # Update stored scenario
    scenarios[session_id]["scenario"] = updated_scenario
    scenarios[session_id]["step"] += 1
    scenarios[session_id]["last_updated"] = asyncio.get_event_loop().time()
    
    logger.info(f"Updated scenario for session {session_id}, now at step {scenarios[session_id]['step']}")
    
    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"Updated Scenario (Step {scenarios[session_id]['step']}):\n{updated_scenario}"
            )
        ]
    )

async def cleanup_old_sessions():
    """Clean up old sessions to prevent memory issues."""
    current_time = asyncio.get_event_loop().time()
    expired_sessions = []
    
    for session_id, session_data in scenarios.items():
        # Remove sessions older than 24 hours
        if current_time - session_data.get("created_at", 0) > 86400:  # 24 hours
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        del scenarios[session_id]
        logger.info(f"Cleaned up expired session: {session_id}")
    
    if expired_sessions:
        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")

async def main():
    """Main function to run the MCP server."""
    logger.info("Starting CrisisSim MCP Server (Gemini Version)")
    logger.info(f"Gemini API Key available: {'Yes' if GEMINI_API_KEY else 'No'}")
    
    # Start cleanup task
    async def periodic_cleanup():
        while True:
            await asyncio.sleep(3600)  # Run every hour
            await cleanup_old_sessions()
    
    # Start cleanup task in background
    asyncio.create_task(periodic_cleanup())
    
    # Check if we should run in HTTP mode or stdio mode
    if os.environ.get("HTTP_SERVER", "true").lower() == "true":
        # Import HTTP server modules
        try:
            from mcp.server.http import http_server
            from mcp.server.models import NotificationOptions
            logger.info(f"Starting HTTP server on port {PORT}")
            
            # Run the server in HTTP mode
            await http_server(
                server,
                InitializationOptions(
                    server_name="CrisisSim",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(tools_changed=True),
                        experimental_capabilities=None,
                    ),
                ),
                host="0.0.0.0",
                port=PORT
            )
        except ImportError:
            logger.error("Failed to import HTTP server modules. Falling back to stdio mode.")
            await run_stdio_server()
    else:
        # Run in stdio mode
        logger.info("Starting in stdio mode")
        await run_stdio_server()

async def run_stdio_server():
    """Run the server in stdio mode."""
    from mcp.server.models import NotificationOptions
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="CrisisSim",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(tools_changed=True),
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise