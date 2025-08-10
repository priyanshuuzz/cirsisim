#!/usr/bin/env python3
"""
CrisisSim MCP Server - Hybrid Version
This version tries OpenAI API first, but falls back to template generation if API fails.
"""

import asyncio
import json
import os
import uuid
from typing import Any, Dict, List
import openai
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

# OpenAI API key
OPENAI_API_KEY = "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"

# In-memory storage for scenarios
scenarios: Dict[str, Dict[str, Any]] = {}

# Create MCP server instance
server = Server("CrisisSim")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools."""
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
                            "description": "Location where the crisis occurs"
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
    if name == "generateScenario":
        return await generate_scenario(arguments)
    elif name == "nextStep":
        return await next_step(arguments)
    else:
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
    Generate a new crisis scenario - tries OpenAI API first, falls back to template.
    """
    crisis_type = arguments["crisis_type"]
    location = arguments["location"]
    people_count = arguments["people_count"]
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    # Try OpenAI API first
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        prompt = f"""Generate a realistic crisis scenario with the following details:
- Crisis Type: {crisis_type}
- Location: {location}
- People Affected: {people_count}

Please provide a 4-6 sentence scenario that includes:
1. Brief situation description
2. 3 assigned roles for responders (e.g., Incident Commander, Medical Team Lead, Communications Officer)
3. First 3 recommended actions

Make it realistic and engaging for crisis simulation training."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crisis simulation expert. Generate realistic, detailed crisis scenarios for training purposes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        scenario = response.choices[0].message.content.strip()
        print(f"✅ Generated scenario using OpenAI API")
        
    except Exception as e:
        # Fall back to template generation
        scenario = generate_template_scenario(crisis_type, location, people_count)
        print(f"⚠️ OpenAI API failed, using template generation: {str(e)}")
    
    # Store scenario in memory
    scenarios[session_id] = {
        "crisis_type": crisis_type,
        "location": location,
        "people_count": people_count,
        "scenario": scenario,
        "step": 1
    }
    
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
    Get the next step in the crisis scenario - tries OpenAI API first, falls back to template.
    """
    session_id = arguments["session_id"]
    decision = arguments["decision"]
    
    # Retrieve previous scenario
    if session_id not in scenarios:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: Session ID {session_id} not found. Please generate a new scenario first."
                )
            ]
        )
    
    previous_scenario = scenarios[session_id]
    
    # Try OpenAI API first
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        prompt = f"""Previous Crisis Scenario:
{previous_scenario['scenario']}

User Decision: {decision}

Based on this decision, provide an updated scenario that includes:
1. Realistic consequences of the decision
2. New challenges or complications that arise
3. Updated recommended actions for the next phase
4. Current status of the crisis

Keep it realistic and maintain the same level of detail (4-6 sentences)."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crisis simulation expert. Provide realistic consequences and next steps based on user decisions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        updated_scenario = response.choices[0].message.content.strip()
        print(f"✅ Generated next step using OpenAI API")
        
    except Exception as e:
        # Fall back to template generation
        updated_scenario = generate_template_next_step(decision)
        print(f"⚠️ OpenAI API failed, using template generation: {str(e)}")
    
    # Update stored scenario
    scenarios[session_id]["scenario"] = updated_scenario
    scenarios[session_id]["step"] += 1
    
    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"Updated Scenario (Step {scenarios[session_id]['step']}):\n{updated_scenario}"
            )
        ]
    )

async def main():
    """Main function to run the MCP server."""
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="CrisisSim",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
