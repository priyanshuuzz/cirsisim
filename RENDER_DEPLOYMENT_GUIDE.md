# CrisisSim MCP Server - Render Deployment Guide (Gemini API Version)

इस गाइड में Render पर CrisisSim MCP Server को Gemini API के साथ डिप्लॉय करने के चरण-दर-चरण निर्देश दिए गए हैं।

## 📋 आवश्यकताएँ

- ✅ Render.com पर एक खाता
- ✅ GitHub पर एक खाता (वैकल्पिक, अगर आप GitHub से डिप्लॉय करना चाहते हैं)
- ✅ Google Gemini API की (वैकल्पिक, लेकिन बेहतर परिणामों के लिए अनुशंसित)

## 🚀 Render पर डिप्लॉय करने के चरण

### विकल्प 1: GitHub से डिप्लॉय करना

#### चरण 1: अपने रिपॉजिटरी को तैयार करें
```bash
# git को इनिशियलाइज़ करें (अगर पहले से नहीं किया है)
git init
git add .
git commit -m "Initial commit - CrisisSim MCP Server with Gemini API"

# GitHub रिपॉजिटरी बनाएँ और पुश करें
git remote add origin https://github.com/yourusername/crisissim-mcp-server.git
git push -u origin main
```

#### चरण 2: Render पर डिप्लॉय करें
1. [Render Dashboard](https://dashboard.render.com) पर जाएँ
2. "New +" → "Web Service" पर क्लिक करें
3. अपनी GitHub रिपॉजिटरी को कनेक्ट करें
4. सर्विस को कॉन्फ़िगर करें:
   - **Name**: `crisissim-mcp-server`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server_gemini.py`
5. एनवायरनमेंट वेरिएबल्स जोड़ें:
   - `GEMINI_API_KEY`: आपकी Google Gemini API की
6. "Create Web Service" पर क्लिक करें

### विकल्प 2: Render CLI से डिप्लॉय करना

#### चरण 1: Render CLI इंस्टॉल करें
```bash
npm install -g @renderinc/cli
```

#### चरण 2: डिप्लॉय करें
```bash
# Render में लॉगिन करें
render login

# प्रोजेक्ट को इनिशियलाइज़ करें
render init

# डिप्लॉय करें
render deploy
```

### विकल्प 3: Render Dashboard से मैन्युअल डिप्लॉय

1. [Render Dashboard](https://dashboard.render.com) पर जाएँ
2. "New +" → "Web Service" पर क्लिक करें
3. "Build and deploy from a Git repository" के बजाय "Deploy an existing image or service" चुनें
4. "Upload Files" विकल्प चुनें और अपने प्रोजेक्ट फाइल्स को अपलोड करें
5. सर्विस को कॉन्फ़िगर करें (ऊपर दिए गए विवरण के अनुसार)
6. "Create Web Service" पर क्लिक करें

## ⚙️ एनवायरनमेंट वेरिएबल्स

### आवश्यक वेरिएबल्स
- `GEMINI_API_KEY`: आपकी Google Gemini API की (वैकल्पिक, सर्वर इसके बिना भी काम करेगा लेकिन टेम्पलेट-आधारित परिदृश्य उत्पन्न करेगा)

### वैकल्पिक वेरिएबल्स
- `LOG_LEVEL`: `DEBUG`, `INFO`, `WARNING`, या `ERROR` पर सेट करें (डिफ़ॉल्ट: `INFO`)
- `PORT`: सर्वर को चलाने के लिए पोर्ट (डिफ़ॉल्ट: 8000)
- `HTTP_SERVER`: `true` या `false` पर सेट करें (डिफ़ॉल्ट: `true`) - HTTP सर्वर मोड या stdio मोड में चलाने के लिए

### .env.local का उपयोग
लोकल डेवलपमेंट के लिए, आप `.env.local` फाइल का उपयोग कर सकते हैं:

1. प्रोजेक्ट रूट में `.env.local` फाइल बनाएँ
2. निम्न फॉर्मेट में एनवायरनमेंट वेरिएबल्स जोड़ें:
   ```
   GEMINI_API_KEY=your-api-key-here
   PORT=8000
   LOG_LEVEL=INFO
   HTTP_SERVER=true
   ```
3. यह फाइल `.gitignore` में शामिल है, इसलिए यह GitHub पर पुश नहीं होगी
4. सर्वर स्टार्ट होने पर `.env.local` से वेरिएबल्स स्वचालित रूप से लोड हो जाएंगे

## 🔍 अपनी डिप्लॉयमेंट की जाँच करना

Render आपकी सर्विस के लिए एक URL प्रदान करेगा, जैसे: `https://your-app-name.onrender.com`

### API एंडपॉइंट्स का परीक्षण

```bash
# परिदृश्य उत्पन्न करने का परीक्षण
curl -X POST https://your-app-name.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{"crisis_type": "natural disaster", "location": "Mumbai", "people_count": 5000}'
```

## 🔄 अपडेट्स और मेंटेनेंस

### अपनी सर्विस को अपडेट करना

अपने कोड में परिवर्तन करने के बाद, बस अपने परिवर्तनों को GitHub पर पुश करें, और Render स्वचालित रूप से आपकी सर्विस को पुनः डिप्लॉय करेगा (अगर आपने `autoDeploy: true` सेट किया है)।

### लॉग्स देखना

Render डैशबोर्ड पर अपनी सर्विस के लॉग्स देखें:
1. अपनी सर्विस पर क्लिक करें
2. "Logs" टैब पर जाएँ

## 🚨 समस्या निवारण

### सामान्य समस्याएँ

#### 1. डिप्लॉयमेंट फेल हो रही है
- Render लॉग्स की जाँच करें
- `requirements.txt` में सभी आवश्यक पैकेज शामिल हैं, यह सुनिश्चित करें
- `render.yaml` फाइल की सिंटैक्स की जाँच करें

#### 2. API की समस्याएँ
- Render डैशबोर्ड में `GEMINI_API_KEY` एनवायरनमेंट वेरिएबल की जाँच करें
- API की के बिलिंग स्टेटस की जाँच करें

## 🎉 सफलता संकेतक

जब डिप्लॉयमेंट सफल हो जाती है:
- ✅ सर्वर बिना किसी त्रुटि के शुरू होता है
- ✅ लॉग्स "Starting CrisisSim MCP Server (Gemini Version)" दिखाते हैं
- ✅ API एंडपॉइंट्स सही ढंग से प्रतिक्रिया देते हैं
- ✅ हेल्थ चेक पास होते हैं

## 🎊 बधाई हो!

आपका CrisisSim MCP सर्वर अब Render पर Gemini API के साथ डिप्लॉय हो गया है! 🚀