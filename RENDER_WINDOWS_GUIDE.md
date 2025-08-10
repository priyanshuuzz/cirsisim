# CrisisSim MCP Server - Render Deployment Guide for Windows

इस गाइड में Windows पर CrisisSim MCP Server को Render पर डिप्लॉय करने के चरण-दर-चरण निर्देश दिए गए हैं।

## 📋 आवश्यकताएँ

- ✅ Windows 10 या Windows 11
- ✅ Git for Windows
- ✅ GitHub खाता
- ✅ Render.com खाता
- ✅ Google Gemini API की (वैकल्पिक, लेकिन अनुशंसित)

## 🚀 Render पर डिप्लॉय करने के चरण

### चरण 1: GitHub रिपॉजिटरी तैयार करें

1. GitHub पर एक नया रिपॉजिटरी बनाएँ (https://github.com/new)
   - रिपॉजिटरी का नाम: `crisissim-mcp-server`
   - विवरण: `CrisisSim MCP Server with Gemini API`
   - Public या Private चुनें
   - "Initialize this repository with a README" को अनचेक करें
   - "Create repository" पर क्लिक करें

2. अपने प्रोजेक्ट को GitHub पर पुश करने से पहले, .env.local फाइल बनाएँ:
   - प्रोजेक्ट रूट में `.env.local` फाइल बनाएँ
   - निम्न फॉर्मेट में एनवायरनमेंट वेरिएबल्स जोड़ें:
     ```
     GEMINI_API_KEY=your-api-key-here
     PORT=8000
     LOG_LEVEL=INFO
     HTTP_SERVER=true
     ```
   - `.gitignore` फाइल में `.env.local` जोड़ें ताकि यह GitHub पर पुश न हो

3. अपने प्रोजेक्ट को GitHub पर पुश करें:
   - PowerShell या Git Bash खोलें
   - अपने प्रोजेक्ट फोल्डर में नेविगेट करें: `cd "C:\New folder\cirsisim"`
   - Git रिपॉजिटरी इनिशियलाइज़ करें:
     ```
     git init
     git add .
     git commit -m "Initial commit - CrisisSim MCP Server with Gemini API"
     git branch -M main
     git remote add origin https://github.com/YOUR_USERNAME/crisissim-mcp-server.git
     git push -u origin main
     ```
     (YOUR_USERNAME को अपने GitHub उपयोगकर्ता नाम से बदलें)

### चरण 2: Render पर डिप्लॉय करें

1. [Render Dashboard](https://dashboard.render.com) पर जाएँ और लॉगिन करें

2. "New +" बटन पर क्लिक करें और "Web Service" चुनें

3. "Connect a repository" पर क्लिक करें और GitHub को कनेक्ट करें
   - अपने GitHub खाते को अधिकृत करें (यदि पहले से नहीं किया है)
   - `crisissim-mcp-server` रिपॉजिटरी को खोजें और चुनें

4. सर्विस कॉन्फ़िगरेशन:
   - **Name**: `crisissim-mcp-server`
   - **Region**: अपने स्थान के निकटतम क्षेत्र चुनें
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server_gemini.py`

5. "Advanced" सेक्शन में क्लिक करें और एनवायरनमेंट वेरिएबल्स जोड़ें:
   - `GEMINI_API_KEY`: अपनी Google Gemini API की
   - `PYTHON_VERSION`: `3.11.0`
   - `HTTP_SERVER`: `true` (HTTP सर्वर मोड में चलाने के लिए)
   - `HTTP_SERVER`: `true`

6. "Create Web Service" पर क्लिक करें

7. डिप्लॉयमेंट प्रगति देखें
   - Render अब आपके कोड को बिल्ड और डिप्लॉय करेगा
   - यह प्रक्रिया 5-10 मिनट तक चल सकती है

8. डिप्लॉयमेंट पूरा होने के बाद, आपकी सर्विस एक URL पर उपलब्ध होगी:
   - `https://crisissim-mcp-server.onrender.com`

## 🔄 अपडेट्स और मेंटेनेंस

### अपनी सर्विस को अपडेट करना

1. अपने लोकल कोड में परिवर्तन करें

2. परिवर्तनों को GitHub पर पुश करें:
   ```
   git add .
   git commit -m "Update description"
   git push
   ```

3. Render स्वचालित रूप से आपकी सर्विस को पुनः डिप्लॉय करेगा (यदि आपने `autoDeploy: true` सेट किया है)

### लॉग्स देखना

1. Render डैशबोर्ड पर अपनी सर्विस पर क्लिक करें
2. "Logs" टैब पर जाएँ

## 🚨 समस्या निवारण

### सामान्य समस्याएँ

#### 1. Git पुश त्रुटियाँ
- GitHub क्रेडेंशियल्स की जाँच करें
- सुनिश्चित करें कि आपके पास रिपॉजिटरी तक पहुँच है

#### 2. डिप्लॉयमेंट फेल हो रही है
- Render लॉग्स की जाँच करें
- `requirements.txt` में सभी आवश्यक पैकेज शामिल हैं, यह सुनिश्चित करें

#### 3. API की समस्याएँ
- Render डैशबोर्ड में `GEMINI_API_KEY` एनवायरनमेंट वेरिएबल की जाँच करें
- API की के बिलिंग स्टेटस की जाँच करें

## 🎉 सफलता संकेतक

जब डिप्लॉयमेंट सफल हो जाती है:
- ✅ Render डैशबोर्ड में "Live" स्टेटस दिखाई देगा
- ✅ आपकी सर्विस URL पर जाने पर कोई त्रुटि नहीं दिखेगी
- ✅ API एंडपॉइंट्स सही ढंग से प्रतिक्रिया देंगे

## 🎊 बधाई हो!

आपका CrisisSim MCP सर्वर अब Render पर Gemini API के साथ डिप्लॉय हो गया है! 🚀