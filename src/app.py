from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import traceback

from src.core.theme import Theme
from src.core.navigation import NavigationManager
from src.state.app_state import AppState
from src.config.constants import ScreenNames

# Screens - with error handling
try:
    from src.ui.screens.splash_screen import SplashScreen
    from src.ui.screens.login_screen import LoginScreen
    from src.ui.screens.register_screen import RegisterScreen
    from src.ui.screens.home_screen import HomeScreen
    from src.ui.screens.sos_screen import SOSScreen
    from src.ui.screens.complaint_screen import ComplaintScreen
    from src.ui.screens.complaint_list_screen import ComplaintListScreen
    from src.ui.screens.profile_screen import ProfileScreen

    SCREENS_IMPORTED = True
except Exception as e:
    print(f"ERROR importing screens: {e}")
    traceback.print_exc()
    SCREENS_IMPORTED = False

# Services - with error handling
try:
    from src.services.hardware_trigger_service import HardwareTriggerService

    HARDWARE_TRIGGER_AVAILABLE = True
except Exception as e:
    print(f"WARNING: Hardware trigger service not available: {e}")
    HARDWARE_TRIGGER_AVAILABLE = False

try:
    from src.services.background_service import BackgroundService

    BACKGROUND_SERVICE_AVAILABLE = True
except Exception as e:
    print(f"WARNING: Background service not available: {e}")
    BACKGROUND_SERVICE_AVAILABLE = False

try:
    from src.services.widget_manager import WidgetManager

    WIDGET_MANAGER_AVAILABLE = True
except Exception as e:
    print(f"WARNING: Widget manager not available: {e}")
    WIDGET_MANAGER_AVAILABLE = False

try:
    from src.services.sos_service import SOSService
    from src.services.location_service import LocationService

    CORE_SERVICES_AVAILABLE = True
except Exception as e:
    print(f"ERROR: Core services not available: {e}")
    traceback.print_exc()
    CORE_SERVICES_AVAILABLE = False


class PyRakshaApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "PyRaksha"
        # Don't require icon file - it may not exist
        # self.icon = "assets/icon.png"
        self._app_state = AppState.get_instance()
        self._nav_manager = None
        self._screen_manager = None

    def build(self):
        """Build the app UI"""
        try:
            print("Building PyRaksha App...")

            # Set dark background
            Window.clearcolor = Theme.background

            # Initialize screen manager
            self._screen_manager = ScreenManager()

            if not SCREENS_IMPORTED:
                print("CRITICAL: Screens not imported, cannot build app")
                raise ImportError("Failed to import screens")

            # Add screens with individual error handling
            try:
                self._screen_manager.add_widget(SplashScreen())
                print("✓ Added SplashScreen")
            except Exception as e:
                print(f"✗ Failed to add SplashScreen: {e}")
                traceback.print_exc()

            try:
                self._screen_manager.add_widget(LoginScreen())
                print("✓ Added LoginScreen")
            except Exception as e:
                print(f"✗ Failed to add LoginScreen: {e}")
                traceback.print_exc()

            try:
                self._screen_manager.add_widget(RegisterScreen())
                print("✓ Added RegisterScreen")
            except Exception as e:
                print(f"✗ Failed to add RegisterScreen: {e}")
                traceback.print_exc()

            try:
                self._screen_manager.add_widget(HomeScreen())
                print("✓ Added HomeScreen")
            except Exception as e:
                print(f"✗ Failed to add HomeScreen: {e}")
                traceback.print_exc()

            try:
                self._screen_manager.add_widget(SOSScreen())
                print("✓ Added SOSScreen")
            except Exception as e:
                print(f"✗ Failed to add SOSScreen: {e}")
                traceback.print_exc()

            try:
                self._screen_manager.add_widget(ComplaintScreen())
                print("✓ Added ComplaintScreen")
            except Exception as e:
                print(f"✗ Failed to add ComplaintScreen: {e}")
                traceback.print_exc()

            try:
                self._screen_manager.add_widget(ComplaintListScreen())
                print("✓ Added ComplaintListScreen")
            except Exception as e:
                print(f"✗ Failed to add ComplaintListScreen: {e}")
                traceback.print_exc()

            try:
                self._screen_manager.add_widget(ProfileScreen())
                print("✓ Added ProfileScreen")
            except Exception as e:
                print(f"✗ Failed to add ProfileScreen: {e}")
                traceback.print_exc()

            # Start at splash
            self._screen_manager.current = ScreenNames.SPLASH

            # Initialize navigation manager
            self._nav_manager = NavigationManager.initialize(self._screen_manager)
            print("✓ Navigation manager initialized")

            print("PyRaksha App built successfully!")
            return self._screen_manager

        except Exception as e:
            print(f"CRITICAL ERROR in build(): {e}")
            traceback.print_exc()
            raise

    def on_start(self):
        """Initialize services and triggers"""
        try:
            print("Starting PyRaksha services...")

            # Hardware SOS triggers (optional - may not work on all devices)
            if HARDWARE_TRIGGER_AVAILABLE:
                try:
                    trigger_service = HardwareTriggerService.get_instance()
                    trigger_service.start_listening(self._on_emergency_trigger)
                    print("✓ Hardware trigger service started")
                except Exception as e:
                    print(f"✗ Hardware trigger failed: {e}")
            else:
                print("⊗ Hardware trigger service disabled")

            # Background service (optional - disabled for stability)
            if BACKGROUND_SERVICE_AVAILABLE:
                try:
                    bg_service = BackgroundService.get_instance()
                    bg_service.start_service()
                    print("✓ Background service started")
                except Exception as e:
                    print(f"✗ Background service failed: {e}")
            else:
                print("⊗ Background service disabled")

            # Widget / quick action manager (optional)
            if WIDGET_MANAGER_AVAILABLE:
                try:
                    widget_manager = WidgetManager.get_instance()
                    widget_manager.create_quick_action()
                    print("✓ Widget manager started")
                except Exception as e:
                    print(f"✗ Widget manager failed: {e}")
            else:
                print("⊗ Widget manager disabled")

            # Location tracking (critical for SOS)
            if CORE_SERVICES_AVAILABLE:
                try:
                    location_service = LocationService.get_instance()
                    # Don't auto-start location tracking - only when SOS is triggered
                    # This saves battery and avoids permission issues on startup
                    print("✓ Location service ready (will start on SOS)")
                except Exception as e:
                    print(f"✗ Location service failed: {e}")
            else:
                print("⊗ Core services not available")

            print("PyRaksha initialized!")

        except Exception as e:
            print(f"ERROR in on_start(): {e}")
            traceback.print_exc()
            # Don't crash - let app continue even if services fail

    def _on_emergency_trigger(self):
        """Handle hardware SOS triggers"""
        try:
            user = self._app_state.current_user
            if not user:
                print("No user logged in for SOS")
                return

            if not CORE_SERVICES_AVAILABLE:
                print("SOS service not available")
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

                # Show notification if available
                if BACKGROUND_SERVICE_AVAILABLE:
                    try:
                        bg_service = BackgroundService.get_instance()
                        bg_service._show_notification(
                            "SOS ACTIVATED", "Emergency services have been notified"
                        )
                    except Exception as e:
                        print(f"Notification failed: {e}")
            else:
                print(f"SOS failed: {message}")

        except Exception as e:
            print(f"ERROR in _on_emergency_trigger: {e}")
            traceback.print_exc()

    def on_pause(self):
        """Handle app going to background"""
        print("App paused")
        return True  # Allow pause

    def on_resume(self):
        """Handle app coming from background"""
        print("App resumed")


if __name__ == "__main__":
    try:
        PyRakshaApp().run()
    except Exception as e:
        print(f"CRITICAL: App crashed: {e}")
        traceback.print_exc()
