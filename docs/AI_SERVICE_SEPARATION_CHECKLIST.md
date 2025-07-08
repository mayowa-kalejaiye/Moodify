# AI Service Separation Checklist

## ✅ Before Moving AI Service

### Backup Current State
- [ ] Ensure current code is committed and pushed
- [ ] Note down current AI service configuration
- [ ] Copy Gemini API key from ai_service/.env

### Prepare Main App
- [ ] Verify AI_SERVICE_URL environment variable is configurable
- [ ] Test app works with AI service unavailable (fallback mode)
- [ ] Update documentation about AI service separation

## 📦 Moving the AI Service

### What to Copy to New Repository
From `ai_service/` folder:
- [ ] `app.py` - Main Flask application
- [ ] `requirements.txt` - Python dependencies  
- [ ] `.env.example` - Environment template (create new one)
- [ ] `README.md` - Create AI service specific readme

### Don't Copy
- [ ] `.env` - Create fresh in new repo (security)
- [ ] `__pycache__/` - Will be regenerated

## 🚀 Setting Up New Repository

### Repository Setup
- [ ] Create new GitHub repository (e.g., `moodsync-ai-service`)
- [ ] Clone to new location
- [ ] Copy files from `ai_service/` folder
- [ ] Create new `.env` with your Gemini API key
- [ ] Test locally: `python app.py`

### Environment Configuration
Add to new `.env`:
```bash
GEMINI_API_KEY=AIzaSyDQEKxNXiV5WUEI_xiJ5nZUL8K3rqPjtqg
PORT=5000
FLASK_ENV=development
```

## 🔧 Deploy to Render

### Render Configuration
- [ ] Create new Web Service in Render
- [ ] Connect to new AI service repository
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `python app.py`
- [ ] Add environment variables:
  - `GEMINI_API_KEY=AIzaSyDQEKxNXiV5WUEI_xiJ5nZUL8K3rqPjtqg`
  - `PORT=10000`
  - `FLASK_ENV=production`

### Get Deployed URL
- [ ] Note the deployed URL (e.g., `https://moodsync-ai-service.onrender.com`)
- [ ] Test AI service endpoints work

## 🔗 Update Main App

### Environment Configuration  
In main app's Render dashboard:
- [ ] Update `AI_SERVICE_URL=https://your-ai-service.onrender.com`
- [ ] Redeploy main app

### Testing
- [ ] Test `/api/suggestions/motivation/` returns AI responses
- [ ] Test `/api/suggestions/habits/` works
- [ ] Test `/api/insights/` provides personalized insights
- [ ] Check logs for `'personalized_with_ai': true`

## 🧹 Cleanup Original Repository

### After Successful Deployment
- [ ] Remove `ai_service/` folder from main repository
- [ ] Update `.gitignore` to remove ai_service references
- [ ] Commit and push cleanup changes
- [ ] Update documentation with new architecture

### Final Verification
- [ ] Main app works with deployed AI service
- [ ] AI features are functional
- [ ] Fallback works if AI service is down
- [ ] Documentation is updated

## 🚨 Rollback Plan

If something goes wrong:
- [ ] Revert `AI_SERVICE_URL` to `http://127.0.0.1:5001`
- [ ] Run AI service locally
- [ ] Investigate issues before trying again

This ensures your main app stays functional during the transition!
