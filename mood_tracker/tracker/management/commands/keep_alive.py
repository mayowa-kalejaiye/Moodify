"""
Django management command to control the keep-alive service

Usage:
    python manage.py keep_alive start
    python manage.py keep_alive stop
    python manage.py keep_alive status
"""

from django.core.management.base import BaseCommand
from mood_tracker.tracker.keep_alive_service import start_keep_alive_service, stop_keep_alive_service, _keep_alive_service


class Command(BaseCommand):
    help = 'Control the Render keep-alive service'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['start', 'stop', 'status'],
            help='Action to perform on the keep-alive service'
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=10,
            help='Ping interval in minutes (default: 10)'
        )

    def handle(self, *args, **options):
        action = options['action']
        interval = options['interval']
        
        if action == 'start':
            self.stdout.write("Starting keep-alive service...")
            start_keep_alive_service(interval)
            self.stdout.write(
                self.style.SUCCESS(f"Keep-alive service started (interval: {interval} minutes)")
            )
            
        elif action == 'stop':
            self.stdout.write("Stopping keep-alive service...")
            stop_keep_alive_service()
            self.stdout.write(
                self.style.SUCCESS("Keep-alive service stopped")
            )
            
        elif action == 'status':
            global _keep_alive_service
            if _keep_alive_service and _keep_alive_service.running:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Keep-alive service is RUNNING (interval: {_keep_alive_service.ping_interval} minutes)\n"
                        f"Target: {_keep_alive_service.health_endpoint}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING("Keep-alive service is NOT running")
                )
