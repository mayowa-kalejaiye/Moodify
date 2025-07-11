# API Documentation

## Development Mode
When running in DEBUG mode (development), Swagger UI and ReDoc are available at:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- JSON Schema: http://localhost:8000/swagger.json

## Production Mode
In production (DEBUG=False), API documentation endpoints are disabled to improve performance and security.

For API usage examples, see:
- `api_examples.md` in the project root
- Individual endpoint documentation in the tracker app

## Authentication
The API uses JWT tokens for authentication. Get a token via:
```
POST /api/api-token-auth/
{
    "username": "your_username",
    "password": "your_password"
}
```

Use the token in subsequent requests:
```
Authorization: Bearer <your-token>
```
