#!/usr/bin/env python3
"""
Test Fallback CrisisSim MCP Server
This script tests the fallback version without OpenAI API calls.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the fallback server functions
from server_fallback import generate_scenario, next_step

async def test_fallback_crisis_sim():
    """Test the CrisisSim fallback functionality."""
    
    print("🚨 CrisisSim Fallback Test")
    print("=" * 50)
    
    # Test 1: Generate a scenario
    print("\n1. Testing scenario generation...")
    
    test_args = {
        "crisis_type": "natural disaster",
        "location": "Faridabad",
        "people_count": 5000
    }
    
    try:
        result = await generate_scenario(test_args)
        print("✅ Scenario generated successfully!")
        print(f"Result: {result.content[0].text}")
        
        # Extract session ID
        content = result.content[0].text
        session_id = content.split("Session ID: ")[1].split("\n")[0]
        print(f"Session ID: {session_id}")
        
        # Test 2: Next step
        print("\n2. Testing next step...")
        
        next_step_args = {
            "session_id": session_id,
            "decision": "Evacuate all buildings in the affected area"
        }
        
        next_result = await next_step(next_step_args)
        print("✅ Next step processed successfully!")
        print(f"Result: {next_result.content[0].text}")
        
        # Test 3: Error handling
        print("\n3. Testing error handling...")
        
        error_args = {
            "session_id": "invalid-session-id",
            "decision": "test decision"
        }
        
        error_result = await next_step(error_args)
        print(f"Error handling test: {error_result.content[0].text}")
        
        print("\n✅ All fallback tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting CrisisSim fallback test...")
    asyncio.run(test_fallback_crisis_sim())
