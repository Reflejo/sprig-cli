import subprocess
import gevent
import os
import sys
import urwid

from .base import Controller
from .utils import run
from ui import MenuUI, ItemDescription
from models import Cart


class MenuController(Controller):

    signals = ["order", "confirm"]

    def __init__(self, parent, sprig, cart=None):
        super(MenuController, self).__init__()
        self.main = parent
        self.cart = cart or Cart(None, sprig.user.payment_description,
                                 sprig.user.default_address)
        self._sprig = sprig

        self._ui = MenuUI()
        self._ui.connect_signal("order", self._on_order)
        self._ui.connect_signal("increment", self._on_add)
        self._ui.connect_signal("decrement", self._on_remove)
        self._ui.connect_signal("view_photo", self._on_photo)
        self._ui.connect_signal("describe", self._on_describe)

    def _on_order(self, menu_ui, scheduled):
        self.cart.scheduled = scheduled
        self._emit("confirm", self.cart)

    def _on_photo(self, menu_ui, item):
        run(item.image_url)

    def _on_add(self, menu_ui, item):
        self.cart.items[item] += 1
        self._update_items()

    def _on_remove(self, menu_ui, item):
        self.cart.items[item] = max(self.cart.items[item] - 1, 0)
        self._update_items()

    def _on_describe(self, menu_ui, item):
        menu_ui.popup(ItemDescription(item))

    def show_menu(self):
        gevent.spawn(self._load_menu).start()

    def keypress(self, key):
        if key == "r":
            self.show_menu()

    def _update_items(self):
        if not self.cart.menu:
            return

        available = self.cart.order_is_available
        for item, count in self.cart.items.iteritems():
            self._ui.set_item_count(item, count, count == 0 or available)

        self.main.footer.right = urwid.Text(
            "%d item(s) in order" % self.cart.total, align="right")
        self._ui.set_order_visible(self.cart.total > 0, not available)
        self.main.footer.left = urwid.Text("Press q to quit, r to refresh")

    def _load_menu(self):
        self.main.footer.set_loading(True)

        try:
            self.cart.menu = self._sprig.menu()
        except Exception, e:
            self.main.footer.show_error(str(e))
            return

        finally:
            self.main.footer.set_loading(False)

        # Bail if there is an ongoing order.
        if self.cart.menu.order_status is not None:
            return self._emit("order")

        # Show banner if kitchen is closed
        if not self.cart.menu.open_now:
            return self._ui.show_closed()

        self._ui.set_items(self.cart.menu.items)
        self._update_items()
