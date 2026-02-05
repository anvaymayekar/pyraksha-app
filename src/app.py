from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from src.core.theme import Theme
from src.core.navigation import NavigationManager
from src.state.app_state import AppState
from src.config.constants import ScreenNames

# Screens
from src.ui.screens.splash_screen import SplashScreen
from src.ui.screens.login_screen import LoginScreen
from src.ui.screens.register_screen import RegisterScreen
from src.ui.screens.home_screen import HomeScreen
from src.ui.screens.sos_screen import SOSScreen
from src.ui.screens.complaint_screen import ComplaintScreen
from src.ui.screens.complaint_list_screen import ComplaintListScreen
from src.ui.screens.profile_screen import ProfileScreen

# Services
from src.services.hardware_trigger_service import HardwareTriggerService
from src.services.background_service import BackgroundService
from src.services.widget_manager import WidgetManager
from src.services.sos_service import SOSService
from src.services.location_service import LocationService


class PyRakshaApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "PyRaksha"
        self.icon = "assets/icon.png"
        self._app_state = AppState.get_instance()
        self._nav_manager = None
        self._screen_manager = None

    def build(self):
        # Set dark background
        Window.clearcolor = Theme.background

        # Initialize screen manager
        self._screen_manager = ScreenManager()
        self._screen_manager.add_widget(SplashScreen())
        self._screen_manager.add_widget(LoginScreen())
        self._screen_manager.add_widget(RegisterScreen())
        self._screen_manager.add_widget(HomeScreen())
        self._screen_manager.add_widget(SOSScreen())
        self._screen_manager.add_widget(ComplaintScreen())
        self._screen_manager.add_widget(ComplaintListScreen())
        self._screen_manager.add_widget(ProfileScreen())

        # Start at splash
        self._screen_manager.current = ScreenNames.SPLASH

        # Initialize navigation manager
        self._nav_manager = NavigationManager.initialize(self._screen_manager)

        return self._screen_manager

    def on_start(self):
        """Initialize services and triggers"""

        # Hardware SOS triggers
        trigger_service = HardwareTriggerService.get_instance()
        trigger_service.start_listening(self._on_emergency_trigger)

        # Background service (notifications, background tasks)
        bg_service = BackgroundService.get_instance()
        bg_service.start_service()

        # Widget / quick action manager
        widget_manager = WidgetManager.get_instance()
        widget_manager.create_quick_action()

        # Location tracking (if needed)
        location_service = LocationService.get_instance()
        if not location_service.is_tracking:
            location_service.start_tracking()

        print("PyRaksha initialized with all services")

    def _on_emergency_trigger(self):
        """Handle hardware SOS triggers"""
        user = self._app_state.current_user
        if not user:
            print("No user logged in for SOS")
            return

        sos_service = SOSService.get_instance()
        if sos_service.get_active_sos():
            print("SOS already active")
            return

        success, message, sos = sos_service.trigger_sos(user.user_id)
        if success and sos:
            self._app_state.set_sos(sos)
            self._nav_manager.navigate_to(ScreenNames.SOS)
            print("SOS activated!")

            # Show notification
            bg_service = BackgroundService.get_instance()
            bg_service._show_notification(
                "SOS ACTIVATED", "Emergency services have been notified"
            )
        else:
            print(f"SOS failed: {message}")


if __name__ == "__main__":
    PyRakshaApp().run()
