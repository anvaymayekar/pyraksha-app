from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from src.core.theme import Theme
from src.core.navigation import NavigationManager
from src.state.session_manager import SessionManager
from src.state.app_state import AppState
from src.config.constants import ScreenNames


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ScreenNames.SPLASH

        with self.canvas.before:
            Color(*Theme.background)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(
            orientation="vertical", padding=Theme.spacing_xl, spacing=Theme.spacing_lg
        )

        logo_label = Label(
            text="PyRaksha",
            font_size=Theme.font_size_xxxl,
            bold=True,
            color=Theme.primary,
            size_hint_y=None,
            height=100,
        )

        tagline_label = Label(
            text="Your Safety, Our Priority",
            font_size=Theme.font_size_lg,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=50,
        )

        layout.add_widget(Label())
        layout.add_widget(logo_label)
        layout.add_widget(tagline_label)
        layout.add_widget(Label())

        self.add_widget(layout)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_enter(self, *args):
        Clock.schedule_once(self._check_session, 2)

    def _check_session(self, dt):
        session_manager = SessionManager.get_instance()
        user = session_manager.load_session()

        app_state = AppState.get_instance()
        nav_manager = NavigationManager.get_instance()

        if user:
            app_state.set_user(user)
            nav_manager.navigate_to(ScreenNames.HOME)
        else:
            nav_manager.navigate_to(ScreenNames.LOGIN)
