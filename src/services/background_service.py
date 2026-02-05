from kivy.utils import platform


class BackgroundService:
    """Handle background SOS triggering"""

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start_service(self):
        """Start background service for widget clicks"""
        if platform == "android":
            self._start_android_service()

    def _start_android_service(self):
        """Start Android background service using Python for Android"""
        try:
            from jnius import autoclass

            # Get the service class
            service = autoclass("org.kivy.android.PythonService")
            mActivity = autoclass("org.kivy.android.PythonActivity").mActivity

            # Start the service
            argument = ""
            service.start(mActivity, argument)

            print("✅ Background service started")

        except Exception as e:
            print(f"Failed to start service: {e}")

    def handle_widget_trigger(self):
        """Handle SOS trigger from widget"""
        from src.services.sos_service import SOSService
        from src.state.app_state import AppState

        app_state = AppState.get_instance()
        sos_service = SOSService.get_instance()

        if app_state.current_user:
            success, message, sos = sos_service.trigger_sos(
                app_state.current_user.user_id
            )

            if success:
                app_state.set_sos(sos)
                # Send notification
                self._show_notification("SOS Activated", "Emergency services notified")

    def _show_notification(self, title: str, message: str):
        """Show notification (Android)"""
        if platform == "android":
            try:
                from plyer import notification

                notification.notify(
                    title=title, message=message, app_name="PyRaksha", timeout=10
                )
            except Exception as e:
                print(f"Notification failed: {e}")
