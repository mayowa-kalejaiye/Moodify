# Postman Collections Post-Response Script Instructions

This file contains instructions for creating post-response scripts at the Postman collection level when working with the Moodify API.

## Collection Post-Response Script

```javascript
// Collection-level Post-response Script for Moodify API
// This script runs after every request in the collection

// Check for authentication errors that might indicate an expired token
if (pm.response.code === 401) {
    try {
        const responseData = pm.response.json();
        
        // Check for token expiration messages
        const errorMessages = [
            "Token is invalid or expired",
            "Authentication credentials were not provided",
            "Invalid token",
            "Token has expired",
            "Signature has expired"
        ];
        
        const hasTokenError = errorMessages.some(msg => 
            responseData.detail && responseData.detail.includes(msg) || 
            responseData.error && responseData.error.includes(msg)
        );
        
        if (hasTokenError) {
            console.log("Authentication token appears to be expired");
            
            // Mark JWT token as expired if we're using JWT
            if (pm.environment.get("jwt_access_token")) {
                pm.environment.set("jwt_token_expired", true);
                console.log("JWT token marked as expired");
            }
            
            // Attempt token refresh if we have a refresh token and this wasn't already a refresh attempt
            const refreshToken = pm.environment.get("jwt_refresh_token");
            const needsRefresh = pm.environment.get("needs_token_refresh");
            
            if (refreshToken && needsRefresh && !pm.request.url.path.includes("token/refresh")) {
                console.log("Will attempt to refresh JWT token");
                
                // You would set up a call to the refresh endpoint here or alert the user to refresh manually
                // pm.environment.set("trigger_refresh_request", true);
                
                // For this example, we'll just log a message
                console.log("⚠️ JWT token expired. Please run the 'Refresh Token' request to get a new token.");
            }
        }
    } catch (error) {
        console.error("Error checking for token expiration:", error);
    }
}

// Log response time for performance monitoring
const responseTime = pm.response.responseTime;
console.log(`Response time: ${responseTime}ms`);

// If this is a successful request, clear any error flags
if (pm.response.code >= 200 && pm.response.code < 300) {
    pm.environment.set("last_request_failed", false);
    
    // If this was a token refresh request, clear the expired flag
    if (pm.request.url.path.includes("token/refresh")) {
        pm.environment.set("jwt_token_expired", false);
        pm.environment.set("needs_token_refresh", false);
        console.log("Token refresh flags cleared");
    }
} else if (pm.response.code >= 400) {
    // Mark that the last request failed
    pm.environment.set("last_request_failed", true);
    
    // Store error information for debugging
    try {
        const errorData = pm.response.json();
        pm.environment.set("last_error", JSON.stringify(errorData));
        console.error("Request failed:", errorData);
    } catch (error) {
        pm.environment.set("last_error", pm.response.text());
        console.error("Request failed with status:", pm.response.code);
        console.error("Response text:", pm.response.text());
    }
}

// Track rate limiting if the API uses it
if (pm.response.headers.has("X-RateLimit-Remaining")) {
    const remaining = pm.response.headers.get("X-RateLimit-Remaining");
    console.log(`Rate limit remaining: ${remaining}`);
    
    if (parseInt(remaining) < 10) {
        console.warn("⚠️ Rate limit is getting low!");
    }
}
```
