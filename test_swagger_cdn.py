import requests
import time

def test_swagger_after_fix():
    """Test Swagger UI after applying CDN fix"""
    
    print("🧪 Testing Swagger UI after CDN fix...")
    print("=" * 50)
    
    url = 'https://moodify-wmcd.onrender.com/swagger/'
    
    try:
        response = requests.get(url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} characters")
        
        if response.status_code == 200:
            # Check if the content contains CDN links
            content = response.text.lower()
            
            if 'cdn.jsdelivr.net' in content:
                print("✅ SUCCESS: CDN resources detected in HTML!")
            else:
                print("⚠️  CDN resources not found, checking for other content...")
            
            if 'swagger' in content and 'div id="swagger-ui"' in content:
                print("✅ SUCCESS: Swagger UI HTML structure present!")
            else:
                print("❌ FAILED: Swagger UI structure missing")
                
            # Check for any error messages
            if 'error' in content or 'not found' in content:
                print("⚠️  Warning: Error messages detected in content")
            
            # Print a sample of the content for debugging
            print(f"\nFirst 200 characters of response:")
            print(f"'{response.text[:200]}...'")
            
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == '__main__':
    # Wait a bit for deployment
    print("Waiting 30 seconds for deployment to complete...")
    time.sleep(30)
    test_swagger_after_fix()
