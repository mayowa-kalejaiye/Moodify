# AI Service Deployment Quick Guide

## Step 1: Deploy AI Service to Render

1. **Run the deployment helper:**
   ```bash
   bash scripts/deploy_ai_service.sh
   ```

2. **Follow the steps shown:**
   - Go to Render dashboard
   - Create new Web Service
   - Connect to your GitHub repo
   - Set root directory: `ai_service`
   - Add environment variable: `GEMINI_API_KEY=your-actual-gemini-key`

3. **Note the deployed URL** (e.g., `https://moodsync-ai-service.onrender.com`)

## Step 2: Update Main App Configuration

1. **In Render dashboard for your main app**, add/update environment variable:
   ```
   AI_SERVICE_URL=https://moodsync-ai-service.onrender.com
   ```

2. **Redeploy** the main app (it will pick up the new AI service URL)

## Step 3: Test AI Features

Visit your main app and test these endpoints:
- `/api/suggestions/motivation/` - Should return AI-powered motivational messages
- `/api/suggestions/habits/` - Should return habit improvement suggestions  
- `/api/insights/` - Should return personalized mood insights

## Verification

Check the app logs for:
- `'personalized_with_ai': true` in API responses
- No "AI service unavailable" fallback messages

## Troubleshooting

If AI features aren't working:
1. Check AI service logs in Render dashboard
2. Verify `GEMINI_API_KEY` is set correctly
3. Ensure `AI_SERVICE_URL` points to deployed service
4. Check main app can reach AI service (no CORS issues)

## Fallback Behavior

If AI service is unavailable, the app will:
- Return generic motivational messages
- Provide basic habit suggestions
- Skip AI-powered insights
- Continue normal operation for all other features

This ensures the app remains fully functional even if AI service has issues.
