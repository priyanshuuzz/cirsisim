# CrisisSim with Gemini API Integration

This document provides information about the Gemini API integration for the CrisisSim project.

## Overview

CrisisSim now supports Google's Gemini API as an alternative to OpenAI for generating crisis scenarios and responses. This integration allows you to use Google's powerful language models for more realistic and dynamic crisis simulations.

## Setup

### Prerequisites

- Python 3.8 or higher
- Required Python packages (install using `pip install -r requirements.txt`)
- Gemini API key

### Configuration

You can configure the Gemini API key in one of two ways:

1. **Environment Variable**: Set the `GEMINI_API_KEY` environment variable with your API key.

   ```bash
   # On Windows
   set GEMINI_API_KEY=your_api_key_here
   
   # On macOS/Linux
   export GEMINI_API_KEY=your_api_key_here
   ```

2. **Direct Configuration**: The default API key is already set in the code, but you can modify it in the `server_gemini.py` and `gemini_demo.py` files if needed.

## Running with Gemini API

### Using the Demo Script

The easiest way to test the Gemini API integration is to use the provided demo script:

```bash
# On Windows
run_gemini_demo.bat

# Or using PowerShell
.\run_gemini_demo.ps1

# On macOS/Linux
python gemini_demo.py
```

This will start an interactive demo that uses the Gemini API to generate crisis scenarios and responses.

### Automated Demo

You can also run an automated demo that generates a scenario and makes decisions without user input:

```bash
python gemini_demo.py --auto
```

### Using the Server

To use the Gemini-powered server in your own applications:

```bash
python server_gemini.py
```

This will start the MCP server with Gemini API integration.

## Fallback Mechanism

If the Gemini API is not available or encounters an error, the system will automatically fall back to using template-based generation. This ensures that the system remains functional even if there are issues with the API.

## Differences from OpenAI Integration

- The Gemini API uses different model names and parameters.
- The response format from Gemini is slightly different from OpenAI.
- The system has been optimized to work with Gemini's specific capabilities.

## Troubleshooting

### API Key Issues

If you encounter issues with the API key:

1. Verify that the API key is correct and has the necessary permissions.
2. Check that the environment variable is set correctly.
3. Try using the key directly in the code for testing.

### Connection Issues

If you encounter connection issues:

1. Check your internet connection.
2. Verify that the Gemini API is available and not experiencing downtime.
3. Check for any firewall or proxy settings that might be blocking the connection.

### Model Issues

If you encounter issues with the model responses:

1. Try adjusting the temperature and other generation parameters in the code.
2. Check that you're using a supported model name.
3. Verify that your prompts are well-formatted and clear.

## Support

For additional support or questions about the Gemini API integration, please refer to the Google Generative AI documentation or contact the project maintainers.