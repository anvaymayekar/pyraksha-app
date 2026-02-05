from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from src.core.theme import Theme
from src.core.navigation import NavigationManager
from src.ui.components.custom_button import CustomButton
from src.ui.components.location_display import LocationDisplay
from src.state.app_state import AppState
from src.services.sos_service import SOSService
from src.services.location_service import LocationService
from src.config.constants import ScreenNames


class SOSScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ScreenNames.SOS
        self._update_event = None

        with self.canvas.before:
            Color(*Theme.background)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        scroll_view = ScrollView()

        main_layout = BoxLayout(
            orientation="vertical",
            padding=Theme.spacing_xl,
            spacing=Theme.spacing_lg,
            size_hint_y=None,
        )
        main_layout.bind(minimum_height=main_layout.setter("height"))

        status_label = Label(
            text="SOS ACTIVE",
            font_size=Theme.font_size_xxl,
            bold=True,
            color=Theme.danger,
            size_hint_y=None,
            height=60,
        )

        info_label = Label(
            text="Emergency services have been notified",
            font_size=Theme.font_size_md,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=40,
        )

        self.timer_label = Label(
            text="Duration: 00:00:00",
            font_size=Theme.font_size_lg,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=50,
        )

        self.location_display = LocationDisplay()

        tracking_label = Label(
            text="Live location tracking is active",
            font_size=Theme.font_size_sm,
            color=Theme.success,
            size_hint_y=None,
            height=30,
        )

        resolve_button = CustomButton(text="RESOLVE SOS", bg_color=Theme.success)
        resolve_button.bind(on_release=self._on_resolve)

        cancel_note = Label(
            text="Tap above to mark this emergency as resolved",
            font_size=Theme.font_size_sm,
            color=Theme.text_disabled,
            size_hint_y=None,
            height=30,
        )

        main_layout.add_widget(Label(size_hint_y=None, height=50))
        main_layout.add_widget(status_label)
        main_layout.add_widget(info_label)
        main_layout.add_widget(Label(size_hint_y=None, height=30))
        main_layout.add_widget(self.timer_label)
        main_layout.add_widget(Label(size_hint_y=None, height=20))
        main_layout.add_widget(self.location_display)
        main_layout.add_widget(tracking_label)
        main_layout.add_widget(Label(size_hint_y=None, height=30))
        main_layout.add_widget(resolve_button)
        main_layout.add_widget(cancel_note)
        main_layout.add_widget(Label(size_hint_y=None, height=50))

        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _format_duration(self, seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def _update_sos_info(self, dt):
        sos_service = SOSService.get_instance()
        active_sos = sos_service.get_active_sos()

        if active_sos:
            duration = active_sos.get_duration_seconds()
            self.timer_label.text = f"Duration: {self._format_duration(duration)}"

            location_service = LocationService.get_instance()
            current_location = location_service.get_current_location()

            if current_location:
                self.location_display.update_location(current_location)
                sos_service.update_location(current_location)
        else:
            nav_manager = NavigationManager.get_instance()
            nav_manager.reset_to_home()

    def _on_resolve(self, instance):
        sos_service = SOSService.get_instance()
        success, message = sos_service.resolve_sos()

        if success:
            app_state = AppState.get_instance()
            app_state.clear_sos()

            nav_manager = NavigationManager.get_instance()
            nav_manager.reset_to_home()

    def on_enter(self, *args):
        app_state = AppState.get_instance()
        sos_service = SOSService.get_instance()
        location_service = LocationService.get_instance()

        if not sos_service.get_active_sos():
            if app_state.current_user:
                success, message, sos = sos_service.trigger_sos(
                    app_state.current_user.user_id
                )
                if success and sos:
                    app_state.set_sos(sos)
                    location_service.start_tracking()

        self._update_event = Clock.schedule_interval(self._update_sos_info, 1)

    def on_leave(self, *args):
        if self._update_event:
            self._update_event.cancel()
            self._update_event = None
