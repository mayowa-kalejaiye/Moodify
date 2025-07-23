# Postman Collections Pre-Request Script Instructions

This file contains instructions for creating pre-request scripts at the Postman collection level when working with the Moodify API.

## Collection Pre-Request Script

```javascript
// Collection-level Pre-request Script for Moodify API
// This script runs before every request in the collection

// Check if we have the required authentication token
const authToken = pm.environment.get("auth_token") || pm.collectionVariables.get("auth_token");
const jwtAccessToken = pm.environment.get("jwt_access_token") || pm.collectionVariables.get("jwt_access_token");

// If this isn't an authentication request and we don't have tokens, warn the user
if (!pm.request.url.path.includes("login") && 
    !pm.request.url.path.includes("register") && 
    !pm.request.url.path.includes("token") && 
    !authToken && !jwtAccessToken) {
    console.warn("⚠️ No authentication token found. You may need to log in first.");
}

// Add authentication headers if we have tokens
if (authToken) {
    // Set the Authorization header with the token if it's not already set
    const hasAuthHeader = pm.request.headers.has("Authorization");
    if (!hasAuthHeader) {
        pm.request.headers.add({
            key: "Authorization",
            value: `Token ${authToken}`
        });
        console.log("Added Token authentication header");
    }
}

// Add JWT authentication if available and Token auth isn't already set
if (jwtAccessToken && !pm.request.headers.has("Authorization")) {
    pm.request.headers.add({
        key: "Authorization",
        value: `Bearer ${jwtAccessToken}`
    });
    console.log("Added JWT authentication header");
}

// Add Content-Type header if not already set and this is a POST, PUT or PATCH request
const method = pm.request.method.toUpperCase();
if ((method === "POST" || method === "PUT" || method === "PATCH") && !pm.request.headers.has("Content-Type")) {
    pm.request.headers.add({
        key: "Content-Type",
        value: "application/json"
    });
    console.log("Added Content-Type header");
}

// Add any custom headers needed for the API
if (!pm.request.headers.has("Accept")) {
    pm.request.headers.add({
        key: "Accept",
        value: "application/json"
    });
    console.log("Added Accept header");
}

// Handle JWT token refresh if needed
const tokenExpired = pm.environment.get("jwt_token_expired");
const refreshToken = pm.environment.get("jwt_refresh_token");

if (tokenExpired && refreshToken && !pm.request.url.path.includes("token/refresh")) {
    console.log("JWT token expired, will attempt refresh after this request");
    pm.environment.set("needs_token_refresh", true);
}
```
