from typing import Optional
from kivy.uix.screenmanager import ScreenManager, SlideTransition


class NavigationManager:
    _instance: Optional["NavigationManager"] = None

    def __init__(self, screen_manager: ScreenManager):
        self.screen_manager = screen_manager
        self._history: list[str] = []

    @classmethod
    def initialize(cls, screen_manager: ScreenManager) -> "NavigationManager":
        if cls._instance is None:
            cls._instance = cls(screen_manager)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "NavigationManager":
        if cls._instance is None:
            raise RuntimeError("NavigationManager not initialized")
        return cls._instance

    def navigate_to(self, screen_name: str, direction: str = "left") -> None:
        if self.screen_manager.current != screen_name:
            self._history.append(self.screen_manager.current)
            self.screen_manager.transition = SlideTransition(direction=direction)
            self.screen_manager.current = screen_name

    def go_back(self) -> None:
        if self._history:
            previous_screen = self._history.pop()
            self.screen_manager.transition = SlideTransition(direction="right")
            self.screen_manager.current = previous_screen

    def reset_to_home(self) -> None:
        self._history.clear()
        self.navigate_to("home", direction="left")

    def reset_to_login(self) -> None:
        self._history.clear()
        self.navigate_to("login", direction="left")
