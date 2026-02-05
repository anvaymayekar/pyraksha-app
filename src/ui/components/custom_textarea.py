from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.core.text import Label as CoreLabel
from src.core.theme import Theme


class CustomTextArea(TextInput):
    def __init__(self, hint_text: str = "", **kwargs):
        super().__init__(**kwargs)
        self.hint_text = hint_text
        self.multiline = True
        self.font_size = Theme.font_size_md
        self.padding = [Theme.spacing_md, Theme.spacing_md]

        # Disable Kivy's default background
        self.background_normal = ""
        self.background_active = ""
        self.background_color = [0, 0, 0, 0]

        # Set text colors
        self.foreground_color = Theme.text_primary
        self.disabled_foreground_color = Theme.text_primary
        self.cursor_color = Theme.accent
        self.selection_color = Theme.accent[:3] + [0.3]
        self.cursor_width = 2

        # Bind to updates
        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self.bind(text=self._update_canvas)
        self.bind(focus=self._update_canvas)

        self._update_canvas()

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()

        with self.canvas.before:
            # Background
            Color(*Theme.surface_elevated)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[Theme.card_radius])

            # Border when focused
            if self.focus:
                Color(*Theme.accent)
                Line(
                    rounded_rectangle=(
                        self.x,
                        self.y,
                        self.width,
                        self.height,
                        Theme.card_radius,
                    ),
                    width=2,
                )

        # Handle text display when defocused
        if self.text and not self.focus:
            with self.canvas.after:
                Color(*Theme.text_primary)
                # For multiline, we need to handle text wrapping
                label = CoreLabel(
                    text=self.text,
                    font_size=self.font_size,
                    text_size=(
                        self.width - 2 * Theme.spacing_md,
                        None,
                    ),  # Enable wrapping
                )
                label.refresh()
                texture = label.texture
                Rectangle(
                    texture=texture,
                    size=texture.size,
                    pos=(
                        self.x + Theme.spacing_md,
                        self.y + self.height - texture.height - Theme.spacing_md,
                    ),
                )
        elif not self.text and not self.focus:
            # Show placeholder
            with self.canvas.after:
                Color(*Theme.text_secondary)
                label = CoreLabel(
                    text=self.hint_text,
                    font_size=self.font_size,
                    text_size=(self.width - 2 * Theme.spacing_md, None),
                )
                label.refresh()
                texture = label.texture
                Rectangle(
                    texture=texture,
                    size=texture.size,
                    pos=(
                        self.x + Theme.spacing_md,
                        self.y + self.height - texture.height - Theme.spacing_md,
                    ),
                )
