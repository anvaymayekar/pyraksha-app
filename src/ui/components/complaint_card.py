from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from src.core.theme import Theme
from src.models.complaint import Complaint


class ComplaintCard(BoxLayout):
    def __init__(self, complaint: Complaint, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = 150
        self.padding = [
            Theme.spacing_lg,
            Theme.spacing_lg,
            Theme.spacing_lg,
            Theme.spacing_lg,
        ]  # [left, top, right, bottom]
        self.spacing = Theme.spacing_sm

        self._complaint = complaint

        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self._update_canvas()

        title_label = Label(
            text=complaint.title,
            font_size=Theme.font_size_lg,
            bold=True,
            color=Theme.text_primary,
            size_hint_y=None,
            height=32,
            halign="left",
            valign="bottom",  # Changed from middle to bottom
        )
        title_label.bind(size=title_label.setter("text_size"))

        description_label = Label(
            text=complaint.description[:100]
            + ("..." if len(complaint.description) > 100 else ""),
            font_size=Theme.font_size_sm,
            color=Theme.text_secondary,
            size_hint_y=None,
            height=48,
            halign="left",
            valign="top",
        )
        description_label.bind(size=description_label.setter("text_size"))

        footer_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=24)

        date_label = Label(
            text=complaint.get_formatted_date(),
            font_size=Theme.font_size_sm,
            color=Theme.text_disabled,
            halign="left",
            valign="middle",
        )
        date_label.bind(size=date_label.setter("text_size"))

        status_label = Label(
            text=complaint.get_status_display(),
            font_size=Theme.font_size_sm,
            color=Theme.accent,
            halign="right",
            valign="middle",
        )
        status_label.bind(size=status_label.setter("text_size"))

        footer_layout.add_widget(date_label)
        footer_layout.add_widget(status_label)

        self.add_widget(title_label)
        self.add_widget(description_label)
        self.add_widget(footer_layout)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*Theme.surface_elevated)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[Theme.card_radius])
