#!/usr/bin/env python3
"""
Quick test to check if Swagger UI content is loading
"""

import requests
import time

def check_swagger_content():
    """Check if Swagger UI is loading with actual content"""
    
    url = 'https://moodify-wmcd.onrender.com/swagger/'
    
    print(f"🔍 Checking Swagger UI content at: {url}")
    print("=" * 50)
    
    try:
        response = requests.get(url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} characters")
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # Check for key indicators that Swagger UI is working
            indicators = [
                'swagger',
                'api',
                'spec',
                'endpoint',
                'authorization',
                'swagger-ui',
                'openapi'
            ]
            
            found_indicators = [ind for ind in indicators if ind in content]
            
            print(f"Found keywords: {found_indicators}")
            
            # Check for common issues
            if len(response.text.strip()) < 100:
                print("❌ ISSUE: Page content is too short - likely blank or error page")
                return False
            elif 'swagger-ui' in content or 'openapi' in content:
                print("✅ SUCCESS: Swagger UI content detected!")
                return True
            elif len(found_indicators) >= 3:
                print("✅ LIKELY SUCCESS: Multiple API-related keywords found")
                return True
            else:
                print("❌ ISSUE: Page loads but doesn't seem to contain Swagger UI")
                print("First 500 characters of response:")
                print("-" * 30)
                print(response.text[:500])
                print("-" * 30)
                return False
        else:
            print(f"❌ FAILED: Status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == '__main__':
    # Wait a moment for deployment
    print("⏳ Waiting 10 seconds for deployment to complete...")
    time.sleep(10)
    
    success = check_swagger_content()
    
    if success:
        print("\n🎉 Swagger UI appears to be working!")
    else:
        print("\n⚠️  There may still be issues with the Swagger UI display.")
        print("💡 Try refreshing the page or checking static file configuration.")
