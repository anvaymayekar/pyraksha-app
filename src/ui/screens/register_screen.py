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
from src.config.constants import ScreenNames


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ScreenNames.REGISTER

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
            text="Create Account",
            font_size=Theme.font_size_xxl,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=60,
        )

        subtitle_label = Label(
            text="Join PyRaksha today",
            font_size=Theme.font_size_md,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=30,
        )

        self.name_input = CustomInput(hint_text="Full Name")
        self.email_input = CustomInput(hint_text="Email")
        self.phone_input = CustomInput(hint_text="Phone Number")
        self.password_input = CustomInput(hint_text="Password", password=True)
        self.confirm_password_input = CustomInput(
            hint_text="Confirm Password", password=True
        )

        self.error_label = Label(
            text="",
            font_size=Theme.font_size_sm,
            color=Theme.danger,
            size_hint_y=None,
            height=30,
        )

        register_button = CustomButton(text="Register", bg_color=Theme.primary)
        register_button.bind(on_release=self._on_register)

        login_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=40,
            spacing=Theme.spacing_sm,
        )

        login_text = Label(
            text="Already have an account?",
            font_size=Theme.font_size_sm,
            color=Theme.text_secondary,
            size_hint_x=0.6,
        )

        login_button = CustomButton(
            text="Login", bg_color=Theme.surface_elevated, text_color=Theme.accent
        )
        login_button.size_hint_x = 0.4
        login_button.bind(on_release=self._on_login)

        login_layout.add_widget(login_text)
        login_layout.add_widget(login_button)

        main_layout.add_widget(Label(size_hint_y=None, height=30))
        main_layout.add_widget(title_label)
        main_layout.add_widget(subtitle_label)
        main_layout.add_widget(Label(size_hint_y=None, height=20))
        main_layout.add_widget(self.name_input)
        main_layout.add_widget(self.email_input)
        main_layout.add_widget(self.phone_input)
        main_layout.add_widget(self.password_input)
        main_layout.add_widget(self.confirm_password_input)
        main_layout.add_widget(self.error_label)
        main_layout.add_widget(register_button)
        main_layout.add_widget(Label(size_hint_y=None, height=20))
        main_layout.add_widget(login_layout)
        main_layout.add_widget(Label(size_hint_y=None, height=30))

        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _on_register(self, instance):
        self.error_label.text = ""

        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        phone = self.phone_input.text.strip()
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if password != confirm_password:
            self.error_label.text = "Passwords do not match"
            return

        auth_service = AuthService.get_instance()
        success, message, user = auth_service.register(name, email, phone, password)

        if success:
            nav_manager = NavigationManager.get_instance()
            nav_manager.navigate_to(ScreenNames.LOGIN)
        else:
            self.error_label.text = message

    def _on_login(self, instance):
        nav_manager = NavigationManager.get_instance()
        nav_manager.go_back()

    def on_enter(self, *args):
        self.name_input.text = ""
        self.email_input.text = ""
        self.phone_input.text = ""
        self.password_input.text = ""
        self.confirm_password_input.text = ""
        self.error_label.text = ""
