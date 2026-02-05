from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from src.core.theme import Theme
from src.models.location import Location


class LocationDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = 100
        self.padding = Theme.spacing_md
        self.spacing = Theme.spacing_sm

        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self._update_canvas()

        self._location_label = Label(
            text="Location: Not available",
            font_size=Theme.font_size_md,
            color=Theme.text_primary,
            halign="center",
            valign="middle",
        )
        self._location_label.bind(size=self._location_label.setter("text_size"))

        self._accuracy_label = Label(
            text="Accuracy: --",
            font_size=Theme.font_size_sm,
            color=Theme.text_secondary,
            halign="center",
            valign="middle",
        )
        self._accuracy_label.bind(size=self._accuracy_label.setter("text_size"))

        self.add_widget(self._location_label)
        self.add_widget(self._accuracy_label)

    def update_location(self, location: Location):
        if location:
            self._location_label.text = f"Location: {location.get_coordinates_string()}"
            if location.accuracy:
                self._accuracy_label.text = f"Accuracy: ±{location.accuracy:.1f}m"
            else:
                self._accuracy_label.text = "Accuracy: Unknown"
        else:
            self._location_label.text = "Location: Not available"
            self._accuracy_label.text = "Accuracy: --"

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*Theme.surface_elevated)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[Theme.card_radius])
