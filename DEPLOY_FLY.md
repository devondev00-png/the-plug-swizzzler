# 🚀 Deploy to Fly.io - The Plug Swizzler

## ✅ Fly.io is ACTUALLY FREE!

Fly.io offers a **generous free tier** with:
- ✅ **Free web hosting** (unlike Railway)
- ✅ **256MB RAM** per app
- ✅ **Shared CPU**
- ✅ **Global deployment**
- ✅ **No sleep mode** (always running)

## Quick Deploy Steps:

### 1. Install Fly CLI
- Download from: https://fly.io/docs/hands-on/install-flyctl/
- Or run: `iwr https://fly.io/install.ps1 -useb | iex` (PowerShell)

### 2. Sign Up
- Visit: https://fly.io
- Sign up with GitHub (free!)

### 3. Login to Fly
```bash
fly auth login
```

### 4. Deploy Your App
```bash
fly launch
```
- Choose **"the-plug-swizzler"** as app name
- Choose **"Yes"** to deploy now

### 5. Set Environment Variables
```bash
fly secrets set OPENAI_API_KEY="[YOUR_OPENAI_API_KEY_HERE]"
```

### 6. Deploy!
```bash
fly deploy
```

## 🎯 Your App Will Be Live At:
`https://the-plug-swizzler.fly.dev`

## ✅ What's Ready:
- ✅ `app.py` - Simple FastAPI app
- ✅ `requirements_minimal.txt` - Only FastAPI + Uvicorn
- ✅ `fly.toml` - Fly.io configuration
- ✅ `Dockerfile` - Container setup
- ✅ `Procfile` - Start command

## 📱 APK Status:
- **Location**: `C:\Users\dg24c\Call Script Gen\PlugSwizzler-APK.apk`
- **Status**: ✅ **READY TO INSTALL**

Fly.io is **ACTUALLY FREE** and much better than Render! 🚀