import colors
import gevent
import itertools
import urwid


class Spinner(urwid.Text):

    def __init__(self, prefix, color=colors.SPINNER):
        self.animating = False
        self.color = color
        self.prefix = prefix
        super(Spinner, self).__init__("")

    def refresh(self, data):
        self.set_text((self.color, self.prefix + data))

    def toggle(self, start):
        self.start() if start else self.stop()

    def stop(self):
        if not self.animating:
            return

        self.process.kill()
        self.set_text("")
        self.animating = False

    def start(self):
        if self.animating:
            return

        self.animating = True
        self.refresh(".")
        self.process = gevent.spawn(self.spin)
        self.process.start()

    def spin(self, write_fd=None):
        for letter in itertools.cycle(["-", "\\", "|", "/"]):
            self.refresh(letter)
            gevent.sleep(0.3)

    __del__ = stop


class FooterUI(urwid.Columns):

    def __init__(self, text=""):
        self._left = urwid.Text("Press q to quit")
        self._right = urwid.Text("")
        super(FooterUI, self).__init__([self._left, self._right])

    def set_loading(self, loading, text="Loading... "):
        is_spinner = isinstance(self.left, Spinner)
        same_spinner = is_spinner and self.left.prefix == text
        if not is_spinner and not loading:
            return

        if not same_spinner:
            self.left = Spinner(text)

        self.left.toggle(loading)

    def show_error(self, error):
        self.left = urwid.Text((colors.ERROR, error))

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, value):
        if isinstance(self.left, Spinner):
            self.left.stop()

        self._left = value
        self.widget_list[0] = value or urwid.Divider()

    @right.setter
    def right(self, value):
        self._right = value
        self.widget_list[1] = value or urwid.Divider()
