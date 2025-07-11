import requests
import time
from datetime import datetime

def keep_alive():
    url = "https://moodify-wmcd.onrender.com/api/health/"
    
    print("🚀 Starting Render Keep-Alive")
    print("⏱️  Pinging every 10 minutes")
    print("🛑 Press Ctrl+C to stop\n")
    
    while True:
        try:
            start = time.time()
            response = requests.get(url, timeout=30)
            duration = time.time() - start
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"✅ [{timestamp}] Ping OK - {duration:.1f}s")
            
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"⚠️  [{timestamp}] Ping failed: {e}")
        
        # Wait 10 minutes (600 seconds)
        time.sleep(600)

if __name__ == "__main__":
    try:
        keep_alive()
    except KeyboardInterrupt:
        print("\n🛑 Keep-alive stopped")
