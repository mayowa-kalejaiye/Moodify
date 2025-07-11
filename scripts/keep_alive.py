#!/usr/bin/env python3
"""
Render Keep-Alive Script

This script sends periodic requests to your Render app to prevent it from 
going to sleep due to inactivity. Render free tier apps sleep after 15 
minutes of inactivity and take ~50 seconds to wake up.

Usage:
    python keep_alive.py

The script will run indefinitely, sending a request every 10 minutes.
Press Ctrl+C to stop.
"""

import requests
import time
import schedule
import threading
from datetime import datetime
import sys

class RenderKeepAlive:
    def __init__(self, app_url, ping_interval_minutes=10):
        self.app_url = app_url.rstrip('/')
        self.ping_interval = ping_interval_minutes
        self.health_endpoint = f"{self.app_url}/api/health/"
        self.running = True
        
    def ping_app(self):
        """Send a ping request to keep the app alive"""
        try:
            start_time = time.time()
            response = requests.get(self.health_endpoint, timeout=30)
            duration = time.time() - start_time
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if response.status_code == 200:
                print(f"✅ [{timestamp}] Ping successful - Response time: {duration:.2f}s")
            else:
                print(f"⚠️  [{timestamp}] Ping returned {response.status_code} - Response time: {duration:.2f}s")
                
        except requests.exceptions.Timeout:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"⏰ [{timestamp}] Ping timeout (>30s) - App might be sleeping, this is normal")
            
        except requests.exceptions.RequestException as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"❌ [{timestamp}] Ping failed: {e}")
    
    def start(self):
        """Start the keep-alive service"""
        print("🚀 Starting Render Keep-Alive Service")
        print(f"📡 Target: {self.health_endpoint}")
        print(f"⏱️  Interval: Every {self.ping_interval} minutes")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        # Schedule the ping
        schedule.every(self.ping_interval).minutes.do(self.ping_app)
        
        # Send initial ping
        print("🔄 Sending initial ping...")
        self.ping_app()
        
        # Run scheduler
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Keep-alive service stopped by user")
            self.running = False
    
    def run_in_background(self):
        """Run the keep-alive service in a background thread"""
        def background_worker():
            schedule.every(self.ping_interval).minutes.do(self.ping_app)
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        thread = threading.Thread(target=background_worker, daemon=True)
        thread.start()
        
        print(f"🔄 Keep-alive running in background (every {self.ping_interval} minutes)")
        return thread


def main():
    # Configuration
    APP_URL = "https://moodify-wmcd.onrender.com"
    PING_INTERVAL = 10  # minutes
    
    # Create and start keep-alive service
    keeper = RenderKeepAlive(APP_URL, PING_INTERVAL)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--background":
        # Run in background mode
        thread = keeper.run_in_background()
        
        print("Keep-alive service started in background.")
        print("The script will continue running. Press Ctrl+C to stop.")
        
        try:
            while keeper.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping keep-alive service...")
            keeper.running = False
    else:
        # Run in foreground mode
        keeper.start()


if __name__ == "__main__":
    main()
