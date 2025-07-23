# Moodify API Examples

This document provides examples of how to use the Moodify API endpoints for various operations.

## Authentication Endpoints

### User Registration

Register a new user account with automatic profile creation and token generation.

**Endpoint:** `POST /api/register/`

**Important:** This endpoint requires data to be sent in the request body as JSON, not as URL query parameters. The `Content-Type: application/json` header must be set.

**Request Body:**
```json
{
  "username": "newuser123",
  "email": "newuser123@example.com",
  "password": "StrongPass123!",
  "password_confirm": "StrongPass123!"
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"securepass123","password_confirm":"securepass123"}'
```

**Sample Success Response:**
```json
{
  "token": "your-auth-token-here",
  "jwt": "your-jwt-token-here",
  "user": {
    "id": 12,
    "username": "newuser123",
    "email": "newuser123@example.com"
  },
  "profile": {
    "id": 12,
    "user": 12,
    "nickname": null,
    "bio": "",
    "mood_points": 0,
    "streak_days": 0,
    "created_at": "2023-06-01T14:23:45.123456Z",
    "updated_at": "2023-06-01T14:23:45.123456Z"
  }
}
```

### User Login

Log in with existing credentials to receive authentication tokens.

**Endpoint:** `POST /api/login/`

**Important:** Like registration, this endpoint requires JSON data in the request body.

**Request Body:**
```json
{
  "username": "existinguser",
  "password": "YourPassword123!"
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"securepass123"}'
```

**Sample Success Response:**
```json
{
  "token": "your-auth-token-here",
  "jwt": "your-jwt-token-here",
  "user": {
    "id": 5,
    "username": "existinguser",
    "email": "existing@example.com"
  }
}
```

## User Profile Endpoints

### Get Current User Profile

Retrieve the profile for the currently authenticated user.

**Endpoint:** `GET /api/profile/`

**Authentication:** Requires JWT or Token authentication.

**Headers:**
```
Authorization: JWT your-jwt-token-here
```
or
```
Authorization: Token your-token-here
```

**curl Example:**
```bash
curl -X GET http://localhost:8000/api/profile/ \
  -H "Authorization: JWT your-jwt-token-here"
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
  "nickname": "Mood Master",
  "bio": "Tracking my moods for better mental health.",
  "mood_points": 250,
  "streak_days": 7,
  "created_at": "2023-05-15T10:20:30.123456Z",
  "updated_at": "2023-06-01T11:22:33.445566Z"
}
```

### Update User Profile

Update the profile details for the currently authenticated user.

**Endpoint:** `PATCH /api/profile/`

**Authentication:** Requires JWT or Token authentication.

**Headers:**
```
Authorization: JWT your-jwt-token-here
Content-Type: application/json
```

**Request Body:**
```json
{
  "nickname": "Mood Explorer",
  "bio": "On a journey to understand my emotional patterns."
}
```

**curl Example:**
```bash
curl -X PATCH http://localhost:8000/api/profile/ \
  -H "Authorization: JWT your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{"nickname":"Mood Explorer","bio":"On a journey to understand my emotional patterns."}'
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
  "nickname": "Mood Explorer",
  "bio": "On a journey to understand my emotional patterns.",
  "mood_points": 250,
  "streak_days": 7,
  "created_at": "2023-05-15T10:20:30.123456Z",
  "updated_at": "2023-06-01T15:22:33.445566Z"
}
```

## Mood Entry Endpoints

### Create a New Mood Entry

Record a new mood entry in the user's mood journal.

**Endpoint:** `POST /api/moods/`

**Authentication:** Requires JWT or Token authentication.

**Headers:**
```
Authorization: JWT your-jwt-token-here
Content-Type: application/json
```

**Request Body:**
```json
{
  "mood_level": 4,
  "notes": "Feeling quite positive today after my morning workout.",
  "activities": ["exercise", "meditation"],
  "tags": ["energetic", "motivated"]
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/api/moods/ \
  -H "Authorization: JWT your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{"mood_level":4,"notes":"Feeling quite positive today after my morning workout.","activities":["exercise","meditation"],"tags":["energetic","motivated"]}'
```

**Sample Response:**
```json
{
  "id": 45,
  "user": 5,
  "mood_level": 4,
  "notes": "Feeling quite positive today after my morning workout.",
  "activities": ["exercise", "meditation"],
  "tags": ["energetic", "motivated"],
  "created_at": "2023-06-01T16:30:45.123456Z",
  "updated_at": "2023-06-01T16:30:45.123456Z"
}
```

### Get Mood Entries History

Retrieve a list of the user's previous mood entries.

**Endpoint:** `GET /api/moods/`

**Authentication:** Requires JWT or Token authentication.

**Headers:**
```
Authorization: JWT your-jwt-token-here
```

**Optional Query Parameters:**
- `start_date`: Filter entries on or after this date (format: YYYY-MM-DD)
- `end_date`: Filter entries on or before this date (format: YYYY-MM-DD)
- `mood_level`: Filter by specific mood level (1-5)
- `page`: Pagination page number
- `page_size`: Number of results per page

**curl Example:**
```bash
curl -X GET "http://localhost:8000/api/moods/?start_date=2023-05-01&end_date=2023-05-31&mood_level=4" \
  -H "Authorization: JWT your-jwt-token-here"
```

**Sample Response:**
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/moods/?page=2&start_date=2023-05-01&end_date=2023-05-31&mood_level=4",
  "previous": null,
  "results": [
    {
      "id": 40,
      "user": 5,
      "mood_level": 4,
      "notes": "Had a great day at work, project is going well.",
      "activities": ["work", "socializing"],
      "tags": ["productive", "connected"],
      "created_at": "2023-05-25T19:15:30.123456Z",
      "updated_at": "2023-05-25T19:15:30.123456Z"
    },
    // More mood entries...
  ]
}
```

## Challenge Endpoints

### Get Available Challenges

Retrieve a list of available mood challenges.

**Endpoint:** `GET /api/challenges/`

**Authentication:** Requires JWT or Token authentication.

**Headers:**
```
Authorization: JWT your-jwt-token-here
```

**curl Example:**
```bash
curl -X GET http://localhost:8000/api/challenges/ \
  -H "Authorization: JWT your-jwt-token-here"
```

**Sample Response:**
```json
[
  {
    "id": 1,
    "title": "7-Day Gratitude Journal",
    "description": "Record three things you're grateful for each day for a week.",
    "duration_days": 7,
    "difficulty": "easy",
    "points_reward": 50,
    "requirements": "Complete all 7 days of entries.",
    "created_at": "2023-01-15T10:00:00.000000Z"
  },
  {
    "id": 2,
    "title": "Mood Improvement Marathon",
    "description": "Track activities that boost your mood for 14 consecutive days.",
    "duration_days": 14,
    "difficulty": "medium",
    "points_reward": 100,
    "requirements": "Enter at least one positive mood-boosting activity each day.",
    "created_at": "2023-02-01T14:30:00.000000Z"
  }
]
```

### Join a Challenge

Sign up for a specific mood challenge.

**Endpoint:** `POST /api/challenges/{challenge_id}/join/`

**Authentication:** Requires JWT or Token authentication.

**Headers:**
```
Authorization: JWT your-jwt-token-here
Content-Type: application/json
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/api/challenges/1/join/ \
  -H "Authorization: JWT your-jwt-token-here"
```

**Sample Response:**
```json
{
  "id": 8,
  "user": 5,
  "challenge": 1,
  "start_date": "2023-06-01T00:00:00.000000Z",
  "end_date": "2023-06-08T00:00:00.000000Z",
  "is_completed": false,
  "progress": 0,
  "created_at": "2023-06-01T17:45:20.123456Z"
}
```

## Additional Notes

- All timestamps are in UTC and follow ISO 8601 format
- Authentication tokens do not expire in the development environment, but will have expiration in production
- For password reset functionality, see the separate documentation
