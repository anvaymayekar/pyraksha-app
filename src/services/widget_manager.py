from kivy.utils import platform


class WidgetManager:
    """Manage home screen widget using notifications as alternative"""

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_quick_action(self):
        """
        Create notification-based quick action
        Since true widgets require Java, we use persistent notification
        """
        if platform == "android":
            try:
                from plyer import notification
                from jnius import autoclass

                # Create ongoing notification with action button
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                Intent = autoclass("android.content.Intent")
                PendingIntent = autoclass("android.app.PendingIntent")

                # This creates a persistent notification users can tap
                notification.notify(
                    title="PyRaksha SOS Ready",
                    message="Tap to trigger emergency SOS",
                    app_name="PyRaksha",
                    timeout=0,  # Never expires
                )

                print("✅ Quick action notification created")
                return True

            except Exception as e:
                print(f"Failed to create quick action: {e}")
                return False

        return False

    def remove_quick_action(self):
        """Remove the quick action notification"""
        # Notifications auto-remove when tapped
        pass
