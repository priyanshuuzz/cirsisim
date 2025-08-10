#!/usr/bin/env python3
"""
CrisisSim Demo Script
This script demonstrates how to use the CrisisSim server without requiring user interaction.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the fallback server functions (works without API)
from server_fallback import generate_scenario, next_step

async def run_demo():
    """Run a demonstration of CrisisSim."""
    print("🚨 CrisisSim Automated Demo")
    print("=" * 50)
    
    # Example crisis parameters
    crisis_type = "earthquake"
    location = "San Francisco"
    people_count = 5000
    
    print(f"\n🔄 Generating scenario for {crisis_type} in {location} affecting {people_count} people...")
    
    try:
        # Generate a scenario
        result = await generate_scenario({
            "crisis_type": crisis_type,
            "location": location,
            "people_count": people_count
        })
        
        print("✅ Scenario generated successfully!")
        print(f"\n{result.content[0].text}")
        
        # Extract session ID
        content = result.content[0].text
        session_id = content.split("Session ID: ")[1].split("\n")[0]
        print(f"\n📝 Session ID: {session_id}")
        
        # Example decision
        decision = "Deploy emergency response teams to affected areas and establish evacuation centers"
        print(f"\n🔄 Processing decision: {decision}")
        
        # Get next step based on decision
        result = await next_step({
            "session_id": session_id,
            "decision": decision
        })
        
        print("✅ Decision processed successfully!")
        print(f"\n{result.content[0].text}")
        
        # Another example decision
        decision = "Request additional resources from neighboring cities and establish a unified command center"
        print(f"\n🔄 Processing decision: {decision}")
        
        # Get next step based on decision
        result = await next_step({
            "session_id": session_id,
            "decision": decision
        })
        
        print("✅ Decision processed successfully!")
        print(f"\n{result.content[0].text}")
        
        print("\n👋 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")

if __name__ == "__main__":
    asyncio.run(run_demo())