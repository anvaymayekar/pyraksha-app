from kivy.utils import platform
import threading
import time
from typing import Optional


class BackgroundService:
    """Handle background SOS triggering - SIMPLIFIED for stability"""

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start_service(self):
        """Start background service - DISABLED for now to prevent crashes"""
        print("⚠️ Background service disabled for stability")
        print("💡 SOS will work while app is open")
        # Don't start any background services for now
        # This prevents crashes on Android
        return

    def _start_desktop_service(self):
        """Start a daemon thread for desktop platforms"""

        def desktop_loop():
            while True:
                try:
                    time.sleep(60)
                    print("Desktop background tick")
                except Exception as e:
                    print(f"Desktop background service error: {e}")

        threading.Thread(target=desktop_loop, daemon=True).start()
        print("✅ Desktop background service started")

    def handle_widget_trigger(self):
        """Handle SOS trigger from widget"""
        print("⚠️ Widget trigger not implemented yet")
        # Will implement after core app is stable

    def _show_notification(self, title: str, message: str):
        """Show notification"""
        print(f"Notification: {title} - {message}")
