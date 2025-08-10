#!/usr/bin/env python3
"""
CrisisSim Gemini Demo
This script demonstrates the CrisisSim server with Gemini API integration.
"""

import asyncio
import os
import sys
import uuid
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Get Gemini API key from environment variable or use provided key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDyNSC5hJfPrVDp4bW8HaAHN1T8zHu2xrU")

# Set environment variable for the server to use
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Store current session ID
current_session_id = None

async def generate_scenario_demo(crisis_type: str, location: str, people_count: int) -> str:
    """
    Generate a new crisis scenario using the Gemini API.
    """
    global current_session_id
    
    try:
        # Import here to avoid circular imports
        from server_gemini import generate_scenario
        
        # Call the server function
        result = await generate_scenario({
            "crisis_type": crisis_type,
            "location": location,
            "people_count": people_count
        })
        
        # Extract session ID from the response
        response_text = result.content[0].text
        lines = response_text.split('\n')
        current_session_id = lines[0].replace("Session ID: ", "").strip()
        
        return response_text
    except Exception as e:
        logger.error(f"Error generating scenario: {str(e)}")
        return f"Error generating scenario: {str(e)}"

async def next_step_demo(decision: str) -> str:
    """
    Get the next step in the crisis scenario based on a decision.
    """
    global current_session_id
    
    if not current_session_id:
        return "Error: No active scenario. Please generate a scenario first."
    
    try:
        # Import here to avoid circular imports
        from server_gemini import next_step
        
        # Call the server function
        result = await next_step({
            "session_id": current_session_id,
            "decision": decision
        })
        
        return result.content[0].text
    except Exception as e:
        logger.error(f"Error processing next step: {str(e)}")
        return f"Error processing next step: {str(e)}"

async def run_demo():
    """
    Run an automated demo of the CrisisSim server with Gemini API.
    """
    print("\n===== CrisisSim Gemini API Demo =====\n")
    print("Generating a crisis scenario...\n")
    
    # Generate a scenario
    scenario_result = await generate_scenario_demo(
        "earthquake", 
        "San Francisco", 
        5000
    )
    print(scenario_result)
    print("\n-----------------------------------\n")
    
    # Make a decision
    print("Making first decision...\n")
    decision1_result = await next_step_demo(
        "deploy search and rescue teams to collapsed buildings"
    )
    print(decision1_result)
    print("\n-----------------------------------\n")
    
    # Make another decision
    print("Making second decision...\n")
    decision2_result = await next_step_demo(
        "establish emergency medical facilities in Golden Gate Park"
    )
    print(decision2_result)
    print("\n-----------------------------------\n")
    
    print("Demo completed successfully!")
    print(f"Session ID: {current_session_id}")

async def main():
    """
    Main function to run the interactive demo.
    """
    global current_session_id
    
    print("\n===== CrisisSim Gemini Demo =====\n")
    print("This demo uses the Gemini API for generating crisis scenarios.")
    print(f"Gemini API Key available: {'Yes' if GEMINI_API_KEY else 'No'}")
    
    while True:
        print("\nOptions:")
        print("1. Generate a new scenario")
        print("2. Make a decision")
        print("3. Show current session ID")
        print("4. Run automated demo")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            crisis_type = input("Enter crisis type (e.g., earthquake, flood, fire): ")
            location = input("Enter location: ")
            try:
                people_count = int(input("Enter number of people affected: "))
            except ValueError:
                print("Invalid number. Using default value of 1000.")
                people_count = 1000
            
            result = await generate_scenario_demo(crisis_type, location, people_count)
            print("\nGenerated Scenario:")
            print(result)
            
        elif choice == "2":
            if not current_session_id:
                print("No active scenario. Please generate a scenario first.")
                continue
                
            decision = input("Enter your decision: ")
            result = await next_step_demo(decision)
            print("\nUpdated Scenario:")
            print(result)
            
        elif choice == "3":
            if current_session_id:
                print(f"Current Session ID: {current_session_id}")
            else:
                print("No active session. Please generate a scenario first.")
                
        elif choice == "4":
            await run_demo()
            
        elif choice == "5":
            print("Exiting CrisisSim Gemini Demo. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--auto":
            # Run automated demo
            asyncio.run(run_demo())
        else:
            # Run interactive demo
            asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDemo stopped by user")
    except Exception as e:
        logger.error(f"Demo error: {e}")
        raise