# 🚀 Quick Setup Guide - Memory AI Assistant

## Step-by-Step Installation

### 1. Get Your FREE Gemini API Key (Required)

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### 2. Configure Your API Keys

Open the `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here
```

**Optional APIs** (for enhanced features):
- **ElevenLabs** (voice cloning): https://elevenlabs.io/
- **D-ID** (avatar generation): https://www.d-id.com/

### 3. Install Dependencies

Open terminal/command prompt in the project folder:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

**Windows:**
```bash
start.bat
```

**Or manually:**
```bash
python app.py
```

### 5. Open in Browser

Navigate to: http://localhost:5000

## 🎯 First Time Usage

### Welcome Screen
1. **Upload Avatar Image** (optional)
   - Click the image upload box
   - Select a photo (PNG, JPG, GIF)
   - You'll see a checkmark when uploaded

2. **Upload Voice Sample** (optional)
   - Click the voice upload box
   - Select audio file (MP3, WAV, M4A)
   - Best: 30-60 seconds of clear speech
   - You'll see a checkmark when uploaded

3. **Start Session**
   - Click "Start Session" to upload and begin
   - Or click "Skip" to use default avatar

### During the Call
1. **Green Phone Button** = Start call (enables camera/mic)
2. **Blue Mic Button** = Toggle voice recognition
3. **Red Phone Button** = End call
4. **Chat Icon** (sidebar) = View conversation history

## ⚙️ Browser Permissions

When you start the call, your browser will ask for:
- ✅ Camera access
- ✅ Microphone access

**Click "Allow"** for both!

## 🔍 Troubleshooting

### "Cannot access camera/microphone"
- Check browser permissions (click lock icon in address bar)
- Close other apps using camera (Zoom, Teams, etc.)
- Try Chrome or Edge browser

### "Connection failed"
- Make sure Python app is running
- Check if port 5000 is free
- Try: http://127.0.0.1:5000 instead

### "AI not responding"
- Verify Gemini API key in `.env` file
- Check internet connection
- Look at terminal for error messages

### Voice cloning not working
- App will automatically use default voice (gTTS)
- To enable: Add ElevenLabs API key to `.env`

## 📝 Tips for Best Experience

### Voice Sample Tips
- Use 30-60 seconds of audio
- Clear, noise-free recording
- Natural speaking pace
- Multiple sentences work best

### Avatar Image Tips
- Front-facing photo
- Good lighting
- Clear facial features
- PNG or JPG format

### Conversation Tips
- Speak naturally and clearly
- Wait for AI to finish responding
- Use the chat panel to review history
- Be patient during first response (AI is thinking!)

## 🎨 Customization

### Change AI Personality
Edit `app.py`, find `emotional_context` variable:
```python
emotional_context = """
You are [describe personality here]...
"""
```

### Change Colors/Theme
Edit `static/styles.css` - look for:
- `background: linear-gradient(...)` for colors
- `.welcome-screen` for welcome page style
- `.chat-panel` for chat styling

## 📊 What Each File Does

- `app.py` - Main server (handles AI, uploads, voice)
- `index_enhanced.html` - New UI with upload feature
- `static/app.js` - Frontend logic (camera, mic, chat)
- `static/styles.css` - Beautiful styling
- `.env` - Your API keys (keep secret!)
- `uploads/` - Stores uploaded files (auto-created)

## 🆘 Getting Help

1. Read error messages in:
   - Browser console (press F12)
   - Terminal/command prompt

2. Common fixes:
   - Restart the Python app
   - Clear browser cache
   - Try incognito/private mode
   - Update browser to latest version

## 🎉 You're Ready!

Your Memory AI Assistant is now set up. Enjoy creating meaningful conversations with your emotionally intelligent AI companion!

---

**Need more details?** Check `README_ENHANCED.md` for complete documentation.
