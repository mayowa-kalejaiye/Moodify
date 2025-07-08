# MoodSync Deployment Guide

## Quick Fix for Current Render Deployment Issue

The "Invalid HTTP_HOST header" errors have been fixed in the latest commit. The deployment should now work correctly.

### What was fixed:
- ✅ Added `moodify-wmcd.onrender.com` to `ALLOWED_HOSTS`
- ✅ Added `.onrender.com` wildcard for Render subdomains  
- ✅ Fixed CORS settings for production
- ✅ Added proper environment variable handling

### Environment Variables for Render

Set these in your Render dashboard under "Environment":

```bash
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=moodify-wmcd.onrender.com,.onrender.com
CORS_ALLOWED_ORIGINS=https://moodify-wmcd.onrender.com
```

## Full Deployment Guide

### 1. Render Web Service Deployment

1. **Connect Repository**: Link your GitHub repository to Render
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `gunicorn mood_tracker.wsgi --log-file -`
4. **Environment Variables**: Set the following in Render dashboard:
   - `DJANGO_SECRET_KEY`: Generate a secure secret key
   - `DEBUG`: Set to `False`
   - `ALLOWED_HOSTS`: Your Render domain
   - `DATABASE_URL`: Automatically provided by Render PostgreSQL
   - `CORS_ALLOWED_ORIGINS`: Your frontend domains

### 2. Database Setup

Render automatically provides PostgreSQL. The `DATABASE_URL` is set automatically.

### 3. Static Files

Static files are handled by WhiteNoise middleware (already configured).

### 4. Health Checks

The app includes a health check endpoint at `/api/health/` that Render uses for monitoring.

### 5. SSL/HTTPS

Render provides HTTPS automatically. The production settings are configured for secure cookies and headers.

## Local Development

1. Copy `.env.example` to `.env`
2. Customize the values in `.env`
3. Run: `python manage.py runserver`

## Management Commands

Use the behavior engine management command:

```bash
# Initialize user profiles
python manage.py behavior_engine --init-profiles

# Update streaks
python manage.py behavior_engine --update-streaks

# Settle challenges
python manage.py behavior_engine --settle-challenges

# Generate demo data
python manage.py behavior_engine --generate-demo-data
```

## API Documentation

Once deployed, API documentation is available at:
- Swagger UI: `https://your-domain.com/swagger/`
- ReDoc: `https://your-domain.com/redoc/`

## Troubleshooting

### Common Issues:

1. **Invalid HTTP_HOST header**: Make sure your domain is in `ALLOWED_HOSTS`
2. **CORS errors**: Update `CORS_ALLOWED_ORIGINS` with your frontend domain
3. **Static files not loading**: Ensure WhiteNoise is properly configured
4. **Database errors**: Check if migrations need to be run

### Logs:
Check Render logs for detailed error information.
