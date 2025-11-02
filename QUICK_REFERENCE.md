# ⚡ Quick Reference Card - Memory AI Assistant

## 🚀 Start in 30 Seconds

```bash
pip install -r requirements.txt
# Add GEMINI_API_KEY to .env
python app.py
# Open: http://localhost:5000
```

---

## 🎮 Controls

| Button | Icon | Action |
|--------|------|--------|
| **Start Call** | 🟢 Green Circle | Enable camera/mic |
| **Microphone** | 🔵 Blue Circle | Toggle voice input |
| **End Call** | 🔴 Red Circle | Stop call |
| **Chat** | 💬 Sidebar | View history |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main server |
| `index_enhanced.html` | New UI |
| `static/app.js` | Frontend logic |
| `static/styles.css` | Styling |
| `.env` | API keys |

---

## 🔑 API Keys

### Required
```env
GEMINI_API_KEY=your_key_here
```
Get FREE at: https://makersuite.google.com/app/apikey

### Optional
```env
ELEVENLABS_API_KEY=your_key_here  # Voice cloning
DID_API_KEY=your_key_here          # Avatar generation
```

---

## 🎯 Common Tasks

### Change AI Personality
**File**: `app.py` (line 80)
```python
emotional_context = """
Your custom personality here...
"""
```

### Change Colors
**File**: `static/styles.css`
- Search: `#667eea` and `#764ba2`
- Replace with your colors

### Change Language
**File**: `static/app.js` (line 551)
```javascript
recognition.lang = 'en-US';  // Change here
```

---

## 🐛 Quick Fixes

### Camera Not Working
```
✓ Click "Allow" in browser
✓ Close other apps using camera
✓ Try Chrome browser
```

### AI Not Responding
```
✓ Check GEMINI_API_KEY in .env
✓ Check internet connection
✓ Look at terminal for errors
```

### Upload Failed
```
✓ File size < 16MB
✓ Use JPG, PNG, MP3, WAV
✓ Check uploads/ folder exists
```

---

## 📊 File Formats

### Images
✅ PNG, JPG, JPEG, GIF, WEBP

### Audio
✅ MP3, WAV, OGG, M4A, WEBM

### Size Limit
⚠️ 16MB maximum

---

## 🎨 UI Elements

### Status Colors
- **Gray** = Ready
- **Blue** = Connected
- **Green** = Listening
- **Red** = Error

### Button States
- **Enabled** = Full color
- **Disabled** = Grayed out
- **Active** = Pulsing animation

---

## 📡 Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Main page |
| GET | `/static/*` | CSS/JS files |
| POST | `/upload` | File upload |

---

## 🔌 Socket Events

### Client → Server
- `connect` - Connection established
- `user_message` - Send message
- `video_frame` - Send video

### Server → Client
- `ai_response` - AI reply
- `video_processed` - Video echo
- `error` - Error message

---

## 📚 Documentation

| File | What's Inside |
|------|---------------|
| `START_HERE.md` | ⭐ Begin here |
| `SETUP_GUIDE.md` | Installation |
| `README_ENHANCED.md` | All features |
| `TESTING_GUIDE.md` | How to test |
| `API_REFERENCE.md` | Technical API |
| `ARCHITECTURE.md` | System design |

---

## 💡 Pro Tips

### Better Voice Cloning
- Use 30-60 seconds of audio
- Clear, noise-free recording
- Natural speaking pace
- Multiple sentences

### Better Conversations
- Speak clearly
- Wait for AI to finish
- Use natural language
- Be patient first time

### Performance
- Close unused tabs
- Use wired internet
- Good lighting for camera
- Quiet environment

---

## 🎯 Testing Checklist

Quick test sequence:
```
[ ] Server starts
[ ] Page loads
[ ] Upload works (or skip)
[ ] Camera enables
[ ] Mic recognizes speech
[ ] AI responds
[ ] Chat shows history
[ ] Call ends cleanly
```

---

## 🔢 Port Numbers

| Service | Port |
|---------|------|
| Flask Server | 5000 |
| Alternative | 127.0.0.1:5000 |

---

## 📞 Emergency Commands

### Restart Server
```bash
Ctrl+C  # Stop
python app.py  # Start
```

### Clear Browser
```
Ctrl+Shift+Delete  # Clear cache
Ctrl+Shift+N       # Incognito mode
F5                 # Refresh
```

### Check Logs
```bash
# Terminal shows server logs
# Browser F12 → Console shows client logs
```

---

## 🎨 Color Palette

```css
Primary: #667eea → #764ba2 (Purple gradient)
Success: #27ae60 (Green)
Danger: #d31500 (Red)
Info: #3498db (Blue)
Background: #1a1a1a (Dark)
```

---

## 📈 Performance Targets

| Metric | Target |
|--------|--------|
| Response Time | 1-3 sec |
| Voice Generation | 2-5 sec |
| File Upload | <5 sec |
| Memory Usage | ~200MB |

---

## 🔐 Security Checklist

```
✓ API keys in .env (not in code)
✓ File validation enabled
✓ Size limits enforced
✓ Secure filenames
✓ Session isolation
```

---

## 🌐 Browser Support

| Browser | Status |
|---------|--------|
| Chrome | ✅ Best |
| Edge | ✅ Good |
| Firefox | ✅ Good |
| Safari | ⚠️ Limited |

---

## 📱 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F12 | Open DevTools |
| F5 | Refresh page |
| Ctrl+Shift+I | Inspect element |
| Esc | Close panels |

---

## 🎯 Success Indicators

### Server Running ✅
```
Server running at http://0.0.0.0:5000
✓ Google Gemini initialized
```

### Connection Good ✅
```
Status: Connected
Socket ID: abc123
Transport: polling
```

### AI Working ✅
```
✅ Received AI response
✓ Vision analysis complete
```

---

## 🔄 Update Workflow

1. Stop server (Ctrl+C)
2. Make changes
3. Save files
4. Restart server
5. Refresh browser (F5)

---

## 📦 Dependencies

### Core
- flask
- flask-socketio
- google-generativeai
- eventlet

### Optional
- requests (APIs)
- Pillow (images)
- opencv-python (video)

---

## 🎓 Learn More

### Beginner
→ START_HERE.md
→ SETUP_GUIDE.md

### Intermediate
→ README_ENHANCED.md
→ TESTING_GUIDE.md

### Advanced
→ ARCHITECTURE.md
→ API_REFERENCE.md

---

## ⚡ One-Liners

### Install Everything
```bash
pip install -r requirements.txt
```

### Run Server
```bash
python app.py
```

### Test Upload
```bash
curl -F "session_id=test" -F "avatar_image=@image.jpg" http://localhost:5000/upload
```

### Check Python Version
```bash
python --version  # Need 3.8+
```

---

## 🎉 Quick Start Checklist

```
1. [ ] pip install -r requirements.txt
2. [ ] Add GEMINI_API_KEY to .env
3. [ ] python app.py
4. [ ] Open http://localhost:5000
5. [ ] Upload files or skip
6. [ ] Click green button
7. [ ] Click blue mic button
8. [ ] Say "Hello!"
9. [ ] Enjoy! 🎊
```

---

**Print this page for quick reference! 📄**

*Last Updated: 2025-11-02*
