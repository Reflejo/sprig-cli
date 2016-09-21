import urwid


class SignalEmitter(object):

    def connect_signal(self, signal, closure):
        urwid.connect_signal(self, signal, closure)


class BodyUI(urwid.Filler, SignalEmitter):

    def __init__(self, *args, **kwargs):
        self._popup_widget = None
        self.__super.__init__(*args, **kwargs)

    def popup(self, widget):
        self._popup_widget = widget
        widget.connect_signal("close", self.dismiss_popup)
        self._invalidate()

    def dismiss_popup(self, button=None):
        self._popup_widget = None
        self._invalidate()

    def render(self, size, focus=False):
        (width, height) = size
        canv = self.__super.render(size, focus)

        if self._popup_widget:
            (wwidth, wheight) = self._popup_widget.size
            canv = urwid.CompositeCanvas(canv)
            cols, rows = urwid.raw_display.Screen().get_cols_rows()
            x = (width / 2.) - (wwidth / 2.)
            y = (height / 2.) - (wheight / 2.) - 5.0 # Header half height
            canv.set_pop_up(self._popup_widget, x, y, wwidth, wheight)

        return canv

    def connect_signal(self, signal, closure):
        urwid.connect_signal(self, signal, closure)
