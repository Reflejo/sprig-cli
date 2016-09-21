import base
import urwid
import colors

from widgets import ColoredLineBox, Button


class LoginUI(base.BodyUI):

    signals = ["login"]

    def __init__(self):
        super(LoginUI, self).__init__(self.ui)

    def focus_next(self):
        contents = self.body[1].contents
        if contents.focus == 6:
            return

        widget = None
        while not widget or isinstance(widget, urwid.Divider):
            contents.focus += 1
            widget = contents[contents.focus][0].base_widget

    def keypress(self, size, key):
        result = super(LoginUI, self).keypress(size, key)
        if key == 'enter' or key == 'tab':
            self.focus_next()
            return None

        return result

    def set_hidden(self, hidden):
        if hidden:
            self._ui = self.body
            self.set_body(urwid.Divider())
        else:
            self.set_body(self._ui)
            self._ui = None

    @property
    def ui(self):
        widgets = []
        widgets += [urwid.Divider(top=0)]
        widgets += [urwid.Edit("Email: ")]
        widgets += [urwid.Edit("Password: ", mask="*")]
        widgets += [urwid.Divider(top=0)]
        widgets += [urwid.CheckBox("Remember password")]
        widgets += [urwid.Divider(top=0)]
        widgets += [Button("Sign In", "login", delegate=self)]

        widgets = [colors.wrap(x, focus=colors.LOGIN_FIELDS_FOCUS)
                   for x in widgets]

        pile = urwid.Pile(widgets)
        pile = urwid.Padding(pile, left=2, right=2)
        pile = urwid.Columns([
            ("weight", 0.3, urwid.Divider()),
            ("weight", 0.3, ColoredLineBox(pile, title="Login")),
            ("weight", 0.3, urwid.Divider()),
        ])

        return pile

    @property
    def remember(self):
        return self.body[1][4].state

    @property
    def email(self):
        return self.body[1][1].edit_text

    @property
    def password(self):
        return self.body[1][2].edit_text

    @remember.setter
    def remember(self, value):
        self.body[1][4].state = value

    @email.setter
    def email(self, value):
        self.body[1][1].set_edit_text(value)

    @password.setter
    def password(self, value):
        self.body[1][2].set_edit_text(value)
