#!/usr/bin/env python3
"""
Test script for CrisisSim MCP Server
This script demonstrates how to test the server functionality.
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any

async def test_mcp_server():
    """Test the MCP server functionality."""
    
    print("🚨 CrisisSim MCP Server Test")
    print("=" * 50)
    
    # Start the server process
    process = subprocess.Popen(
        [sys.executable, "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Test 1: List tools
        print("\n1. Testing tool listing...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }
        
        process.stdin.write(json.dumps(list_tools_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print(f"Response: {response.strip()}")
        
        # Test 2: Generate scenario
        print("\n2. Testing scenario generation...")
        generate_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "generateScenario",
                "arguments": {
                    "crisis_type": "terrorist attack",
                    "location": "London Underground",
                    "people_count": 1000
                }
            }
        }
        
        process.stdin.write(json.dumps(generate_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print(f"Response: {response.strip()}")
        
        # Extract session ID from response
        try:
            response_data = json.loads(response)
            if "result" in response_data and "content" in response_data["result"]:
                content = response_data["result"]["content"][0]["text"]
                session_id = content.split("Session ID: ")[1].split("\n")[0]
                print(f"Session ID extracted: {session_id}")
                
                # Test 3: Next step
                print("\n3. Testing next step...")
                next_step_request = {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "nextStep",
                        "arguments": {
                            "session_id": session_id,
                            "decision": "Evacuate all stations and deploy bomb disposal units"
                        }
                    }
                }
                
                process.stdin.write(json.dumps(next_step_request) + "\n")
                process.stdin.flush()
                
                response = process.stdout.readline()
                print(f"Response: {response.strip()}")
                
        except Exception as e:
            print(f"Error extracting session ID: {e}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
    
    finally:
        # Clean up
        process.terminate()
        process.wait()
        print("\n✅ Test completed!")

if __name__ == "__main__":
    print("Note: This test script requires the server to be properly configured with OpenAI API key.")
    print("Make sure to set the OPENAI_API_KEY environment variable before running.")
    print("\nTo run the test:")
    print("1. Set your OpenAI API key: $env:OPENAI_API_KEY='your-key-here'")
    print("2. Run: python test_server.py")
    
    # Uncomment the line below to run the test
    # asyncio.run(test_mcp_server())
