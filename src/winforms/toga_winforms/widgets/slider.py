from travertino.size import at_least
from toga_winforms.libs import WinForms
from toga_winforms import color
from .base import Widget


class TogaSlider(WinForms.TrackBar):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.Scroll += self.on_slide

    def on_slide(self, sender, event):
        if self.interface.on_slide:
            self.interface.on_slide(self.interface)


class Slider(Widget):
    def create(self):
        self.native = TogaSlider(self.interface)
        self.set_enabled(self.interface._enabled)

    def get_value(self):
        return self.native.Value

    def set_value(self, value):
        self.native.Value = value

    def set_range(self, range):
        # TODO: Should I use self.interface.range etc for the values?
        self.native.Minimum = range[0]
        self.native.Maximum = range[1]

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_on_slide(self, handler):
        pass
