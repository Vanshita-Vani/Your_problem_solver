# 🧪 Testing Guide - Memory AI Assistant

## Pre-Testing Checklist

### ✅ Before You Start
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Gemini API key added to `.env` file
- [ ] Webcam and microphone available
- [ ] Modern browser (Chrome/Edge recommended)

---

## 🎯 Test Scenarios

### Test 1: Basic Setup
**Goal**: Verify the application starts correctly

**Steps**:
1. Open terminal in project folder
2. Run: `python app.py`
3. Check terminal output

**Expected Output**:
```
✓ Google Gemini 2.5 Flash initialized successfully (FREE)
✓ Vision capabilities enabled - AI can see your video!
⚠ Warning: ElevenLabs API key not set. Using default TTS.
⚠ Warning: D-ID API key not set. Using default avatar.
Starting AI Video Call Assistant...
Server running at http://0.0.0.0:5000
```

**✅ Pass Criteria**: Server starts without errors

---

### Test 2: Welcome Screen
**Goal**: Verify welcome screen loads and file uploads work

**Steps**:
1. Open browser: http://localhost:5000
2. Verify welcome screen appears with purple gradient
3. Click "Upload Avatar Image"
4. Select an image file (JPG/PNG)
5. Verify checkmark appears
6. Click "Upload Voice Sample"
7. Select an audio file (MP3/WAV)
8. Verify checkmark appears

**Expected Result**:
- Welcome screen displays correctly
- Upload boxes change color when file selected
- File names show with checkmark (✓)

**✅ Pass Criteria**: Both files can be selected

---

### Test 3: File Upload to Server
**Goal**: Verify files are uploaded and processed

**Steps**:
1. After selecting files, click "Start Session"
2. Watch terminal output
3. Check `uploads/` folder

**Expected Terminal Output**:
```
✓ Avatar image saved: uploads/session_xxx_avatar_xxx.jpg
✓ Voice sample saved: uploads/session_xxx_voice_xxx.mp3
```

**Expected Files**:
- `uploads/` folder created
- Image file saved
- Audio file saved

**✅ Pass Criteria**: Files uploaded successfully, terminal shows confirmation

---

### Test 4: Skip Upload (Default Mode)
**Goal**: Verify app works without uploads

**Steps**:
1. Refresh page
2. Click "Skip and use default avatar"
3. Verify welcome screen disappears
4. Main interface appears

**Expected Result**:
- Welcome screen fades out
- Video call interface visible
- No errors in console

**✅ Pass Criteria**: App loads without uploads

---

### Test 5: Camera & Microphone Access
**Goal**: Verify media device access

**Steps**:
1. Click green phone button (Start Call)
2. Browser asks for permissions
3. Click "Allow" for both camera and microphone
4. Verify your video appears

**Expected Result**:
- Permission prompt appears
- Your video shows in main window
- Status changes to "Connected"
- Green button disabled, red button enabled
- Blue mic button enabled

**✅ Pass Criteria**: Video stream starts, controls update

---

### Test 6: Speech Recognition
**Goal**: Verify voice input works

**Steps**:
1. With call active, click blue mic button
2. Verify button turns green and pulses
3. Status shows "🎤 Listening..."
4. Say: "Hello, how are you?"
5. Wait for response

**Expected Result**:
- Mic button animates (green pulse)
- Status indicator shows listening
- Your message appears in chat (if panel open)
- AI responds with text and voice
- AI message appears in chat

**Expected AI Response Style**:
- Warm and empathetic
- Natural conversation
- 2-4 sentences
- Emotionally aware

**✅ Pass Criteria**: Speech recognized, AI responds with voice and text

---

### Test 7: Chat History
**Goal**: Verify conversation tracking

**Steps**:
1. Click chat icon (💬) in sidebar
2. Chat panel slides in from right
3. Verify messages are displayed
4. Have multiple exchanges
5. Verify history accumulates

**Expected Result**:
- Chat panel opens smoothly
- User messages on right (purple gradient)
- AI messages on left (dark gray)
- Messages animate in
- Scroll works for long conversations

**✅ Pass Criteria**: Chat history displays correctly

---

### Test 8: Vision Analysis (Optional)
**Goal**: Test AI's ability to see through camera

**Steps**:
1. Hold an object in front of camera
2. Say: "What do you see?"
3. Wait for AI response

**Expected Result**:
- Terminal shows: "🎥 Analyzing video frame..."
- AI describes what it sees
- Response is relevant to the object

**✅ Pass Criteria**: AI correctly identifies objects

---

### Test 9: Emotional Intelligence
**Goal**: Verify empathetic responses

**Test Phrases**:
1. "I'm feeling sad today"
2. "I just got great news!"
3. "I'm worried about something"
4. "Tell me about yourself"

**Expected AI Behavior**:
- Responds with empathy to sadness
- Shows excitement for good news
- Offers comfort for worries
- Describes itself warmly

**✅ Pass Criteria**: AI shows emotional awareness

---

### Test 10: Voice Cloning (With ElevenLabs API)
**Goal**: Test custom voice generation

**Prerequisites**: ElevenLabs API key in `.env`

**Steps**:
1. Refresh page
2. Upload voice sample (30-60 seconds)
3. Click "Start Session"
4. Wait for voice cloning (check terminal)
5. Start call and have conversation

**Expected Terminal Output**:
```
✓ Voice sample saved: uploads/session_xxx_voice_xxx.mp3
✓ Voice cloned successfully: voice_id_here
```

**Expected Result**:
- AI speaks in uploaded voice
- Voice quality is good
- Matches original sample

**✅ Pass Criteria**: AI uses cloned voice

---

### Test 11: End Call
**Goal**: Verify cleanup works

**Steps**:
1. Click red phone button (End Call)
2. Verify video stops
3. Verify mic stops (if active)
4. Check button states

**Expected Result**:
- Video stream stops
- Camera light turns off
- Status shows "Disconnected"
- Green button enabled
- Red/blue buttons disabled

**✅ Pass Criteria**: Clean shutdown, no errors

---

### Test 12: Reconnection
**Goal**: Test multiple sessions

**Steps**:
1. End call (if active)
2. Start new call
3. Have conversation
4. Verify everything works

**Expected Result**:
- New session starts cleanly
- Previous conversation not visible
- All features work

**✅ Pass Criteria**: Multiple sessions work independently

---

## 🐛 Common Issues & Solutions

### Issue: "Cannot access camera"
**Solutions**:
- Check browser permissions (click lock icon in address bar)
- Close other apps using camera (Zoom, Teams, etc.)
- Try different browser
- Restart browser

### Issue: "Speech recognition not working"
**Solutions**:
- Check microphone permissions
- Verify mic is not muted
- Try Chrome browser (best support)
- Check mic in system settings

### Issue: "AI not responding"
**Solutions**:
- Verify Gemini API key in `.env`
- Check internet connection
- Look at terminal for errors
- Try refreshing page

### Issue: "Upload failed"
**Solutions**:
- Check file size (<16MB)
- Verify file format (JPG, PNG, MP3, WAV)
- Check `uploads/` folder permissions
- Look at terminal for error details

### Issue: "Voice cloning not working"
**Solutions**:
- Verify ElevenLabs API key
- Check API quota (free tier limits)
- App will fallback to gTTS automatically
- Check terminal for API errors

### Issue: "Connection timeout"
**Solutions**:
- Check if server is running
- Verify port 5000 is not blocked
- Try http://127.0.0.1:5000 instead
- Disable VPN temporarily

---

## 📊 Performance Testing

### Load Test
**Goal**: Verify app handles continuous use

**Steps**:
1. Start call
2. Have 10+ minute conversation
3. Monitor memory usage
4. Check for slowdowns

**Expected**:
- No memory leaks
- Consistent response times
- No crashes

### Stress Test
**Goal**: Test rapid interactions

**Steps**:
1. Start call
2. Speak rapidly (multiple messages)
3. Toggle mic on/off quickly
4. Open/close chat panel repeatedly

**Expected**:
- App remains responsive
- No errors in console
- Messages queue properly

---

## 🔍 Browser Console Testing

### Check for Errors
**Steps**:
1. Press F12 to open DevTools
2. Go to Console tab
3. Look for red errors

**Expected**:
- No critical errors
- Only info/log messages
- Socket.IO connection successful

### Network Monitoring
**Steps**:
1. Open DevTools → Network tab
2. Filter: WS (WebSocket)
3. Monitor Socket.IO traffic

**Expected**:
- WebSocket connection established
- Messages flowing both ways
- No failed requests

---

## 📝 Test Results Template

```
Date: ___________
Tester: ___________
Browser: ___________
OS: ___________

Test Results:
[ ] Test 1: Basic Setup
[ ] Test 2: Welcome Screen
[ ] Test 3: File Upload
[ ] Test 4: Skip Upload
[ ] Test 5: Camera/Mic Access
[ ] Test 6: Speech Recognition
[ ] Test 7: Chat History
[ ] Test 8: Vision Analysis
[ ] Test 9: Emotional Intelligence
[ ] Test 10: Voice Cloning
[ ] Test 11: End Call
[ ] Test 12: Reconnection

Issues Found:
1. ___________
2. ___________

Notes:
___________
```

---

## 🎯 Acceptance Criteria

### Minimum Viable Product (MVP)
- ✅ App starts without errors
- ✅ Welcome screen displays
- ✅ Can skip uploads
- ✅ Camera/mic access works
- ✅ Speech recognition works
- ✅ AI responds with text + voice
- ✅ Chat history displays
- ✅ Call can be ended cleanly

### Enhanced Features
- ✅ File uploads work
- ✅ Emotional responses
- ✅ Vision analysis works
- ✅ Voice cloning (with API key)
- ✅ Beautiful UI/animations

### Production Ready
- ✅ All MVP + Enhanced features
- ✅ No console errors
- ✅ Handles edge cases
- ✅ Performance is good
- ✅ Documentation complete

---

## 🚀 Next Steps After Testing

### If All Tests Pass ✅
1. Customize AI personality
2. Add ElevenLabs API key
3. Try D-ID integration
4. Share with friends
5. Consider deployment

### If Tests Fail ❌
1. Note which test failed
2. Check error messages
3. Review troubleshooting section
4. Check documentation
5. Verify setup steps

---

## 📞 Support Checklist

Before asking for help:
- [ ] Checked all error messages
- [ ] Reviewed troubleshooting section
- [ ] Verified API keys are correct
- [ ] Tried different browser
- [ ] Restarted server
- [ ] Checked documentation

Include when reporting issues:
- Which test failed
- Error messages (terminal + console)
- Browser and OS version
- Steps to reproduce
- Screenshots if relevant

---

**Happy Testing! 🎉**

Your Memory AI Assistant should pass all tests and provide an amazing emotionally intelligent conversation experience!
