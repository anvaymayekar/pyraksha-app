from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from src.core.theme import Theme
from src.core.navigation import NavigationManager
from src.ui.components.custom_button import CustomButton
from src.ui.components.custom_input import CustomInput
from src.state.app_state import AppState
from src.services.complaint_service import ComplaintService
from src.config.constants import ScreenNames


class ComplaintScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ScreenNames.COMPLAINT

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
            text="File Complaint",
            font_size=Theme.font_size_xxl,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=60,
        )

        subtitle_label = Label(
            text="Describe your issue below",
            font_size=Theme.font_size_md,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=30,
        )

        self.title_input = CustomInput(hint_text="Complaint Title")

        description_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=180,
            spacing=Theme.spacing_xs,
        )

        description_label = Label(
            text="Description",
            font_size=Theme.font_size_sm,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=20,
            halign="left",
        )
        description_label.bind(size=description_label.setter("text_size"))

        # Import CustomTextArea
        from src.ui.components.custom_textarea import CustomTextArea

        self.description_input = CustomTextArea(
            hint_text="Describe your complaint in detail...",
            size_hint_y=None,
            height=150,
        )

        description_container.add_widget(description_label)
        description_container.add_widget(self.description_input)

        self.error_label = Label(
            text="",
            font_size=Theme.font_size_sm,
            color=Theme.danger,
            size_hint_y=None,
            height=30,
        )

        submit_button = CustomButton(text="Submit Complaint", bg_color=Theme.primary)
        submit_button.bind(on_release=self._on_submit)

        back_button = CustomButton(
            text="Back", bg_color=Theme.surface_elevated, text_color=Theme.text_primary
        )
        back_button.bind(on_release=self._on_back)

        main_layout.add_widget(Label(size_hint_y=None, height=20))
        main_layout.add_widget(title_label)
        main_layout.add_widget(subtitle_label)
        main_layout.add_widget(Label(size_hint_y=None, height=30))
        main_layout.add_widget(self.title_input)
        main_layout.add_widget(description_container)
        main_layout.add_widget(self.error_label)
        main_layout.add_widget(submit_button)
        main_layout.add_widget(back_button)
        main_layout.add_widget(Label(size_hint_y=None, height=50))

        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _on_submit(self, instance):
        self.error_label.text = ""

        title = self.title_input.text.strip()
        description = self.description_input.text.strip()

        app_state = AppState.get_instance()
        if not app_state.current_user:
            self.error_label.text = "User not authenticated"
            return

        complaint_service = ComplaintService.get_instance()
        success, message, complaint = complaint_service.file_complaint(
            app_state.current_user.user_id, title, description
        )

        if success and complaint:
            app_state.add_complaint(complaint)
            nav_manager = NavigationManager.get_instance()
            nav_manager.navigate_to(ScreenNames.COMPLAINT_LIST)
        else:
            self.error_label.text = message

    def _on_back(self, instance):
        nav_manager = NavigationManager.get_instance()
        nav_manager.go_back()

    def on_enter(self, *args):
        self.title_input.text = ""
        self.description_input.text = ""
        self.error_label.text = ""
