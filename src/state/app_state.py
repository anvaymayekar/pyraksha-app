from typing import Optional, List
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from src.models.user import User
from src.models.sos import SOS
from src.models.complaint import Complaint


class AppState(EventDispatcher):
    _instance: Optional["AppState"] = None

    current_user = ObjectProperty(None, allownone=True)
    is_authenticated = BooleanProperty(False)
    active_sos = ObjectProperty(None, allownone=True)
    complaints = ListProperty([])

    def __init__(self):
        super().__init__()
        if AppState._instance is not None:
            raise RuntimeError("AppState is a singleton. Use get_instance()")

    @classmethod
    def get_instance(cls) -> "AppState":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_user(self, user: Optional[User]) -> None:
        self.current_user = user
        self.is_authenticated = user is not None

    def clear_user(self) -> None:
        self.current_user = None
        self.is_authenticated = False

    def set_sos(self, sos: Optional[SOS]) -> None:
        self.active_sos = sos

    def clear_sos(self) -> None:
        self.active_sos = None

    def add_complaint(self, complaint: Complaint) -> None:
        self.complaints.append(complaint)

    def set_complaints(self, complaints: List[Complaint]) -> None:
        self.complaints = complaints

    def clear_all(self) -> None:
        self.clear_user()
        self.clear_sos()
        self.complaints = []
