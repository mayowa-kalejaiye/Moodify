# Postman HTTP Request Post-Response Script Instructions

This file contains instructions for creating post-response scripts for Postman HTTP requests when working with the Moodify API.

## User Registration Post-Response Script

```javascript
// Post-response script for Postman User Registration Request
// This script processes the response after registration

// Check if the registration was successful
if (pm.response.code === 201) {
    // Extract token and user data from response
    try {
        const responseData = pm.response.json();
        
        // Save authentication token to environment
        if (responseData.token) {
            pm.environment.set("auth_token", responseData.token);
            console.log("Authentication token saved to environment");
        }
        
        // Save user ID to environment if present
        if (responseData.user && responseData.user.id) {
            pm.environment.set("user_id", responseData.user.id);
            console.log("User ID saved to environment");
        }
        
        // Set a flag to indicate successful registration
        pm.environment.set("registration_successful", true);
        
        console.log("Registration successful! User created with data:", responseData.user);
    } catch (error) {
        console.error("Error processing response:", error);
    }
} else {
    // Set flag to indicate failed registration
    pm.environment.set("registration_successful", false);
    
    // Log the error for debugging
    try {
        const errorData = pm.response.json();
        console.error("Registration failed:", errorData);
    } catch (error) {
        console.error("Registration failed with status:", pm.response.code);
        console.error("Response text:", pm.response.text());
    }
}

// Add test assertions
pm.test("Status code is 201 Created", function () {
    pm.response.to.have.status(201);
});

pm.test("Response contains token", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('token');
    pm.expect(responseData.token).to.be.a('string').and.to.have.lengthOf.at.least(1);
});

pm.test("Response contains user data", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('user');
    pm.expect(responseData.user).to.have.property('id');
    pm.expect(responseData.user).to.have.property('username');
    pm.expect(responseData.user).to.have.property('email');
});
```

## User Login Post-Response Script

```javascript
// Post-response script for Postman User Login Request
// This script processes the response after login

// Check if the login was successful
if (pm.response.code === 200) {
    // Extract tokens and user data from response
    try {
        const responseData = pm.response.json();
        
        // Save authentication tokens to environment
        if (responseData.token) {
            pm.environment.set("auth_token", responseData.token);
            console.log("Legacy token saved to environment");
        }
        
        if (responseData.access) {
            pm.environment.set("jwt_access_token", responseData.access);
            console.log("JWT access token saved to environment");
        }
        
        if (responseData.refresh) {
            pm.environment.set("jwt_refresh_token", responseData.refresh);
            console.log("JWT refresh token saved to environment");
        }
        
        // Save user ID to environment if present
        if (responseData.user && responseData.user.id) {
            pm.environment.set("user_id", responseData.user.id);
            console.log("User ID saved to environment");
        }
        
        // Set a flag to indicate successful login
        pm.environment.set("login_successful", true);
        
        console.log("Login successful! User data:", responseData.user);
    } catch (error) {
        console.error("Error processing response:", error);
    }
} else {
    // Set flag to indicate failed login
    pm.environment.set("login_successful", false);
    
    // Log the error for debugging
    try {
        const errorData = pm.response.json();
        console.error("Login failed:", errorData);
    } catch (error) {
        console.error("Login failed with status:", pm.response.code);
        console.error("Response text:", pm.response.text());
    }
}

// Add test assertions
pm.test("Status code is 200 OK", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains authentication tokens", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('token');  // Legacy token
    pm.expect(responseData).to.have.property('access'); // JWT access token
    pm.expect(responseData).to.have.property('refresh'); // JWT refresh token
});

pm.test("Response contains user data", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('user');
    pm.expect(responseData.user).to.have.property('id');
    pm.expect(responseData.user).to.have.property('username');
});

// Setup for subsequent requests
if (pm.response.code === 200) {
    const responseData = pm.response.json();
    if (responseData.token) {
        // Create a collection variable for the Authorization header
        pm.collectionVariables.set("Authorization", "Token " + responseData.token);
    }
    
    if (responseData.access) {
        // Create a collection variable for the JWT Authorization header
        pm.collectionVariables.set("JWTAuthorization", "Bearer " + responseData.access);
    }
}
```
