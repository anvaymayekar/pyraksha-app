from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from src.core.theme import Theme
from src.core.navigation import NavigationManager
from src.ui.components.custom_button import CustomButton
from src.state.app_state import AppState
from src.state.session_manager import SessionManager
from src.services.auth_service import AuthService
from src.config.constants import ScreenNames


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ScreenNames.PROFILE

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

        title_label = Label(
            text="Profile",
            font_size=Theme.font_size_xxl,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=60,
        )

        profile_card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=250,
            padding=Theme.spacing_lg,
            spacing=Theme.spacing_md,
        )

        with profile_card.canvas.before:
            Color(*Theme.surface_elevated)
            profile_card.bg = RoundedRectangle(
                pos=profile_card.pos, size=profile_card.size, radius=[Theme.card_radius]
            )
        profile_card.bind(
            pos=lambda *args: setattr(profile_card.bg, "pos", profile_card.pos),
            size=lambda *args: setattr(profile_card.bg, "size", profile_card.size),
        )

        self.name_label = Label(
            text="Name: --",
            font_size=Theme.font_size_lg,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=40,
            halign="left",
        )
        self.name_label.bind(size=self.name_label.setter("text_size"))

        self.email_label = Label(
            text="Email: --",
            font_size=Theme.font_size_md,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=30,
            halign="left",
        )
        self.email_label.bind(size=self.email_label.setter("text_size"))

        self.phone_label = Label(
            text="Phone: --",
            font_size=Theme.font_size_md,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=30,
            halign="left",
        )
        self.phone_label.bind(size=self.phone_label.setter("text_size"))

        self.member_since_label = Label(
            text="Member since: --",
            font_size=Theme.font_size_sm,
            color=Theme.text_disabled,
            size_hint_y=None,
            height=30,
            halign="left",
        )
        self.member_since_label.bind(size=self.member_since_label.setter("text_size"))

        profile_card.add_widget(self.name_label)
        profile_card.add_widget(self.email_label)
        profile_card.add_widget(self.phone_label)
        profile_card.add_widget(self.member_since_label)

        logout_button = CustomButton(text="Logout", bg_color=Theme.danger)
        logout_button.bind(on_release=self._on_logout)

        back_button = CustomButton(
            text="Back", bg_color=Theme.surface_elevated, text_color=Theme.text_primary
        )
        back_button.bind(on_release=self._on_back)

        main_layout.add_widget(Label(size_hint_y=None, height=20))
        main_layout.add_widget(title_label)
        main_layout.add_widget(Label(size_hint_y=None, height=20))
        main_layout.add_widget(profile_card)
        main_layout.add_widget(Label(size_hint_y=None, height=30))
        main_layout.add_widget(logout_button)
        main_layout.add_widget(back_button)
        main_layout.add_widget(Label(size_hint_y=None, height=50))

        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _on_logout(self, instance):
        session_manager = SessionManager.get_instance()
        session_manager.clear_session()

        app_state = AppState.get_instance()
        app_state.clear_all()

        nav_manager = NavigationManager.get_instance()
        nav_manager.reset_to_login()

    def _on_back(self, instance):
        nav_manager = NavigationManager.get_instance()
        nav_manager.go_back()

    def on_enter(self, *args):
        app_state = AppState.get_instance()
        if app_state.current_user:
            user = app_state.current_user
            self.name_label.text = f"Name: {user.name}"
            self.email_label.text = f"Email: {user.email}"
            self.phone_label.text = f"Phone: {user.phone}"
            self.member_since_label.text = (
                f"Member since: {user.created_at.strftime('%B %d, %Y')}"
            )
        else:
            self.name_label.text = "Name: --"
            self.email_label.text = "Email: --"
            self.phone_label.text = "Phone: --"
            self.member_since_label.text = "Member since: --"
