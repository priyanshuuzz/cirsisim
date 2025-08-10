#!/usr/bin/env python3
"""
Interactive Demo for CrisisSim MCP Server
This script provides an interactive way to test the CrisisSim functionality.
"""

import asyncio
import json
import subprocess
import sys
import os

class CrisisSimDemo:
    def __init__(self):
        self.process = None
        self.session_id = None
        
    def start_server(self):
        """Start the MCP server process."""
        try:
            self.process = subprocess.Popen(
                [sys.executable, "server.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("✅ MCP Server started successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def send_request(self, request):
        """Send a request to the MCP server."""
        try:
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()
            response = self.process.stdout.readline()
            return json.loads(response)
        except Exception as e:
            print(f"❌ Error sending request: {e}")
            return None
    
    def generate_scenario(self, crisis_type, location, people_count):
        """Generate a new crisis scenario."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "generateScenario",
                "arguments": {
                    "crisis_type": crisis_type,
                    "location": location,
                    "people_count": people_count
                }
            }
        }
        
        response = self.send_request(request)
        if response and "result" in response:
            content = response["result"]["content"][0]["text"]
            # Extract session ID
            self.session_id = content.split("Session ID: ")[1].split("\n")[0]
            return content
        return None
    
    def next_step(self, decision):
        """Get the next step in the scenario."""
        if not self.session_id:
            print("❌ No active session. Generate a scenario first.")
            return None
            
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "nextStep",
                "arguments": {
                    "session_id": self.session_id,
                    "decision": decision
                }
            }
        }
        
        response = self.send_request(request)
        if response and "result" in response:
            return response["result"]["content"][0]["text"]
        return None
    
    def cleanup(self):
        """Clean up the server process."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("✅ Server stopped.")

def main():
    """Main demo function."""
    print("🚨 CrisisSim MCP Server Demo")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set.")
        print("The server will use the hardcoded fallback key.")
    
    demo = CrisisSimDemo()
    
    if not demo.start_server():
        return
    
    try:
        while True:
            print("\n" + "="*50)
            print("CrisisSim Demo Menu:")
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
                
                print("\n🔄 Generating scenario...")
                result = demo.generate_scenario(crisis_type, location, people_count)
                
                if result:
                    print("\n✅ Scenario Generated:")
                    print(result)
                else:
                    print("❌ Failed to generate scenario.")
            
            elif choice == "2":
                if not demo.session_id:
                    print("❌ No active session. Generate a scenario first.")
                    continue
                
                print("\n--- Make Decision ---")
                decision = input("Enter your decision: ").strip()
                
                print("\n🔄 Processing decision...")
                result = demo.next_step(decision)
                
                if result:
                    print("\n✅ Updated Scenario:")
                    print(result)
                else:
                    print("❌ Failed to process decision.")
            
            elif choice == "3":
                if demo.session_id:
                    print(f"\nCurrent Session ID: {demo.session_id}")
                else:
                    print("\nNo active session.")
            
            elif choice == "4":
                print("\n👋 Thanks for using CrisisSim!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-4.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Cleaning up...")
    
    finally:
        demo.cleanup()

if __name__ == "__main__":
    main()
