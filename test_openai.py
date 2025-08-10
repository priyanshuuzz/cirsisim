#!/usr/bin/env python3
"""
Test OpenAI API Integration for CrisisSim
This script tests if the OpenAI API is working correctly.
"""

import openai

# Use the new API key
OPENAI_API_KEY = "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"

def test_openai_connection():
    """Test OpenAI API connection."""
    print("🔑 Testing OpenAI API Connection")
    print("=" * 40)
    
    try:
        # Create OpenAI client
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI client created successfully")
        
        # Test a simple API call
        print("🔄 Testing API call...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'Hello from CrisisSim!' in one sentence."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ API call successful!")
        print(f"Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_crisis_scenario_generation():
    """Test crisis scenario generation."""
    print("\n🚨 Testing Crisis Scenario Generation")
    print("=" * 40)
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = """Generate a brief crisis scenario with the following details:
- Crisis Type: natural disaster
- Location: Faridabad
- People Affected: 5000

Please provide a 2-3 sentence scenario that includes:
1. Brief situation description
2. 2 assigned roles for responders
3. 2 recommended actions

Make it realistic and engaging."""

        print("🔄 Generating crisis scenario...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crisis simulation expert. Generate realistic, detailed crisis scenarios for training purposes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        scenario = response.choices[0].message.content.strip()
        print("✅ Crisis scenario generated successfully!")
        print(f"Scenario:\n{scenario}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating scenario: {e}")
        return False

def main():
    """Run all OpenAI tests."""
    print("🚨 CrisisSim OpenAI API Integration Test")
    print("=" * 50)
    
    # Test basic connection
    connection_ok = test_openai_connection()
    
    if connection_ok:
        # Test scenario generation
        scenario_ok = test_crisis_scenario_generation()
        
        if scenario_ok:
            print("\n🎉 All OpenAI tests passed!")
            print("✅ OpenAI API is working correctly")
            print("✅ CrisisSim server is ready to use")
        else:
            print("\n❌ Scenario generation failed")
    else:
        print("\n❌ OpenAI API connection failed")
        print("Please check your API key and internet connection")

if __name__ == "__main__":
    main()
