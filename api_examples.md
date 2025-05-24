# Mood Tracker API Examples

## Authentication Examples

### Register a new user
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"securepass123","password_confirm":"securepass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"securepass123"}'
```

### How to use the token

The token should be included in the Authorization header with the prefix "Token":

```bash
curl -X POST http://localhost:8000/api/moods/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"mood":"happy","notes":"Had a great day today!"}'
```

### How to use JWT

Alternatively, you can use the JWT token (access token) with Bearer prefix:

```bash
curl -X POST http://localhost:8000/api/moods/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"mood":"happy","notes":"Had a great day today!"}'
```

## New Features: Comments and AI Suggestions

### Add a comment to a mood entry
```bash
curl -X POST http://localhost:8000/api/moods/1/comments/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"content":"I reflected on this mood entry and realized it was triggered by my lack of sleep"}'
```

### Get comments for a mood entry
```bash
curl -X GET http://localhost:8000/api/moods/1/comments/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Update a comment
```bash
curl -X PUT http://localhost:8000/api/moods/1/comments/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"content":"Updated reflection on my mood"}'
```

### Delete a comment
```bash
curl -X DELETE http://localhost:8000/api/moods/1/comments/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Get personalized motivation
**Description:** Retrieves AI-generated motivational messages tailored to the user's recent mood trends and specific patterns like anxiety or stress.
```bash
curl -X GET http://localhost:8000/api/suggestions/motivation/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Get habit improvement suggestions
**Description:** Provides AI-generated suggestions for habit improvements based on activities correlated with positive or negative moods from the last two weeks.
```bash
curl -X GET http://localhost:8000/api/suggestions/habits/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Get mood pattern analysis
**Description:** Analyzes mood data from the last month to identify patterns related to time of day and day of the week, offering insights for better activity planning.
```bash
curl -X GET http://localhost:8000/api/moods/analysis/patterns/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Mood Operations

### Get mood options
```bash
curl -X GET http://localhost:8000/api/moods/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Log a new mood
```bash
curl -X POST http://localhost:8000/api/moods/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"mood":"happy","notes":"Had a great day today!"}'
```

### Get mood history
```bash
curl -X GET http://localhost:8000/api/moods/history/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Filter mood history
```bash
curl -X GET "http://localhost:8000/api/moods/history/?start_date=2023-01-01&end_date=2023-12-31&mood=happy" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Get mood summary
```bash
curl -X GET http://localhost:8000/api/moods/summary/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Get mood trends
```bash
curl -X GET "http://localhost:8000/api/moods/trends/?days=30" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Get a specific mood entry
```bash
curl -X GET http://localhost:8000/api/moods/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Update a mood entry
```bash
curl -X PUT http://localhost:8000/api/moods/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"notes":"Updated notes about my mood"}'
```

### Delete a mood entry
```bash
curl -X DELETE http://localhost:8000/api/moods/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Data Export

### Export as JSON
```bash
curl -X GET http://localhost:8000/api/moods/export/json/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -o moods.json
```

### Export as CSV
```bash
curl -X GET http://localhost:8000/api/moods/export/csv/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -o moods.csv
```

## Admin Operations (requires staff/admin user)

### Sentiment analysis across users
```bash
curl -X GET http://localhost:8000/api/sentiment-analysis/ \
  -H "Authorization: Token ADMIN_TOKEN_HERE"
```
