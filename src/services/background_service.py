from kivy.utils import platform
import threading
import time
from src.services.sos_service import SOSService
from src.state.app_state import AppState


class BackgroundService:
    """Handle background SOS triggering"""

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start_service(self):
        """Start background service"""
        if platform == "android":
            self._start_android_service()
        else:
            self._start_desktop_service()

    def _start_android_service(self):
        """Start Android background service using Python for Android"""
        try:
            from jnius import autoclass

            service = autoclass("org.kivy.android.PythonService")
            mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
            service.start(mActivity, "")
            print("✅ Android background service started")
        except Exception as e:
            print(f"Failed to start Android service: {e}")

    def _start_desktop_service(self):
        """Start a daemon thread for desktop platforms"""

        def desktop_loop():
            sos_service = SOSService.get_instance()
            app_state = AppState.get_instance()
            while True:
                try:
                    if app_state.current_user:
                        active_sos = sos_service.get_active_sos()
                        if active_sos:
                            print("Active SOS detected (desktop)")
                            # Optional: trigger desktop notification
                    time.sleep(60)
                except Exception as e:
                    print(f"Desktop background service error: {e}")

        threading.Thread(target=desktop_loop, daemon=True).start()
        print("✅ Desktop background service started")

    def handle_widget_trigger(self):
        """Handle SOS trigger from widget"""
        app_state = AppState.get_instance()
        sos_service = SOSService.get_instance()

        if app_state.current_user:
            success, message, sos = sos_service.trigger_sos(
                app_state.current_user.user_id
            )

            if success:
                app_state.set_sos(sos)
                self._show_notification("SOS Activated", "Emergency services notified")

    def _show_notification(self, title: str, message: str):
        """Show notification"""
        if platform == "android":
            try:
                from plyer import notification

                notification.notify(
                    title=title, message=message, app_name="PyRaksha", timeout=10
                )
            except Exception as e:
                print(f"Notification failed: {e}")
        else:
            print(f"Notification (desktop): {title} - {message}")
