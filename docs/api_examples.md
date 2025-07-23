# 🌟 Moodify API Examples - Complete Guide

This document provides comprehensive examples of how to use all Moodify API endpoints for various operations.

## 🏠 Base URL
- **Local Development**: `http://localhost:8000`
- **Production**: `https://moodify-wmcd.onrender.com`

## 🔐 Authentication Overview

Moodify supports dual authentication:
- **Token Authentication**: `Authorization: Token your-token-here`
- **JWT Authentication**: `Authorization: Bearer your-jwt-access-token`

---

## 📚 API Endpoints Reference

### 🏠 **System Endpoints**

#### API Home
Get API information and available endpoints.

**Endpoint:** `GET /api/`

```bash
# Local Development
curl -X GET http://localhost:8000/api/

# Production
curl -X GET https://moodify-wmcd.onrender.com/api/
```

**Sample Response:**
```json
{
  "name": "MoodSync 2.0 API",
  "version": "2.0.0",
  "description": "AI-Powered Emotional Wellness Platform",
  "endpoints": {
    "authentication": {
      "login": {"url": "/api/login/", "method": "POST"},
      "register": {"url": "/api/register/", "method": "POST"},
      "logout": {"url": "/api/logout/", "method": "POST"}
    }
  }
}
```

#### Health Check
Check API system status.

**Endpoint:** `GET /api/health/`

```bash
curl -X GET http://localhost:8000/api/health/
```

---

## 🔐 **Authentication Endpoints**

### User Registration
Register a new user account with automatic profile creation.

**Endpoint:** `POST /api/register/`

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser123",
    "email": "newuser123@example.com", 
    "password": "StrongPass123!",
    "password_confirm": "StrongPass123!"
  }'
```

**Sample Response:**
```json
{
  "token": "abc123defg456...",
  "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 12,
    "username": "newuser123",
    "email": "newuser123@example.com"
  },
  "profile": {
    "id": 12,
    "age": null,
    "coin_balance": 0,
    "streak_count": 0,
    "clarity_score": 100
  }
}
```

### User Login
Log in with existing credentials.

**Endpoint:** `POST /api/login/`

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "existinguser",
    "password": "YourPassword123!"
  }'
```

### JWT Token Endpoints

#### Get JWT Token
**Endpoint:** `POST /api/token/`

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "youruser",
    "password": "yourpassword"
  }'
```

#### Refresh JWT Token
**Endpoint:** `POST /api/token/refresh/`

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your-refresh-token-here"
  }'
```

### User Logout
**Endpoint:** `POST /api/logout/`

```bash
curl -X POST http://localhost:8000/api/logout/ \
  -H "Authorization: Token your-token-here"
```

### Password Change
**Endpoint:** `POST /api/password-change/`

```bash
curl -X POST http://localhost:8000/api/password-change/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "CurrentPass123!",
    "new_password": "NewPass456!",
    "new_password_confirm": "NewPass456!"
  }'
```

---

## 👤 **User Profile Management**

### Get User Profile
**Endpoint:** `GET /api/profile/`

```bash
curl -X GET http://localhost:8000/api/profile/ \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "id": 5,
  "user": {
    "id": 5,
    "username": "existinguser",
    "email": "existing@example.com"
  },
  "age": 28,
  "coin_balance": 47,
  "streak_count": 12,
  "clarity_score": 95,
  "last_mood_log": "2025-07-22",
  "created_at": "2025-07-01T10:20:30.123456Z"
}
```

### Update User Profile
**Endpoint:** `PATCH /api/profile/`

```bash
curl -X PATCH http://localhost:8000/api/profile/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 29
  }'
```

---

## 📊 **Mood Tracking Endpoints**

### Create Mood Entry
Log a new mood entry with automatic rewards.

**Endpoint:** `POST /api/moods/`

```bash
curl -X POST http://localhost:8000/api/moods/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "mood": "Contemplating",
    "rating": 7,
    "notes": "Late night coding",
    "activities": "work,coding"
  }'
```

**Sample Response:**
```json
{
  "id": 45,
  "user": 5,
  "mood": "Contemplating",
  "rating": 7,
  "notes": "Late night coding",
  "activities": "work,coding",
  "sentiment": 0.6,
  "created_at": "2025-07-24T01:30:45.123456Z",
  "username": "newuser123",
  "comments": [],
  "time_context": {
    "period": "late_night",
    "greeting": "Good morning!",
    "energy_level": "focused"
  }
}
```

### Get Mood History
**Endpoint:** `GET /api/moods/history/`

```bash
# Basic request
curl -X GET http://localhost:8000/api/moods/history/ \
  -H "Authorization: Token your-token-here"

# With filters
curl -X GET "http://localhost:8000/api/moods/history/?start_date=2025-07-01&end_date=2025-07-23&mood=Contemplating&limit=10" \
  -H "Authorization: Token your-token-here"
```

### Get Mood Summary
**Endpoint:** `GET /api/moods/summary/`

```bash
curl -X GET http://localhost:8000/api/moods/summary/ \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "total_entries": 25,
  "mood_counts": {
    "Happy": 8,
    "Content": 6,
    "Neutral": 5,
    "Sad": 4,
    "Anxious": 2
  },
  "average_rating": 3.4,
  "average_sentiment": 0.2,
  "date_range": {
    "first_entry": "2025-06-01T10:00:00Z",
    "last_entry": "2025-07-23T16:30:45Z"
  }
}
```

### Get Mood Trends
**Endpoint:** `GET /api/moods/trends/`

```bash
curl -X GET "http://localhost:8000/api/moods/trends/?days=30" \
  -H "Authorization: Token your-token-here"
```

### Get Specific Mood Entry
**Endpoint:** `GET /api/moods/{mood_id}/`

```bash
curl -X GET http://localhost:8000/api/moods/45/ \
  -H "Authorization: Token your-token-here"
```

### Update Mood Entry
**Endpoint:** `PUT /api/moods/{mood_id}/`

```bash
curl -X PUT http://localhost:8000/api/moods/45/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Updated: Had an amazing day at work!"
  }'
```

### Delete Mood Entry
**Endpoint:** `DELETE /api/moods/{mood_id}/`

```bash
curl -X DELETE http://localhost:8000/api/moods/45/ \
  -H "Authorization: Token your-token-here"
```

---

## 💬 **Comments & Reflections**

### Add Comment to Mood Entry
**Endpoint:** `POST /api/moods/{mood_id}/comments/`

```bash
curl -X POST http://localhost:8000/api/moods/45/comments/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Reflecting on this mood, I realize exercise really helps my mental state."
  }'
```

**Sample Response:**
```json
{
  "id": 12,
  "content": "Reflecting on this mood, I realize exercise really helps my mental state.",
  "created_at": "2025-07-23T17:00:00.123456Z",
  "coin_reward": 2
}
```

### Get Comments for Mood Entry
**Endpoint:** `GET /api/moods/{mood_id}/comments/`

```bash
curl -X GET http://localhost:8000/api/moods/45/comments/ \
  -H "Authorization: Token your-token-here"
```

### Update Comment
**Endpoint:** `PUT /api/moods/{mood_id}/comments/{comment_id}/`

```bash
curl -X PUT http://localhost:8000/api/moods/45/comments/12/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Updated reflection: Exercise and adequate sleep are key to my happiness."
  }'
```

### Delete Comment
**Endpoint:** `DELETE /api/moods/{mood_id}/comments/{comment_id}/`

```bash
curl -X DELETE http://localhost:8000/api/moods/45/comments/12/ \
  -H "Authorization: Token your-token-here"
```

---

## 🤖 **AI-Powered Features**

### Get AI Motivation
**Endpoint:** `GET /api/suggestions/motivation/`

```bash
curl -X GET http://localhost:8000/api/suggestions/motivation/ \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "motivation": "Good afternoon! Your 12-day streak is impressive! 🌟 Based on your recent positive moods, you're building amazing momentum. Keep nurturing this upward trend!",
  "mood_trend": "positive",
  "personalized_with_ai": true,
  "source": "AI Service",
  "time_context": {
    "period": "afternoon",
    "greeting": "Good afternoon!",
    "suggested_activities": ["continued effort", "progress tracking"]
  }
}
```

### Get Habit Improvement Suggestions
**Endpoint:** `GET /api/suggestions/habits/`

```bash
curl -X GET http://localhost:8000/api/suggestions/habits/ \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "habit_suggestions": [
    "Try morning exercise - it correlates with your highest-rated moods",
    "Consider reducing work stress through better time management",
    "Maintain your meditation practice - it shows positive mood impact"
  ],
  "message": "AI-powered habit suggestions to help you cultivate wellbeing.",
  "personalized_with_ai": true,
  "source": "AI Service"
}
```

### Get Mood Pattern Analysis
**Endpoint:** `GET /api/moods/analysis/patterns/`

```bash
curl -X GET http://localhost:8000/api/moods/analysis/patterns/ \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "pattern_insights": [
    "Your mood tends to be best in the mornings",
    "Your mood tends to be best on Fridays",
    "Your mood tends to be worst on Mondays"
  ],
  "message": "Understanding your mood patterns can help you plan your activities better."
}
```

### Submit AI Feedback
**Endpoint:** `POST /api/ai-feedback/`

```bash
curl -X POST http://localhost:8000/api/ai-feedback/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "suggestion_type": "motivation",
    "rating": 5,
    "feedback": "Very helpful and personalized!"
  }'
```

### Get Premium AI Mood Insights
**Endpoint:** `GET /api/insights/?days=30`

```bash
curl -X GET "http://localhost:8000/api/insights/?days=30" \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "insights": [
    "Your mood shows a consistent upward trend over the past 30 days",
    "Exercise activities correlate strongly with your best moods"
  ],
  "recommendations": [
    "Continue your current exercise routine",
    "Consider tracking sleep patterns for additional insights"
  ],
  "mood_trends": {
    "average_rating": 3.7,
    "trend_direction": "improving",
    "pattern_strength": "strong"
  },
  "cost_coins": 5,
  "remaining_balance": 42
}
```

---

## 💰 **Behavior Engine & Gamification**

### Get Coin Balance
**Endpoint:** `GET /api/coins/balance/`

```bash
curl -X GET http://localhost:8000/api/coins/balance/ \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "current_balance": 47,
  "total_earned": 73,
  "total_spent": 26,
  "recent_transactions": [
    {
      "id": 15,
      "transaction_type": "earned",
      "amount": 2,
      "description": "Comment on mood entry",
      "balance_after": 47,
      "created_at": "2025-07-23T17:00:00.123456Z"
    }
  ]
}
```

### Stake Coins on Challenge
**Endpoint:** `POST /api/coins/stake/`

```bash
curl -X POST http://localhost:8000/api/coins/stake/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "challenge_type": "daily_log",
    "stake": 10,
    "duration_days": 7
  }'
```

**Sample Response:**
```json
{
  "challenge": {
    "id": 3,
    "challenge_type": "daily_log",
    "stake": 10,
    "duration_days": 7,
    "start_date": "2025-07-23",
    "end_date": "2025-07-30",
    "completed": false
  },
  "message": "Challenge accepted! You've staked 10 coins on a 7-day daily logging challenge.",
  "ai_message": "🎯 You've got this! A 7-day streak will double your investment. Stay consistent!"
}
```

### Get Streak Information
**Endpoint:** `GET /api/streak/`

```bash
curl -X GET http://localhost:8000/api/streak/ \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "current_streak": 12,
  "longest_streak": 18,
  "last_mood_log": "2025-07-23",
  "streak_status": "active",
  "days_until_next_milestone": 3,
  "clarity_score": 95,
  "motivational_message": "Amazing 12-day streak! You're on fire! 🔥"
}
```

### Get Next Nudge
**Endpoint:** `GET /api/nudges/next/`

```bash
curl -X GET http://localhost:8000/api/nudges/next/ \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "nudge": {
    "id": 25,
    "message": "Hey there! 🌅 Your morning energy is perfect for setting intentions. Ready for a quick mood check-in?",
    "nudge_type": "check_in",
    "tone": "gen_z_casual",
    "created_at": "2025-07-23T08:30:00.123456Z"
  },
  "time_context": {
    "period": "early_morning",
    "greeting": "Good morning!",
    "energy_level": "rising"
  },
  "personalized_with_ai": true
}
```

### Get Behavior Engine Stats
**Endpoint:** `GET /api/behavior/stats/`

```bash
curl -X GET http://localhost:8000/api/behavior/stats/ \
  -H "Authorization: Token your-token-here"
```

**Sample Response:**
```json
{
  "user_stats": {
    "total_moods": 25,
    "current_streak": 12,
    "coin_balance": 47,
    "clarity_score": 95,
    "total_comments": 8,
    "active_challenges": 1
  },
  "achievements": [
    "First Week Streak",
    "Reflection Master",
    "AI Collaborator"
  ],
  "engagement_level": "high",
  "next_milestone": "Two Week Streak (2 days to go)"
}
```

---

## 📤 **Data Export**

### Export Moods as JSON
**Endpoint:** `GET /api/moods/export/json/`

```bash
curl -X GET http://localhost:8000/api/moods/export/json/ \
  -H "Authorization: Token your-token-here" \
  -o moods_backup.json
```

### Export Moods as CSV
**Endpoint:** `GET /api/moods/export/csv/`

```bash
curl -X GET http://localhost:8000/api/moods/export/csv/ \
  -H "Authorization: Token your-token-here" \
  -o moods_data.csv
```

---

## 🔧 **Admin Endpoints**

### Sentiment Analysis (Admin Only)
**Endpoint:** `GET /api/sentiment-analysis/`

```bash
curl -X GET http://localhost:8000/api/sentiment-analysis/ \
  -H "Authorization: Token admin-token-here"
```

**Sample Response:**
```json
[
  {
    "user__username": "user1",
    "average_sentiment": 0.35,
    "mood_count": 15
  },
  {
    "user__username": "user2", 
    "average_sentiment": -0.12,
    "mood_count": 8
  }
]
```

---

## 🎯 **Usage Tips**

### Authentication Headers
Always include one of these headers for protected endpoints:
```bash
# Token Authentication
-H "Authorization: Token your-token-here"

# JWT Authentication  
-H "Authorization: Bearer your-jwt-access-token"
```

### Content Type
For POST/PUT/PATCH requests with JSON data:
```bash
-H "Content-Type: application/json"
```

### Error Handling
All endpoints return appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Server Error

### Rate Limiting
Be mindful of AI-powered endpoints which may have rate limits:
- Motivation suggestions: 10 requests/minute
- Habit suggestions: 5 requests/minute
- Premium insights: 3 requests/minute

---

## 🚀 **Quick Start Workflow**

1. **Register**: `POST /api/register/`
2. **Login**: `POST /api/login/` (get tokens)
3. **Log Mood**: `POST /api/moods/` 
4. **Add Reflection**: `POST /api/moods/{id}/comments/`
5. **Get AI Suggestions**: `GET /api/suggestions/motivation/`
6. **Check Progress**: `GET /api/behavior/stats/`

This covers all the major endpoints in the Moodify API. Each endpoint includes authentication, request/response examples, and practical usage patterns.
