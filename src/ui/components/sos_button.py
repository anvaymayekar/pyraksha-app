from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation
from src.core.theme import Theme


class SOSButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text = "SOS"
        self.font_size = Theme.font_size_xxxl
        self.bold = True
        self.size_hint = (None, None)
        self.size = (Theme.sos_button_size, Theme.sos_button_size)

        self.background_color = (0, 0, 0, 0)
        self.background_normal = ""
        self.background_down = ""
        self.color = Theme.text_on_primary

        self._is_pulsing = False
        self._pulse_anim = None

        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self._update_canvas()

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*Theme.danger)
            Ellipse(pos=self.pos, size=self.size)

    def start_pulse(self):
        if self._is_pulsing:
            return

        self._is_pulsing = True
        self._pulse_anim = Animation(opacity=0.5, duration=0.8) + Animation(
            opacity=1.0, duration=0.8
        )
        self._pulse_anim.repeat = True
        self._pulse_anim.start(self)

    def stop_pulse(self):
        if self._pulse_anim:
            self._pulse_anim.cancel(self)
            self._pulse_anim = None

        self._is_pulsing = False
        self.opacity = 1.0

    def on_press(self):
        self.canvas.before.clear()
        with self.canvas.before:
            darker = [c * 0.7 for c in Theme.danger[:3]] + [Theme.danger[3]]
            Color(*darker)
            Ellipse(pos=self.pos, size=self.size)

    def on_release(self):
        self._update_canvas()
