from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from datetime import datetime
from typing import Optional, Callable


class HardwareTriggerService:
    """Trigger SOS using hardware button patterns"""

    _instance = None

    def __init__(self):
        self.press_count = 0
        self.last_press_time = None
        self.trigger_threshold = 5  # Press 5 times
        self.time_window = 3.0  # Within 3 seconds
        self.callback: Optional[Callable] = None
        self._reset_timer = None
        self._is_listening = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start_listening(self, callback: Callable):
        """Start listening for volume button pattern"""
        if self._is_listening:
            return

        self.callback = callback
        self._is_listening = True

        # Bind to keyboard events (includes volume buttons on Android)
        Window.bind(on_keyboard=self._on_keyboard)

        print("📱 Hardware trigger activated: Press volume down 5 times quickly")

    def stop_listening(self):
        """Stop listening for button presses"""
        if not self._is_listening:
            return

        Window.unbind(on_keyboard=self._on_keyboard)
        self._is_listening = False
        self._reset()

    def _on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle keyboard/volume button events"""
        # Volume button keycodes:
        # Android: 24 (volume up), 25 (volume down)
        # Desktop: 1073741899 (for testing)

        volume_keys = [24, 25, 1073741899, 1073741898]

        if key in volume_keys:
            self._on_button_press()
            return True  # Consume the event

        return False

    def _on_button_press(self):
        """Handle button press detection"""
        current_time = datetime.now()

        if self.last_press_time is None:
            # First press
            self.press_count = 1
            self.last_press_time = current_time
            self._schedule_reset()
            print(f"Button press 1/{self.trigger_threshold}")
        else:
            # Check if within time window
            time_diff = (current_time - self.last_press_time).total_seconds()

            if time_diff <= self.time_window:
                self.press_count += 1
                self.last_press_time = current_time
                print(f"Button press {self.press_count}/{self.trigger_threshold}")

                if self.press_count >= self.trigger_threshold:
                    # Pattern matched! Trigger SOS
                    self._trigger_sos()
                    self._reset()
                else:
                    self._schedule_reset()
            else:
                # Too slow, reset counter
                self.press_count = 1
                self.last_press_time = current_time
                self._schedule_reset()
                print(f"Too slow! Starting over: 1/{self.trigger_threshold}")

    def _schedule_reset(self):
        """Schedule automatic reset after time window"""
        if self._reset_timer:
            self._reset_timer.cancel()

        self._reset_timer = Clock.schedule_once(
            lambda dt: self._reset(), self.time_window
        )

    def _reset(self):
        """Reset press counter"""
        self.press_count = 0
        self.last_press_time = None
        if self._reset_timer:
            self._reset_timer.cancel()
            self._reset_timer = None

    def _trigger_sos(self):
        """Trigger SOS callback"""
        print("SOS PATTERN DETECTED! Triggering emergency...")

        # Vibrate to confirm (Android only)
        self._vibrate_confirm()

        # Call the callback
        if self.callback:
            Clock.schedule_once(lambda dt: self.callback(), 0)

    def _vibrate_confirm(self):
        """Vibrate phone to confirm SOS trigger"""
        if platform == "android":
            try:
                from jnius import autoclass

                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                Context = autoclass("android.content.Context")
                Vibrator = autoclass("android.os.Vibrator")

                activity = PythonActivity.mActivity
                vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)

                # Vibrate pattern: short-short-short (SOS in morse)
                if vibrator:
                    vibrator.vibrate(500)  # Vibrate for 500ms

            except Exception as e:
                print(f"Vibration failed: {e}")
