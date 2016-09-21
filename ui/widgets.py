# -*- encoding: UTF-8

import base
import colors
import itertools
import urwid


class Button(urwid.WidgetWrap):

    def __init__(self, text, signal, data=None, delegate=None, align="center",
                 left="<", right=">", color=colors.BUTTONS,
                 focus=colors.BUTTONS_FOCUS):
        urwid.Button.button_left = urwid.Text(left)
        urwid.Button.button_right = urwid.Text(right)

        if callable(signal):
            self._button = urwid.Button(text, signal, user_data=data)
        else:
            self._button = urwid.Button(text, user_data=data)
            urwid.connect_signal(self._button, 'click',
                                 self._hook(signal, data, delegate))

        super(Button, self).__init__(None)
        self.set_color(color, focus)

        self._button._label.align = align
        self.enabled = True

    def set_color(self, normal_color, focus_color=None):
        self._color = normal_color
        self._focus_color = focus_color or self._focus_color
        self._w = colors.wrap(self._button, normal_color, self._focus_color)

    def selectable(self):
        return self._enabled

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self._enabled = enabled

        color = self._color if enabled else colors.BUTTON_DISABLED
        focus = self._focus_color if enabled else None
        self._w = colors.wrap(self._button, color, focus)

    def _hook(self, signal, data, delegate):
        def closure(button):
            args = filter(lambda x: x is not None, [signal, data])
            (delegate or self)._emit(*args)

        return closure


class ColoredText(urwid.AttrWrap):

    def __init__(self, text, color, align="left"):
        label = urwid.Text(text, align=align)
        super(ColoredText, self).__init__(label, color)


class ColoredLineBox(urwid.LineBox):

    def __init__(self, *args, **kwargs):
        color = kwargs.pop("color", colors.BOX)
        title_color = kwargs.pop("title_color", colors.TITLE_BOX)

        super(ColoredLineBox, self).__init__(*args, **kwargs)
        self.set_color(color, title_color)

    def set_color(self, color, title_color):
        for (row, col) in itertools.product(xrange(3), xrange(3)):
            if row == 1 and col == 1:
                continue

            line, space = self._w[row].contents[col]
            self._w[row].contents[col] = colors.wrap(line, color), space

        title_color = title_color or color
        title, space = self.tline_widget.contents[1]
        self.tline_widget.contents[1] = colors.wrap(title, title_color), space


class PopUp(urwid.WidgetWrap, base.SignalEmitter):

    _sizing = frozenset([urwid.FIXED])
    signals = ['close']
    body_delta = (4, 5)

    def _truncate(self, text, width):
        n = width - 7
        return (text[:n - 2] + u' …') if text and len(text) > n else text

    def __init__(self, body, width, height, title=None):
        self.size = (width, height)
        self.body = body

        title = self._truncate(title, width) or ""
        filler = colors.wrap(urwid.Filler(body), colors.DIALOG_BODY)
        self.frame = urwid.Frame(filler, focus_part='footer')
        box = ColoredLineBox(self.frame, title=title)

        # Dialog's shadow effect
        shadow = urwid.Text(('', '  '))
        bottom_shadow = colors.wrap(shadow, colors.DIALOG_SHADOW)
        left_shadow = urwid.Filler(shadow, "top")
        w = urwid.Columns([
            box,
            ('fixed', 2, colors.wrap(left_shadow, colors.DIALOG_SHADOW))
        ])

        self.__super.__init__(urwid.Frame(w, footer=bottom_shadow))
        self.add_buttons([Button("OK", "close", delegate=self)])

    def add_buttons(self, buttons):
        self.buttons = urwid.GridFlow(buttons, 10, 3, 1, 'center')
        self.frame.footer = urwid.Pile([urwid.Divider(), self.buttons],
                                       focus_item=1)
