# 🎬 Talking Avatar Setup Guide

## What You'll Get

Your uploaded avatar image will **come alive and talk** in the video window! Instead of seeing your webcam, you'll see your avatar speaking with lip-sync.

---

## ✅ What's Already Done

I've implemented:
1. ✅ D-ID avatar video generation
2. ✅ Avatar replaces webcam video
3. ✅ Lip-sync with AI voice
4. ✅ Continuous conversation support
5. ✅ Auto-switch between avatar and webcam

---

## 🚀 How to Use

### Step 1: Restart Your Server

```bash
# Stop the server (Ctrl+C)
# Then restart:
python app.py
```

### Step 2: Upload Your Avatar

1. Open http://localhost:5000
2. Click "Upload Avatar Image"
3. Select a clear photo of yourself (or any person)
4. Optionally upload voice sample
5. Click "Start Session"

### Step 3: Start Talking

1. Click the green phone button (Start Call)
2. Click the blue mic button
3. Say something like "Hello, how are you?"
4. **Watch the magic!** 🎬

---

## 🎭 How It Works

```
You speak → AI responds → D-ID generates video → Avatar talks!
```

### Behind the Scenes:
1. Your speech is recognized
2. AI generates response text
3. D-ID API creates talking avatar video
4. Video replaces your webcam
5. Avatar speaks with perfect lip-sync
6. After speaking, webcam returns

---

## ⚙️ Technical Details

### D-ID API Integration

**What happens when you speak:**
1. AI generates response text
2. Server calls D-ID API with:
   - Your uploaded avatar image
   - AI response text
   - Voice settings
3. D-ID generates video (takes ~5-10 seconds)
4. Video URL sent to browser
5. Browser plays avatar video

### Video Flow:
```
┌─────────────┐
│  Your       │
│  Webcam     │ ← Shows by default
└──────┬──────┘
       │
       ▼ (when AI responds)
┌─────────────┐
│  Avatar     │
│  Video      │ ← Talking avatar
└──────┬──────┘
       │
       ▼ (when done)
┌─────────────┐
│  Your       │
│  Webcam     │ ← Returns to webcam
└─────────────┘
```

---

## 🎨 Customization Options

### Change Avatar Voice

Edit `app.py` line 220:
```python
"voice_id": "en-US-JennyNeural"  # Change to other voices
```

**Available voices:**
- `en-US-JennyNeural` (Female, friendly)
- `en-US-GuyNeural` (Male, professional)
- `en-US-AriaNeural` (Female, cheerful)
- `en-GB-SoniaNeural` (British female)
- `en-AU-NatashaNeural` (Australian female)

### Keep Avatar Visible

To keep avatar on screen (not switch back to webcam), edit `static/app.js` line 222:

```javascript
// Comment out these lines:
// videoContainer.removeChild(avatarVideoElement);
// localVideo.style.display = 'block';
// if (localStream) {
//     localVideo.srcObject = localStream;
// }
```

---

## 🐛 Troubleshooting

### "Avatar video not showing"

**Check:**
1. D-ID API key is correct in `.env`
2. Avatar image was uploaded
3. Check terminal for errors
4. D-ID API has credits

**Terminal should show:**
```
✓ D-ID API key found - Avatar generation enabled
🎬 Generating talking avatar video...
✓ Avatar video generation started: tlk_xxxxx
✓ Avatar video ready: https://...
```

### "Video generation takes too long"

- D-ID takes 5-15 seconds to generate video
- First response might be slower
- Check your internet connection
- Verify D-ID API quota

### "Avatar doesn't look right"

**Best avatar images:**
- Front-facing photo
- Clear facial features
- Good lighting
- Neutral background
- PNG or JPG format
- At least 512x512 pixels

---

## 💡 Pro Tips

### For Best Results:

1. **Image Quality**
   - Use high-resolution photos
   - Clear, well-lit faces
   - Front-facing angle
   - Minimal background clutter

2. **Conversation Flow**
   - Speak clearly
   - Wait for avatar to finish
   - Short sentences work best
   - Be patient on first response

3. **Performance**
   - Good internet connection
   - Close unnecessary tabs
   - Use Chrome or Edge browser

---

## 📊 D-ID API Limits

### Free Tier:
- 20 video credits
- Each video = 1 credit
- ~20 conversations

### Paid Plans:
- Lite: $5.90/month (15 min)
- Basic: $29/month (90 min)
- Advanced: Custom pricing

**Check your credits:** https://studio.d-id.com/

---

## 🎯 Expected Behavior

### Normal Flow:
```
1. You: "Hello!"
2. [5-10 sec wait - video generating]
3. Avatar appears and says: "Hello! How are you today?"
4. Avatar video ends
5. Webcam returns
6. You: "I'm great!"
7. [Repeat]
```

### What You'll See:
- ✅ Webcam initially
- ✅ "Generating avatar..." (in console)
- ✅ Avatar video plays
- ✅ Perfect lip-sync
- ✅ Natural expressions
- ✅ Webcam returns

---

## 🔧 Advanced Configuration

### Use Custom Voice with Avatar

If you uploaded a voice sample and have ElevenLabs:

Edit `app.py` line 232-236 to use custom audio:
```python
# Generate audio first
audio_url = generate_speech_url(ai_response, session_id)

# Then pass to D-ID
avatar_video_url = generate_avatar_video(session_id, ai_response, audio_url)
```

### Continuous Avatar Mode

To keep avatar always visible:

1. Hide webcam permanently
2. Queue avatar videos
3. Show avatar between responses

Edit `static/app.js` - remove webcam fallback logic.

---

## 📝 Testing Checklist

- [ ] Server starts without errors
- [ ] Avatar image uploads successfully
- [ ] D-ID API key recognized
- [ ] First conversation triggers video
- [ ] Avatar video plays smoothly
- [ ] Lip-sync is accurate
- [ ] Webcam returns after video
- [ ] Multiple conversations work

---

## 🎉 You're Ready!

Your avatar is now ready to come alive and have conversations with you!

**Quick Start:**
1. Restart server: `python app.py`
2. Open: http://localhost:5000
3. Upload avatar image
4. Start talking
5. Watch your avatar speak! 🎬

---

**Enjoy your talking avatar! 💝**
