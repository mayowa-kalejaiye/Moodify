# Postman Folder Post-Response Script Instructions

This file contains instructions for creating post-response scripts at the Postman folder level when working with the Moodify API.

## Authentication Folder Post-Response Script

```javascript
// Post-response script for the Authentication folder
// This script runs after each request in the Authentication folder

console.log("Running authentication request post-script...");

// Process login and token responses
if (pm.response.code === 200 || pm.response.code === 201) {
    if (pm.request.url.path.includes("login") || pm.request.url.path.includes("register") || pm.request.url.path.includes("token")) {
        try {
            const responseData = pm.response.json();
            
            // Save tokens from login or register responses
            if (responseData.token) {
                pm.environment.set("auth_token", responseData.token);
                console.log("Authentication token saved");
            }
            
            if (responseData.access) {
                pm.environment.set("jwt_access_token", responseData.access);
                console.log("JWT access token saved");
                
                // Reset token expired flag
                pm.environment.set("jwt_token_expired", false);
            }
            
            if (responseData.refresh) {
                pm.environment.set("jwt_refresh_token", responseData.refresh);
                console.log("JWT refresh token saved");
            }
            
            // Save user data if available
            if (responseData.user) {
                if (responseData.user.id) {
                    pm.environment.set("user_id", responseData.user.id);
                }
                
                if (responseData.user.username) {
                    pm.environment.set("username", responseData.user.username);
                }
                
                console.log("User data saved to environment");
            }
        } catch (error) {
            console.error("Error processing authentication response:", error);
        }
    }
    
    // Process token refresh responses
    if (pm.request.url.path.includes("token/refresh")) {
        try {
            const responseData = pm.response.json();
            
            if (responseData.access) {
                pm.environment.set("jwt_access_token", responseData.access);
                console.log("JWT access token refreshed");
                
                // Reset token expired flag
                pm.environment.set("jwt_token_expired", false);
                pm.environment.set("needs_token_refresh", false);
            }
            
            // Some implementations also return a new refresh token
            if (responseData.refresh) {
                pm.environment.set("jwt_refresh_token", responseData.refresh);
                console.log("JWT refresh token updated");
            }
        } catch (error) {
            console.error("Error processing token refresh response:", error);
        }
    }
    
    // Process logout responses
    if (pm.request.url.path.includes("logout") && pm.response.code === 200) {
        // Clear tokens on successful logout
        pm.environment.unset("auth_token");
        pm.environment.unset("jwt_access_token");
        pm.environment.unset("jwt_refresh_token");
        
        console.log("Authentication tokens cleared after logout");
    }
}

// Handle authentication errors
if (pm.response.code === 401 || pm.response.code === 403) {
    console.error("Authentication error:", pm.response.code);
    
    try {
        const responseData = pm.response.json();
        console.error("Error details:", responseData);
    } catch (error) {
        console.error("Response text:", pm.response.text());
    }
}
```

## User Data Folder Post-Response Script

```javascript
// Post-response script for the User Data folder
// This script runs after each request in the User Data folder

console.log("Running user data request post-script...");

// Process user profile responses
if (pm.response.code === 200 && pm.request.url.path.includes("profile")) {
    try {
        const responseData = pm.response.json();
        
        // Save user profile data to environment for use in other requests
        if (responseData.profile) {
            if (responseData.profile.age) {
                pm.environment.set("user_age", responseData.profile.age);
            }
            
            if (responseData.profile.coin_balance !== undefined) {
                pm.environment.set("coin_balance", responseData.profile.coin_balance);
            }
            
            if (responseData.profile.streak_count !== undefined) {
                pm.environment.set("streak_count", responseData.profile.streak_count);
            }
            
            console.log("User profile data saved to environment");
        }
    } catch (error) {
        console.error("Error processing user profile response:", error);
    }
}

// Handle user data errors
if (pm.response.code >= 400) {
    console.error("User data request error:", pm.response.code);
    
    try {
        const responseData = pm.response.json();
        console.error("Error details:", responseData);
    } catch (error) {
        console.error("Response text:", pm.response.text());
    }
}
```

## Mood Data Folder Post-Response Script

```javascript
// Post-response script for the Mood Data folder
// This script runs after each request in the Mood Data folder

console.log("Running mood data request post-script...");

// Process mood creation responses
if (pm.response.code === 201 && pm.request.method === "POST" && pm.request.url.path.includes("moods")) {
    try {
        const responseData = pm.response.json();
        
        // Save mood ID for use in subsequent requests
        if (responseData.id) {
            pm.environment.set("last_mood_id", responseData.id);
            console.log("Mood ID saved to environment:", responseData.id);
        }
        
        // Save other mood data if needed
        if (responseData.date) {
            pm.environment.set("last_mood_date", responseData.date);
        }
        
        if (responseData.mood_value) {
            pm.environment.set("last_mood_value", responseData.mood_value);
        }
        
        console.log("Created mood:", responseData);
    } catch (error) {
        console.error("Error processing mood creation response:", error);
    }
}

// Process mood history responses
if (pm.response.code === 200 && pm.request.url.path.includes("history")) {
    try {
        const responseData = pm.response.json();
        
        // Process and save mood history data if needed
        if (responseData.results && responseData.results.length > 0) {
            // Save most recent mood ID
            pm.environment.set("most_recent_mood_id", responseData.results[0].id);
            
            // Save mood count
            pm.environment.set("mood_count", responseData.count || responseData.results.length);
            
            console.log(`Mood history retrieved: ${responseData.count || responseData.results.length} moods`);
        } else {
            console.log("No mood history found");
        }
    } catch (error) {
        console.error("Error processing mood history response:", error);
    }
}

// Handle mood data errors
if (pm.response.code >= 400) {
    console.error("Mood data request error:", pm.response.code);
    
    try {
        const responseData = pm.response.json();
        console.error("Error details:", responseData);
    } catch (error) {
        console.error("Response text:", pm.response.text());
    }
}
```
