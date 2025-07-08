# AI Service Deployment Guide

## 🤖 AI Service Configuration for Production

The MoodSync app uses an AI service for generating personalized insights, motivational messages, and habit suggestions. Here's how to set it up for production deployment:

## Current Status: ⚠️ AI Service Not Deployed

Your main app is live at `https://moodify-wmcd.onrender.com`, but the AI service is configured for local development only (`http://127.0.0.1:5001`). This means AI features will use fallback responses.

## 🔧 Solution Options:

### Option 1: Deploy AI Service to Render (Recommended)

1. **Create a new Render Web Service** for the AI service:
   - Repository: Same repo, but point to `ai_service/` directory
   - Build Command: `pip install -r ai_service/requirements.txt`
   - Start Command: `python ai_service/app.py`
   - Environment Variables:
     ```
     OPENAI_API_KEY=your-openai-api-key
     PORT=10000
     ```

2. **Update main app environment variables**:
   ```
   AI_SERVICE_URL=https://your-ai-service-name.onrender.com
   AI_FALLBACK_ENABLED=True
   ```

### Option 2: Use External AI Service

Deploy the AI service to another platform:
- Heroku: `git subtree push --prefix ai_service heroku main`
- Railway: Point to `ai_service/` subdirectory
- Fly.io: Deploy with `fly deploy` from `ai_service/` directory

### Option 3: Direct OpenAI Integration (Simplified)

Skip the separate AI service and integrate OpenAI directly:
- Set `OPENAI_API_KEY` in main app environment
- AI features will use simplified, direct OpenAI calls
- Fallback responses when API is unavailable

## 🚀 Quick Deploy: AI Service to Render

### Step 1: Create AI Service Deployment

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Create New → Web Service
3. Connect your GitHub repository
4. Configure:
   - **Name**: `moodsync-ai-service`
   - **Root Directory**: `ai_service`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### Step 2: Set Environment Variables

In the AI service settings:
```
GEMINI_API_KEY=your-actual-gemini-api-key
PORT=10000
FLASK_ENV=production
```

**Note**: The AI service uses Google Gemini API (not OpenAI). Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### Step 3: Update Main App Settings

In your main app's environment variables:
```
AI_SERVICE_URL=https://moodsync-ai-service.onrender.com
AI_FALLBACK_ENABLED=True
OPENAI_API_KEY=your-openai-api-key  # backup
```

## 📋 Environment Variables Summary

### Main App (moodify-wmcd.onrender.com):
```bash
# Required
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=moodify-wmcd.onrender.com
CORS_ALLOWED_ORIGINS=https://moodify-wmcd.onrender.com

# AI Configuration
AI_SERVICE_URL=https://moodsync-ai-service.onrender.com
AI_FALLBACK_ENABLED=True
OPENAI_API_KEY=your-openai-api-key  # Optional fallback
```

### AI Service (separate deployment):
```bash
# Required
OPENAI_API_KEY=your-openai-api-key
PORT=10000
FLASK_ENV=production
```

## 🧪 Testing AI Features

Once deployed, test these endpoints:

### 1. Motivational Messages
```
GET https://moodify-wmcd.onrender.com/api/suggestions/motivation/
Authorization: Bearer YOUR_JWT_TOKEN
```

### 2. Habit Suggestions
```
GET https://moodify-wmcd.onrender.com/api/suggestions/habits/
Authorization: Bearer YOUR_JWT_TOKEN
```

### 3. Mood Insights
```
GET https://moodify-wmcd.onrender.com/api/insights/
Authorization: Bearer YOUR_JWT_TOKEN
```

## 🔄 Current Fallback Behavior

Until AI service is deployed, the app will:
- ✅ Provide time-aware motivational messages
- ✅ Show basic habit suggestions
- ✅ Display mood trends and statistics
- ⚠️ Mark responses as "fallback" (not AI-generated)
- ✅ Continue all other functionality normally

## 📊 Monitoring

Check AI service status:
- Main app logs: Look for "AI service error" messages
- AI service logs: Monitor for OpenAI API errors
- Response field: `"personalized_with_ai": false` indicates fallback mode

## 💡 Next Steps

1. **Immediate**: App works with fallback responses
2. **Short-term**: Deploy AI service to Render (15-30 minutes)
3. **Long-term**: Monitor usage and optimize AI responses

The app is fully functional without the AI service - it just provides more generic (but still time-aware and context-appropriate) responses!
