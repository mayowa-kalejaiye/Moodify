import requests

def test_json_endpoint():
    """Test if the JSON schema endpoint is working"""
    
    print("🔍 Testing JSON Schema Endpoint")
    print("=" * 40)
    
    url = 'https://moodify-wmcd.onrender.com/swagger.json'
    
    try:
        response = requests.get(url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ SUCCESS: Valid JSON response!")
                
                # Check for OpenAPI/Swagger structure
                if 'swagger' in data or 'openapi' in data:
                    print("✅ SUCCESS: Valid OpenAPI schema detected!")
                    
                    if 'paths' in data:
                        path_count = len(data['paths'])
                        print(f"✅ SUCCESS: Found {path_count} API endpoints!")
                    else:
                        print("⚠️  Warning: No 'paths' found in schema")
                        
                else:
                    print("⚠️  Warning: Not a valid OpenAPI schema")
                    
            except Exception as e:
                print(f"❌ FAILED: Invalid JSON - {e}")
                
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == '__main__':
    test_json_endpoint()
