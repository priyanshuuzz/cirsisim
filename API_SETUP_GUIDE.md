# CrisisSim OpenAI API Integration Guide

This guide explains how to set up and use the OpenAI API with CrisisSim MCP server.

## 🔑 API Key Options

### Option 1: Use Your Own OpenAI API Key

1. **Get an OpenAI API Key:**
   - Go to [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Copy the key (starts with `sk-`)

2. **Set Environment Variable:**
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # Windows Command Prompt
   set OPENAI_API_KEY=your-api-key-here
   
   # Linux/Mac
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **Update server.py:**
   ```python
   # Replace this line in server.py
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
   ```

### Option 2: Use Fallback Version (No API Key Required)

If you don't have an API key or want to test without API calls:

```bash
# Use the fallback version
python server_fallback.py
```

### Option 3: Use Different API Key in Code

Edit `server.py` and replace the API key:

```python
# Line 30 in server.py
OPENAI_API_KEY = "your-new-api-key-here"
```

## 🧪 Testing API Integration

### Test with Your API Key

1. **Update the test script:**
   ```python
   # In test_openai.py, replace line 8
   OPENAI_API_KEY = "your-api-key-here"
   ```

2. **Run the test:**
   ```bash
   python test_openai.py
   ```

### Test Fallback Version

```bash
python test_fallback.py
```

## 🚀 Running the Server

### With OpenAI API (Full Version)
```bash
python server.py
```

### Without OpenAI API (Fallback Version)
```bash
python server_fallback.py
```

## 📋 API Usage Examples

### Example 1: Natural Disaster
```json
{
  "crisis_type": "natural disaster",
  "location": "Faridabad",
  "people_count": 5000
}
```

### Example 2: Terrorist Attack
```json
{
  "crisis_type": "terrorist attack",
  "location": "Mumbai",
  "people_count": 10000
}
```

### Example 3: Pandemic
```json
{
  "crisis_type": "pandemic",
  "location": "Delhi",
  "people_count": 50000
}
```

## 🔧 Troubleshooting

### Common Issues

1. **API Quota Exceeded:**
   - Error: "You exceeded your current quota"
   - Solution: Get a new API key or use fallback version

2. **Invalid API Key:**
   - Error: "Invalid API key"
   - Solution: Check your API key format (should start with `sk-`)

3. **Network Issues:**
   - Error: "Connection timeout"
   - Solution: Check internet connection

### Fallback Mode

If API calls fail, the fallback version provides:
- ✅ Realistic crisis scenarios
- ✅ Session management
- ✅ Decision-based progression
- ✅ Error handling
- ✅ No API key required

## 💡 Tips for Hackathon

### For Demo Purposes:
1. **Use Fallback Version:** No API key needed, works offline
2. **Pre-generate Scenarios:** Create sample scenarios beforehand
3. **Show Both Versions:** Demonstrate API and fallback capabilities

### For Production:
1. **Use Your API Key:** Get proper OpenAI API access
2. **Monitor Usage:** Track API calls and costs
3. **Error Handling:** Implement proper fallbacks

## 📁 File Structure

```
cirsisim/
├── server.py              # Full version with OpenAI API
├── server_fallback.py     # Fallback version (no API needed)
├── test_openai.py         # Test OpenAI API integration
├── test_fallback.py       # Test fallback version
├── API_SETUP_GUIDE.md     # This guide
└── ... (other files)
```

## 🎯 Quick Start Commands

```bash
# Test fallback version (recommended for demo)
python test_fallback.py

# Run fallback server
python server_fallback.py

# Test with your API key (if you have one)
python test_openai.py

# Run full server with API
python server.py
```

## ✅ Success Indicators

When API integration is working:
- ✅ "OpenAI client created successfully"
- ✅ "API call successful!"
- ✅ "Crisis scenario generated successfully!"

When fallback is working:
- ✅ "Scenario generated successfully!"
- ✅ "Next step processed successfully!"
- ✅ "All fallback tests completed successfully!"

## 🚨 Important Notes

1. **API Costs:** OpenAI API calls cost money. Monitor usage.
2. **Rate Limits:** API has rate limits. Use fallback for testing.
3. **Privacy:** Don't share API keys publicly.
4. **Backup:** Always have fallback version ready for demos.

## 🎉 Ready for Hackathon!

Your CrisisSim MCP server is now ready with:
- ✅ Full OpenAI API integration
- ✅ Fallback mode for offline use
- ✅ Comprehensive testing
- ✅ Error handling
- ✅ Session management
- ✅ Puch AI compatibility

Choose the version that works best for your needs!
