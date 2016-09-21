import urwid
import gevent

from .base import Controller
from sprig import Sprig, MenuNotAvailable
from ui import CartUI


class CartController(Controller):

    signals = ["cancel", "order"]

    def __init__(self, parent, sprig, cart):
        super(CartController, self).__init__()
        self.cart = cart
        self.main = parent
        self.confirmation = None

        self._sprig = sprig
        self._ui = CartUI()
        self._ui.connect_signal("order", self._order_pressed)
        self._ui.connect_signal("cancel", self._cancel)

    def show_confirmation(self):
        gevent.spawn(self._load_confirmation).start()

    def _cancel(self, cart_ui):
        if getattr(self, '_waiting_greenlet', None):
            self._waiting_greenlet.kill()

        self._emit("cancel", self.cart)

    def _order_pressed(self, cart_ui):
        if self.confirmation is None:
            self._waiting_greenlet = gevent.spawn(self._wait_for_stock)
            self._waiting_greenlet.start()
        else:
            gevent.spawn(self._order).start()

    def _order(self):
        self.main.footer.set_loading(True, "Ordering... ")
        self._ui.set_order_enabled(False, allow_cancel=False)
        try:
            order = self._sprig.place_order(self.confirmation, self.cart.menu)
        except Exception, e:
            self._ui.set_order_enabled(True, allow_cancel=True)
            return self.main.footer.show_error(str(e))

        self.main.footer.set_loading(False)
        self._emit("order", order)

    def _retrying_in(self, n):
        for i in xrange(n):
            self.main.footer.set_loading(True, "Retrying in %d... " % (n - i))
            gevent.sleep(1)

    def _wait_for_stock(self):
        self.main.footer.set_loading(True, "Checking stock... ")
        self._ui.set_order_enabled(False)
        while True:
            try:
                self.confirmation = self._sprig.confirm(self.cart.menu,
                                                        self.cart.items)
            except MenuNotAvailable, e:
                self._retrying_in(30)
                continue

            except Exception, e:
                return self.main.footer.show_error(str(e))

            self.main.footer.set_loading(False)
            self._ui.set_order_enabled(True)
            return self._order_pressed(self._ui)

    def _load_confirmation(self):
        self.main.footer.set_loading(True, "Confirming... ")

        try:
            self.confirmation = self._sprig.confirm(self.cart.menu,
                                                    self.cart.items)
        except MenuNotAvailable, e:
            self.confirmation = None
        except Exception, e:
            return self.main.footer.show_error(str(e))
        finally:
            self.main.footer.set_loading(False)

        self._ui.show_confirmation(self.confirmation, self.cart)

        self.main.footer.left = urwid.Text("Press q to quit")
