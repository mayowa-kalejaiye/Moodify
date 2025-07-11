"""
Internal Keep-Alive Service for Render

This module provides a background service that runs within the Django application
to prevent Render free tier apps from going to sleep due to inactivity.

The service runs in a separate thread and sends periodic requests to the health endpoint.
"""

import requests
import time
import threading
from datetime import datetime
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class InternalKeepAlive:
    def __init__(self, ping_interval_minutes=10):
        self.ping_interval = ping_interval_minutes
        self.running = False
        self.thread = None
        
        # Determine the app URL from settings
        if hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
            # Find the production host
            production_host = None
            for host in settings.ALLOWED_HOSTS:
                if 'onrender.com' in host and not host.startswith('.'):
                    production_host = host
                    break
            
            if production_host:
                self.app_url = f"https://{production_host}"
            else:
                self.app_url = "https://moodify-wmcd.onrender.com"  # fallback
        else:
            self.app_url = "https://moodify-wmcd.onrender.com"  # fallback
            
        self.health_endpoint = f"{self.app_url}/api/health/"
        
    def ping_self(self):
        """Send a ping request to our own health endpoint"""
        try:
            start_time = time.time()
            response = requests.get(self.health_endpoint, timeout=30)
            duration = time.time() - start_time
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if response.status_code == 200:
                logger.info(f"Keep-alive ping successful - Response time: {duration:.2f}s")
            else:
                logger.warning(f"Keep-alive ping returned {response.status_code} - Response time: {duration:.2f}s")
                
        except requests.exceptions.Timeout:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.warning(f"Keep-alive ping timeout (>30s) - This is normal during cold starts")
            
        except requests.exceptions.RequestException as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"Keep-alive ping failed: {e}")
    
    def _background_worker(self):
        """Background worker that sends periodic pings"""
        logger.info(f"Keep-alive service started - pinging every {self.ping_interval} minutes")
        
        while self.running:
            try:
                self.ping_self()
                # Sleep for the interval (convert minutes to seconds)
                time.sleep(self.ping_interval * 60)
            except Exception as e:
                logger.error(f"Keep-alive service error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def start(self):
        """Start the keep-alive service in a background thread"""
        if self.running:
            logger.warning("Keep-alive service is already running")
            return
            
        # Only run in production (not in DEBUG mode)
        if getattr(settings, 'DEBUG', False):
            logger.info("Keep-alive service disabled in DEBUG mode")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._background_worker, daemon=True)
        self.thread.start()
        
        logger.info(f"Keep-alive service started for {self.app_url}")
    
    def stop(self):
        """Stop the keep-alive service"""
        if not self.running:
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            
        logger.info("Keep-alive service stopped")


# Global instance
_keep_alive_service = None

def start_keep_alive_service(ping_interval_minutes=10):
    """Start the global keep-alive service"""
    global _keep_alive_service
    
    if _keep_alive_service is None:
        _keep_alive_service = InternalKeepAlive(ping_interval_minutes)
    
    _keep_alive_service.start()

def stop_keep_alive_service():
    """Stop the global keep-alive service"""
    global _keep_alive_service
    
    if _keep_alive_service:
        _keep_alive_service.stop()
        _keep_alive_service = None
