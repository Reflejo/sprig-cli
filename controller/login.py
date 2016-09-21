import gevent
import os

from .base import Controller
from sprig import NotLoggedInError
from ui import LoginUI

CREDENTIALS_FILE = os.path.expanduser("~/.sprigpass")


class LoginController(Controller):

    signals = ["login"]

    def __init__(self, parent, sprig):
        super(LoginController, self).__init__()
        self.main = parent
        self._sprig = sprig

        self._ui = LoginUI()
        self._ui.connect_signal("login", self._login_pressed)
        self._restore_if_saved()

    def _restore_if_saved(self):
        if not os.path.exists(CREDENTIALS_FILE):
            return

        content = open(CREDENTIALS_FILE).read()
        content = content.strip().split(":")
        if len(content) == 2 and all(content):
            self._ui.email = content[0]
            self._ui.password = content[-1]
            self._ui.remember = True
            self._login_pressed(self._ui)

    def _login_pressed(self, login_ui):
        user, password = login_ui.email, login_ui.password
        gevent.spawn(self._login, user, password, login_ui.remember).start()

    def _login(self, user, password, remember):
        self._ui.set_hidden(True)
        self.main.footer.set_loading(True)

        try:
            self._sprig.login(user, password)
        except NotLoggedInError, e:
            user = password = None
            self.main.footer.show_error(str(e))
            self._ui.set_hidden(False)
            return

        finally:
            content = "%s:%s" % (user, password) if user and remember else ""
            open(CREDENTIALS_FILE, "w").write(content)
            os.chmod(CREDENTIALS_FILE, 0600)

        self.main.footer.set_loading(False)
        self._emit("login")

    def __repr__(self):
        return r"LoginController(%r, ***)" % self.user.email
