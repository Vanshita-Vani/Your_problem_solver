# Test Scripts - Simple Testing Guide

These are **simple, standalone scripts** to test each feature independently.

---

## 🎤 Test 1: Voice Cloning

**File:** `test_voice_clone.py`

**What it does:**
1. Takes your audio file
2. Sends it to ElevenLabs
3. Clones your voice
4. Generates a test audio with your cloned voice
5. Saves it as `test_cloned_voice_output.mp3`

**How to run:**
```bash
python test_voice_clone.py
```

**What you'll see:**
- ✅ If successful: You'll get a file `test_cloned_voice_output.mp3` - play it to hear your cloned voice!
- ❌ If failed: You'll see the exact error from ElevenLabs

**Requirements:**
- Audio file (MP3, WAV, M4A, or WebM)
- ElevenLabs API key in `.env` file

---

## 🎬 Test 2: Avatar Creation

**File:** `test_avatar_creation.py`

**What it does:**
1. Takes an image (or uses default)
2. Sends it to D-ID
3. Creates a talking avatar video
4. Downloads it as `test_avatar_output.mp4`

**How to run:**
```bash
python test_avatar_creation.py
```

**What you'll see:**
- ✅ If successful: You'll get a file `test_avatar_output.mp4` - play it to see the talking avatar!
- ❌ If failed: You'll see the exact error from D-ID

**IMPORTANT NOTE:**
- D-ID **does NOT accept base64 images**
- You must use a **publicly accessible URL** (ending with .jpg, .jpeg, or .png)
- For testing, the script uses D-ID's default avatar
- To use YOUR image: Upload it to Imgur/Cloudinary/S3 first and get the public URL

**Requirements:**
- D-ID API key in `.env` file
- For custom avatar: Public image URL

---

## 📋 Why These Scripts?

**Problems with the main app:**
1. ❌ Too complex - hard to debug
2. ❌ Generates new video for EVERY message (expensive!)
3. ❌ Voice cloning not working - can't tell why
4. ❌ Avatar not showing - too many moving parts

**These test scripts:**
1. ✅ Simple - one feature at a time
2. ✅ Clear output - you see exactly what's happening
3. ✅ Saves files - you can verify the results
4. ✅ Shows exact errors - easy to debug

---

## 🎯 Recommended Workflow

### Step 1: Test Voice Cloning
```bash
python test_voice_clone.py
```
- Upload your audio file
- Check if `test_cloned_voice_output.mp3` sounds like you
- If YES: Voice cloning works! ✅
- If NO: Check the error message

### Step 2: Test Avatar Creation
```bash
python test_avatar_creation.py
```
- Press Enter to use default avatar
- Check if `test_avatar_output.mp4` is created
- If YES: Avatar creation works! ✅
- If NO: Check the error message

### Step 3: Fix Main App
Once both tests pass, we know:
- ✅ APIs are working
- ✅ API keys are correct
- ✅ The problem is in the main app logic

Then we can simplify the main app!

---

## 🚨 Common Issues

### Voice Cloning Fails
- **Check:** Is your audio file at least 1 second long?
- **Check:** Is the file size under 10MB?
- **Check:** Is your ElevenLabs API key correct?

### Avatar Creation Fails
- **Error 400:** Image URL format is wrong (must end with .jpg/.jpeg/.png)
- **Error 401:** D-ID API key is incorrect
- **Error 429:** You've hit the rate limit (wait a bit)

---

## 💡 Next Steps

After testing:

1. **If voice cloning works:** We can integrate it properly into the main app
2. **If avatar works:** We need to set up image hosting (S3/Cloudinary)
3. **Simplify main app:** Remove the messy code, make it cleaner

The main app should:
- Generate avatar video ONCE per session (not per message!)
- Reuse the same avatar for all responses
- Only regenerate if user uploads new image
