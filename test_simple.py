import urllib.request
import urllib.error

def test_production_swagger():
    url = 'https://moodify-wmcd.onrender.com/swagger/'
    
    try:
        # Create request without following redirects
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Python Test Client')
        
        # Open without following redirects  
        response = urllib.request.urlopen(request)
        
        print(f"Status: {response.getcode()}")
        print(f"URL: {response.geturl()}")
        
        # Check if it redirected
        if response.geturl() != url:
            print(f"Redirected from {url} to {response.geturl()}")
            
            if '/accounts/login/' in response.geturl():
                print("❌ STILL redirecting to login!")
                return False
            else:
                print("✅ Redirected but not to login")
                return True
        else:
            print("✅ Direct access successful")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        if hasattr(e, 'headers'):
            location = e.headers.get('Location')
            if location:
                print(f"Redirect location: {location}")
                if '/accounts/login/' in location:
                    print("❌ Still redirecting to login!")
                    return False
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    test_production_swagger()
