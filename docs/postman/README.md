# Postman Collection and API Examples

This directory contains API examples, Postman collections, and other API testing resources for the Moodify application.

## Contents

- [API Examples](api_examples.md) - Comprehensive guide to using the Moodify API with curl examples
- Postman Collections (JSON files) - Import these into Postman for quick API testing

## Using the Postman Collections

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Import the collection JSON files from this directory
3. Set up environment variables:
   - `base_url`: Your API base URL (e.g., `http://localhost:8000` for local development)
   - `jwt_token`: Store your JWT token after login
   - `auth_token`: Store your Auth token after login

## Authentication Flow

1. Use the Register or Login requests to get authentication tokens
2. The collection's scripts will automatically set your JWT and Auth tokens as environment variables
3. Subsequent requests will use these tokens for authentication

## API Testing Tips

- Use the Pre-request Scripts to set up test data
- Check the Tests tab for assertion examples
- Use environment variables to avoid hardcoding values
