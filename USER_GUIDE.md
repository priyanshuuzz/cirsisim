# CrisisSim User Guide

## Overview

CrisisSim is an AI-driven crisis scenario simulator that helps users train for emergency response situations. It generates realistic crisis scenarios and allows users to make decisions to see how the situation evolves. This guide will help you get started with using CrisisSim.

## Installation

### Prerequisites
- Python 3.11 or higher
- OpenAI API key (optional, for enhanced functionality)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/priyanshuuzz/cirsisim.git
   cd cirsisim
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set your OpenAI API key:
   ```bash
   # On Linux/Mac
   export OPENAI_API_KEY="your-openai-api-key-here"
   
   # On Windows (PowerShell)
   $env:OPENAI_API_KEY="your-openai-api-key-here"
   ```

## Running CrisisSim

CrisisSim offers several ways to run the server:

### 1. Using the Demo Scripts

For a quick demonstration of CrisisSim's capabilities:

- **Automated Demo** (non-interactive):
  ```bash
  python demo_script.py
  ```
  This script automatically generates a scenario and makes decisions without requiring user input.

- **Simple Demo** (interactive, no API required):
  ```bash
  python simple_demo.py
  ```
  This interactive demo uses the fallback server that works without an OpenAI API key.

- **Hybrid Demo** (interactive, uses API when available):
  ```bash
  python hybrid_demo.py
  ```
  This interactive demo tries to use the OpenAI API first and falls back to templates if the API is unavailable.

### 2. Running the Server

To run the server for integration with other applications:

- **Production Server** (recommended):
  ```bash
  python server_production.py
  ```
  This version is optimized for deployment with environment variables and production features.

- **Hybrid Server** (tries API first, falls back to template):
  ```bash
  python server_hybrid.py
  ```
  This version attempts to use the OpenAI API first and falls back to template generation if the API fails.

- **Fallback Server** (no API needed):
  ```bash
  python server_fallback.py
  ```
  This version works without an OpenAI API key, using template-based generation.

## Using CrisisSim

### Generating a Crisis Scenario

When using the interactive demos, you'll be prompted to enter:
1. Crisis type (e.g., earthquake, flood, terrorist attack)
2. Location (e.g., New York, Tokyo, London)
3. Number of people affected

The system will generate a scenario with:
- A description of the crisis
- Assigned roles for responders
- Recommended initial actions

### Making Decisions

After a scenario is generated, you can make decisions about how to respond. The system will process your decision and provide:
- Updated scenario based on your decision
- New challenges or complications
- Current status of the crisis
- Updated recommended actions

## Testing

To test the functionality of CrisisSim:

```bash
# Test hybrid functionality
python test_hybrid.py

# Test fallback functionality
python test_fallback.py

# Test OpenAI integration
python test_openai.py
```

## Troubleshooting

### API Key Issues

If you're having issues with the OpenAI API:

1. Check if your API key is set correctly:
   ```bash
   # On Linux/Mac
   echo $OPENAI_API_KEY
   
   # On Windows (PowerShell)
   echo $env:OPENAI_API_KEY
   ```

2. If you don't have an API key, use the fallback server:
   ```bash
   python server_fallback.py
   ```

### Dependency Issues

If you encounter dependency problems:

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Additional Resources

- Check the `README.md` file for more information about the project
- Refer to `DEPLOYMENT_GUIDE.md` for deployment instructions
- See `FINAL_SETUP.md` for final setup instructions

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository: https://github.com/priyanshuuzz/cirsisim