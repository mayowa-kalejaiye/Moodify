import requests

def test_swagger():
    url = 'https://moodify-wmcd.onrender.com/swagger/'
    
    try:
        response = requests.get(url, allow_redirects=False, timeout=30)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            print(f"Redirects to: {location}")
            
            if '/accounts/login/' in location:
                print("❌ STILL redirecting to login!")
            else:
                print("✅ Redirecting but not to login")
        elif response.status_code == 200:
            print("✅ SUCCESS: Direct access")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_swagger()
