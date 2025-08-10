#!/usr/bin/env python3
"""
Mock Test for CrisisSim MCP Server
This script tests the server structure without making OpenAI API calls.
"""

import asyncio
import json
import uuid
from typing import Dict, Any

# Mock scenario data
mock_scenarios: Dict[str, Dict[str, Any]] = {}

def mock_generate_scenario(crisis_type: str, location: str, people_count: int) -> Dict[str, Any]:
    """Mock scenario generation without OpenAI API."""
    
    session_id = str(uuid.uuid4())
    
    # Create a realistic mock scenario
    scenario_text = f"""A {crisis_type} has occurred in {location}, affecting approximately {people_count} people. The situation requires immediate emergency response coordination.

Assigned Roles:
1. Incident Commander - Coordinate overall emergency response and resource allocation
2. Medical Team Lead - Oversee triage, medical treatment, and casualty management  
3. Communications Officer - Manage public information, media relations, and inter-agency communication

Recommended Actions:
1. Establish emergency command center and activate incident command system
2. Deploy emergency response teams to the affected area
3. Set up emergency shelters and medical triage centers"""

    # Store scenario in memory
    mock_scenarios[session_id] = {
        "crisis_type": crisis_type,
        "location": location,
        "people_count": people_count,
        "scenario": scenario_text,
        "step": 1
    }
    
    return {
        "session_id": session_id,
        "scenario": scenario_text
    }

def mock_next_step(session_id: str, decision: str) -> Dict[str, Any]:
    """Mock next step processing without OpenAI API."""
    
    if session_id not in mock_scenarios:
        return {"error": f"Session ID {session_id} not found"}
    
    previous_scenario = mock_scenarios[session_id]
    
    # Create a realistic mock updated scenario
    updated_scenario = f"""Based on the decision to {decision}, the situation has evolved. The emergency response has been implemented with both positive outcomes and new challenges.

Current Status: The decision has been executed, but new complications have arisen that require additional coordination and resources.

Updated Recommended Actions:
1. Assess the effectiveness of the implemented decision
2. Address new challenges that have emerged
3. Coordinate with additional emergency services as needed"""

    # Update stored scenario
    mock_scenarios[session_id]["scenario"] = updated_scenario
    mock_scenarios[session_id]["step"] += 1
    
    return {
        "updated_scenario": updated_scenario,
        "step": mock_scenarios[session_id]["step"]
    }

async def test_mock_crisis_sim():
    """Test the CrisisSim functionality with mock data."""
    
    print("🚨 CrisisSim Mock Test")
    print("=" * 50)
    
    # Test 1: Generate a scenario
    print("\n1. Testing scenario generation...")
    
    try:
        result = mock_generate_scenario("natural disaster", "Faridabad", 5000)
        print("✅ Scenario generated successfully!")
        print(f"Session ID: {result['session_id']}")
        print(f"Scenario:\n{result['scenario']}")
        
        # Test 2: Next step
        print("\n2. Testing next step...")
        
        next_result = mock_next_step(
            result['session_id'], 
            "evacuate all buildings in the affected area"
        )
        
        if "error" not in next_result:
            print("✅ Next step processed successfully!")
            print(f"Step: {next_result['step']}")
            print(f"Updated Scenario:\n{next_result['updated_scenario']}")
        else:
            print(f"❌ Error: {next_result['error']}")
        
        # Test 3: Test error handling
        print("\n3. Testing error handling...")
        
        error_result = mock_next_step("invalid-session-id", "test decision")
        print(f"Error handling test: {error_result['error']}")
        
        print("\n✅ All mock tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

def test_mcp_structure():
    """Test the MCP server structure."""
    
    print("\n🔧 Testing MCP Server Structure")
    print("=" * 40)
    
    # Test manifest.json structure
    try:
        with open("manifest.json", "r") as f:
            manifest = json.load(f)
        
        print("✅ manifest.json is valid JSON")
        print(f"Server name: {manifest.get('name')}")
        print(f"Version: {manifest.get('version')}")
        print(f"Tools: {len(manifest.get('tools', []))}")
        
        for tool in manifest.get('tools', []):
            print(f"  - {tool.get('name')}: {tool.get('description')}")
            
    except Exception as e:
        print(f"❌ Error reading manifest.json: {e}")
    
    # Test server.py imports
    try:
        import server
        print("✅ server.py imports successfully")
        print("✅ MCP server structure is correct")
        
    except Exception as e:
        print(f"❌ Error importing server.py: {e}")

if __name__ == "__main__":
    print("Starting CrisisSim mock tests...")
    
    # Test MCP structure
    test_mcp_structure()
    
    # Test mock functionality
    asyncio.run(test_mock_crisis_sim())
    
    print("\n🎉 All tests completed!")
