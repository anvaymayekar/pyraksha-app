from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from src.core.theme import Theme


class CustomButton(Button):
    def __init__(self, text: str = "", bg_color=None, text_color=None, **kwargs):
        super().__init__(**kwargs)

        self.text = text
        self.size_hint_y = None
        self.height = Theme.button_height
        self.font_size = Theme.font_size_md
        self.bold = True

        self._bg_color = bg_color or Theme.primary
        self._text_color = text_color or Theme.text_on_primary

        self.background_color = (0, 0, 0, 0)
        self.background_normal = ""
        self.background_down = ""
        self.color = self._text_color

        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self._update_canvas()

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self._bg_color)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[Theme.button_radius],
            )

    def on_press(self):
        self.canvas.before.clear()
        with self.canvas.before:
            darker = [c * 0.8 for c in self._bg_color[:3]] + [self._bg_color[3]]
            Color(*darker)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[Theme.button_radius],
            )

    def on_release(self):
        self._update_canvas()
