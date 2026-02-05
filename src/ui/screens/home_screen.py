from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from src.core.theme import Theme
from src.core.navigation import NavigationManager
from src.ui.components.custom_button import CustomButton
from src.ui.components.sos_button import SOSButton
from src.state.app_state import AppState
from src.services.sos_service import SOSService
from src.config.constants import ScreenNames


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ScreenNames.HOME

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

        self.welcome_label = Label(
            text="Welcome",
            font_size=Theme.font_size_xl,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=15,
        )

        subtitle_label = Label(
            text="Your safety is our priority",
            font_size=Theme.font_size_md,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=10,
            valign="top",
        )

        sos_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=200,
            spacing=Theme.spacing_md,
        )

        sos_label = Label(
            text="Emergency Button",
            font_size=Theme.font_size_lg,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=30,
        )

        sos_button_container = BoxLayout(size_hint_y=None, height=Theme.sos_button_size)

        self.sos_button = SOSButton()
        self.sos_button.bind(on_release=self._on_sos_trigger)

        sos_button_container.add_widget(Label())
        sos_button_container.add_widget(self.sos_button)
        sos_button_container.add_widget(Label())

        sos_container.add_widget(sos_label)
        sos_container.add_widget(sos_button_container)

        quick_actions_label = Label(
            text="Quick Actions",
            font_size=Theme.font_size_lg,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=40,
        )

        complaint_button = CustomButton(text="File Complaint", bg_color=Theme.primary)
        complaint_button.bind(on_release=self._on_file_complaint)

        view_complaints_button = CustomButton(
            text="View Complaints",
            bg_color=Theme.surface_elevated,
            text_color=Theme.accent,
        )
        view_complaints_button.bind(on_release=self._on_view_complaints)

        profile_button = CustomButton(
            text="Profile",
            bg_color=Theme.surface_elevated,
            text_color=Theme.text_primary,
        )
        profile_button.bind(on_release=self._on_profile)

        main_layout.add_widget(Label(size_hint_y=None, height=20))
        main_layout.add_widget(self.welcome_label)
        main_layout.add_widget(subtitle_label)
        main_layout.add_widget(Label(size_hint_y=None, height=30))
        main_layout.add_widget(sos_container)
        main_layout.add_widget(Label(size_hint_y=None, height=30))
        main_layout.add_widget(quick_actions_label)
        main_layout.add_widget(complaint_button)
        main_layout.add_widget(view_complaints_button)
        main_layout.add_widget(profile_button)
        main_layout.add_widget(Label(size_hint_y=None, height=50))

        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _on_sos_trigger(self, instance):
        nav_manager = NavigationManager.get_instance()
        nav_manager.navigate_to(ScreenNames.SOS)

    def _on_file_complaint(self, instance):
        nav_manager = NavigationManager.get_instance()
        nav_manager.navigate_to(ScreenNames.COMPLAINT)

    def _on_view_complaints(self, instance):
        nav_manager = NavigationManager.get_instance()
        nav_manager.navigate_to(ScreenNames.COMPLAINT_LIST)

    def _on_profile(self, instance):
        nav_manager = NavigationManager.get_instance()
        nav_manager.navigate_to(ScreenNames.PROFILE)

    def on_enter(self, *args):
        app_state = AppState.get_instance()
        if app_state.current_user:
            self.welcome_label.text = f"Welcome, {app_state.current_user.name}"
