# Postman HTTP Request Pre-Request Script Instructions

This file contains instructions for creating pre-request scripts for Postman HTTP requests when working with the Moodify API.

## User Registration Pre-Request Script

```javascript
// Pre-request script for Postman User Registration Request
// This script prepares the data for a new user registration

// Generate random values for testing
const randomNum = Math.floor(Math.random() * 10000);
const username = `testuser${randomNum}`;
const email = `testuser${randomNum}@example.com`;
const password = `TestPass123!`;

// Set default values in the request body
if (!pm.request.body || !pm.request.body.raw) {
    // Create request body if it doesn't exist
    pm.request.body = {
        mode: 'raw',
        raw: JSON.stringify({
            username: username,
            email: email,
            password: password,
            password_confirm: password,
            first_name: "Test",
            last_name: "User",
            profile: {
                age: 25
            }
        }),
        options: {
            raw: {
                language: 'json'
            }
        }
    };
} else {
    // Parse existing body if it exists
    try {
        const bodyData = JSON.parse(pm.request.body.raw);
        
        // Only set values if they're not already set by the user
        if (!bodyData.username) bodyData.username = username;
        if (!bodyData.email) bodyData.email = email;
        if (!bodyData.password) bodyData.password = password;
        if (!bodyData.password_confirm) bodyData.password_confirm = password;
        
        // Update the request body
        pm.request.body.update({
            raw: JSON.stringify(bodyData, null, 2)
        });
    } catch (error) {
        console.error("Error parsing request body:", error);
    }
}

// Set environment variables for use in later requests
pm.environment.set("username", username);
pm.environment.set("password", password);
pm.environment.set("email", email);

console.log(`Prepared registration data for user: ${username}`);
```

## User Login Pre-Request Script

```javascript
// Pre-request script for Postman User Login Request
// This script prepares the data for user login

// Get username and password from environment or set defaults
const username = pm.environment.get("username") || "your_username";
const password = pm.environment.get("password") || "your_password";

// Set request body
if (!pm.request.body || !pm.request.body.raw) {
    // Create request body if it doesn't exist
    pm.request.body = {
        mode: 'raw',
        raw: JSON.stringify({
            username: username,
            password: password
        }),
        options: {
            raw: {
                language: 'json'
            }
        }
    };
} else {
    // Parse existing body if it exists
    try {
        const bodyData = JSON.parse(pm.request.body.raw);
        
        // Only set values if they're not already set by the user
        if (!bodyData.username) bodyData.username = username;
        if (!bodyData.password) bodyData.password = password;
        
        // Update the request body
        pm.request.body.update({
            raw: JSON.stringify(bodyData, null, 2)
        });
    } catch (error) {
        console.error("Error parsing request body:", error);
    }
}

console.log(`Prepared login data for user: ${username}`);
```
