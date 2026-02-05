from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from src.core.theme import Theme
from src.core.navigation import NavigationManager
from src.ui.components.custom_button import CustomButton
from src.ui.components.custom_input import CustomInput
from src.services.auth_service import AuthService
from src.state.session_manager import SessionManager
from src.state.app_state import AppState
from src.config.constants import ScreenNames


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ScreenNames.LOGIN

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
            text="Welcome Back",
            font_size=Theme.font_size_xxl,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=60,
        )

        subtitle_label = Label(
            text="Login to continue",
            font_size=Theme.font_size_md,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=30,
        )

        self.email_input = CustomInput(hint_text="Email")
        self.password_input = CustomInput(hint_text="Password", password=True)

        self.error_label = Label(
            text="",
            font_size=Theme.font_size_sm,
            color=Theme.danger,
            size_hint_y=None,
            height=30,
        )

        login_button = CustomButton(text="Login", bg_color=Theme.primary)
        login_button.bind(on_release=self._on_login)

        register_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=40,
            spacing=Theme.spacing_sm,
        )

        register_text = Label(
            text="Don't have an account?",
            font_size=Theme.font_size_sm,
            color=Theme.text_secondary,
            size_hint_x=0.6,
        )

        register_button = CustomButton(
            text="Register", bg_color=Theme.surface_elevated, text_color=Theme.accent
        )
        register_button.size_hint_x = 0.4
        register_button.bind(on_release=self._on_register)

        register_layout.add_widget(register_text)
        register_layout.add_widget(register_button)

        main_layout.add_widget(Label(size_hint_y=None, height=50))
        main_layout.add_widget(title_label)
        main_layout.add_widget(subtitle_label)
        main_layout.add_widget(Label(size_hint_y=None, height=30))
        main_layout.add_widget(self.email_input)
        main_layout.add_widget(self.password_input)
        main_layout.add_widget(self.error_label)
        main_layout.add_widget(login_button)
        main_layout.add_widget(Label(size_hint_y=None, height=20))
        main_layout.add_widget(register_layout)
        main_layout.add_widget(Label(size_hint_y=None, height=50))

        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _on_login(self, instance):
        self.error_label.text = ""

        email = self.email_input.text.strip()
        password = self.password_input.text

        auth_service = AuthService.get_instance()
        success, message, user = auth_service.login(email, password)

        if success and user:
            session_manager = SessionManager.get_instance()
            session_manager.save_session(user)

            app_state = AppState.get_instance()
            app_state.set_user(user)

            nav_manager = NavigationManager.get_instance()
            nav_manager.navigate_to(ScreenNames.HOME)
        else:
            self.error_label.text = message

    def _on_register(self, instance):
        nav_manager = NavigationManager.get_instance()
        nav_manager.navigate_to(ScreenNames.REGISTER)

    def on_enter(self, *args):
        self.email_input.text = ""
        self.password_input.text = ""
        self.error_label.text = ""
