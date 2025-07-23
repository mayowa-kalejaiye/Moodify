# Postman Folder Pre-Request Script Instructions

This file contains instructions for creating pre-request scripts at the Postman folder level when working with the Moodify API.

## Authentication Folder Pre-Request Script

```javascript
// Pre-request script for the Authentication folder
// This script runs before each request in the Authentication folder

console.log("Running authentication request pre-script...");

// For authentication requests, we want to clear any existing tokens when explicitly logging in
// This prevents confusion when testing different users
if (pm.request.url.path.includes("login") || pm.request.url.path.includes("register")) {
    // Check if this is an intentional fresh login
    const freshLogin = pm.variables.get("fresh_login");
    
    if (freshLogin === "true") {
        // Clear existing authentication tokens
        pm.environment.unset("auth_token");
        pm.environment.unset("jwt_access_token");
        pm.environment.unset("jwt_refresh_token");
        
        console.log("Cleared existing authentication tokens for fresh login");
        
        // Reset the flag
        pm.variables.set("fresh_login", "false");
    }
}

// For token refresh requests, ensure we have a refresh token
if (pm.request.url.path.includes("token/refresh")) {
    const refreshToken = pm.environment.get("jwt_refresh_token");
    
    if (!refreshToken) {
        console.error("⚠️ No refresh token found. Please login first to obtain a refresh token.");
    } else {
        // Ensure the request body contains the refresh token
        try {
            if (!pm.request.body) {
                pm.request.body = {
                    mode: 'raw',
                    raw: JSON.stringify({ refresh: refreshToken }),
                    options: {
                        raw: {
                            language: 'json'
                        }
                    }
                };
            } else if (pm.request.body.mode === 'raw') {
                const bodyData = JSON.parse(pm.request.body.raw || '{}');
                bodyData.refresh = refreshToken;
                
                pm.request.body.update({
                    raw: JSON.stringify(bodyData, null, 2)
                });
            }
            
            console.log("Refresh token added to request body");
        } catch (error) {
            console.error("Error updating request body with refresh token:", error);
        }
    }
}
```

## User Data Folder Pre-Request Script

```javascript
// Pre-request script for the User Data folder
// This script runs before each request in the User Data folder

console.log("Running user data request pre-script...");

// Check for authentication before making user data requests
const authToken = pm.environment.get("auth_token");
const jwtAccessToken = pm.environment.get("jwt_access_token");

if (!authToken && !jwtAccessToken) {
    console.error("⚠️ No authentication tokens found. User data requests will likely fail.");
    console.error("Please login first to obtain authentication tokens.");
}

// Add user ID to URL if needed and available
const userId = pm.environment.get("user_id");
if (userId && pm.request.url.path.includes("{user_id}")) {
    // Replace the placeholder with the actual user ID
    const url = pm.request.url.toString().replace("{user_id}", userId);
    pm.request.url = url;
    console.log(`User ID ${userId} added to request URL`);
}
```

## Mood Data Folder Pre-Request Script

```javascript
// Pre-request script for the Mood Data folder
// This script runs before each request in the Mood Data folder

console.log("Running mood data request pre-script...");

// Check for authentication before making mood data requests
const authToken = pm.environment.get("auth_token");
const jwtAccessToken = pm.environment.get("jwt_access_token");

if (!authToken && !jwtAccessToken) {
    console.error("⚠️ No authentication tokens found. Mood data requests will likely fail.");
    console.error("Please login first to obtain authentication tokens.");
}

// For mood creation requests, ensure we have a valid mood value
if (pm.request.method === "POST" && pm.request.url.path.includes("moods")) {
    try {
        if (pm.request.body && pm.request.body.mode === 'raw') {
            const bodyData = JSON.parse(pm.request.body.raw || '{}');
            
            // Validate mood value if present
            if (bodyData.mood_value !== undefined) {
                const moodValue = parseInt(bodyData.mood_value);
                
                if (isNaN(moodValue) || moodValue < 1 || moodValue > 10) {
                    console.error("⚠️ Invalid mood value. Mood must be between 1 and 10.");
                }
            }
            
            // If no date is provided, add current date
            if (!bodyData.date) {
                bodyData.date = new Date().toISOString().split('T')[0];
                
                pm.request.body.update({
                    raw: JSON.stringify(bodyData, null, 2)
                });
                
                console.log("Added current date to mood request");
            }
        }
    } catch (error) {
        console.error("Error processing mood request body:", error);
    }
}
```
