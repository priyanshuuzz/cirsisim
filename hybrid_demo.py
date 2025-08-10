#!/usr/bin/env python3
"""
Hybrid CrisisSim Demo
This demo shows the hybrid version that tries API first, falls back to template.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the hybrid server functions
from server_hybrid import generate_scenario, next_step

class HybridCrisisSimDemo:
    def __init__(self):
        self.session_id = None
    
    async def generate_scenario_demo(self, crisis_type, location, people_count):
        """Generate a new crisis scenario."""
        print(f"\n🔄 Generating scenario for {crisis_type} in {location} affecting {people_count} people...")
        print("(Trying OpenAI API first, will fall back to template if API fails)")
        
        try:
            result = await generate_scenario({
                "crisis_type": crisis_type,
                "location": location,
                "people_count": people_count
            })
            
            print("✅ Scenario generated successfully!")
            print(f"\n{result.content[0].text}")
            
            # Extract session ID
            content = result.content[0].text
            self.session_id = content.split("Session ID: ")[1].split("\n")[0]
            print(f"\n📝 Session ID: {self.session_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating scenario: {e}")
            return False
    
    async def next_step_demo(self, decision):
        """Make a decision and get next step."""
        if not self.session_id:
            print("❌ No active session. Generate a scenario first.")
            return False
        
        print(f"\n🔄 Processing decision: {decision}")
        print("(Trying OpenAI API first, will fall back to template if API fails)")
        
        try:
            result = await next_step({
                "session_id": self.session_id,
                "decision": decision
            })
            
            print("✅ Decision processed successfully!")
            print(f"\n{result.content[0].text}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing decision: {e}")
            return False

async def main():
    """Main demo function."""
    print("🚨 CrisisSim Hybrid Demo")
    print("=" * 50)
    print("This demo uses the hybrid version:")
    print("- Tries OpenAI API first (when available)")
    print("- Falls back to template generation (when API fails)")
    print("- Always works, no matter what!")
    print("=" * 50)
    
    demo = HybridCrisisSimDemo()
    
    try:
        while True:
            print("\n" + "="*50)
            print("CrisisSim Hybrid Demo Menu:")
            print("1. Generate new scenario")
            print("2. Make decision (next step)")
            print("3. Show current session ID")
            print("4. Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\n--- Generate New Scenario ---")
                crisis_type = input("Enter crisis type (e.g., natural disaster, terrorist attack): ").strip()
                location = input("Enter location: ").strip()
                people_count = input("Enter number of people affected: ").strip()
                
                try:
                    people_count = int(people_count)
                except ValueError:
                    print("❌ Invalid number. Using 1000 as default.")
                    people_count = 1000
                
                await demo.generate_scenario_demo(crisis_type, location, people_count)
            
            elif choice == "2":
                if not demo.session_id:
                    print("❌ No active session. Generate a scenario first.")
                    continue
                
                print("\n--- Make Decision ---")
                decision = input("Enter your decision: ").strip()
                
                await demo.next_step_demo(decision)
            
            elif choice == "3":
                if demo.session_id:
                    print(f"\nCurrent Session ID: {demo.session_id}")
                else:
                    print("\nNo active session.")
            
            elif choice == "4":
                print("\n👋 Thanks for using CrisisSim Hybrid!")
                print("🎉 Your server is ready for Puch AI integration!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-4.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted.")

if __name__ == "__main__":
    asyncio.run(main())
