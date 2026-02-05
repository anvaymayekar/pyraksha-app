from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from src.core.theme import Theme
from src.core.navigation import NavigationManager
from src.ui.components.custom_button import CustomButton
from src.ui.components.complaint_card import ComplaintCard
from src.state.app_state import AppState
from src.services.complaint_service import ComplaintService
from src.config.constants import ScreenNames


class ComplaintListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ScreenNames.COMPLAINT_LIST

        with self.canvas.before:
            Color(*Theme.background)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        main_container = BoxLayout(orientation="vertical")

        header_layout = BoxLayout(
            orientation="vertical",
            padding=[
                Theme.spacing_xl,
                Theme.spacing_xl * 3,
                Theme.spacing_xl,
                Theme.spacing_xl,
            ],
            spacing=Theme.spacing_md,
            size_hint_y=None,
            height=170,
        )
        header_layout.add_widget(Label(size_hint_y=None, height=Theme.spacing_xxl))
        title_label = Label(
            text="My Complaints",
            font_size=Theme.font_size_xxl,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=50,
        )

        back_button = CustomButton(
            text="Back to Home",
            bg_color=Theme.surface_elevated,
            text_color=Theme.text_primary,
        )
        back_button.bind(on_release=self._on_back)

        header_layout.add_widget(title_label)
        header_layout.add_widget(back_button)

        self.scroll_view = ScrollView()

        self.complaints_layout = BoxLayout(
            orientation="vertical",
            padding=[Theme.spacing_xl, 0, Theme.spacing_xl, Theme.spacing_xl],
            spacing=Theme.spacing_md,
            size_hint_y=None,
        )
        self.complaints_layout.bind(
            minimum_height=self.complaints_layout.setter("height")
        )

        self.scroll_view.add_widget(self.complaints_layout)

        main_container.add_widget(header_layout)
        main_container.add_widget(self.scroll_view)

        self.add_widget(main_container)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _load_complaints(self):
        self.complaints_layout.clear_widgets()

        app_state = AppState.get_instance()
        if not app_state.current_user:
            no_user_label = Label(
                text="User not authenticated",
                font_size=Theme.font_size_md,
                color=Theme.text_secondary,
                size_hint_y=None,
                height=100,
            )
            self.complaints_layout.add_widget(no_user_label)
            return

        complaint_service = ComplaintService.get_instance()
        complaints = complaint_service.get_user_complaints(
            app_state.current_user.user_id
        )

        if not complaints:
            no_complaints_label = Label(
                text="No complaints filed yet",
                font_size=Theme.font_size_md,
                color=Theme.text_secondary,
                size_hint_y=None,
                height=100,
            )
            self.complaints_layout.add_widget(no_complaints_label)
        else:
            complaints.sort(key=lambda c: c.timestamp, reverse=True)

            for complaint in complaints:
                card = ComplaintCard(complaint=complaint)
                self.complaints_layout.add_widget(card)

    def _on_back(self, instance):
        nav_manager = NavigationManager.get_instance()
        nav_manager.go_back()

    def on_enter(self, *args):
        self._load_complaints()
