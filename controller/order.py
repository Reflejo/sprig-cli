import urwid
import gevent

from .base import Controller
from .utils import run
from ui import OrderUI
from sprig.models import Order

MAP_URL = "https://maps.google.com/maps?q=loc:{lat},{lng}"


class OrderController(Controller):

    signals = ["menu"]

    def __init__(self, parent, sprig, order):
        super(OrderController, self).__init__()
        self.main = parent

        self._order = order
        self._sprig = sprig
        self._last_computed_at = None
        self._ui = OrderUI()

    def show_order(self):
        if self._order:
            self._show_order(self._order)

        gevent.spawn(self._load_order).start()
        self.main.footer.right = None

    def _finish_order(self):
        self._sprig.finish(self._order.id)
        self._emit("menu")

    def _track_driver(self):
        pos = self._order.driver_location
        URL = MAP_URL.format(lat=pos["latitude"], lng=pos["longitude"])
        run(URL)

    def _show_order(self, order):
        if order.status == Order.STATUS_UNRATED:
            button_title = "Finish Order"
            button_closure = lambda x: self._finish_order()
        else:
            button_title = "See Driver's Position"
            button_closure = lambda x: self._track_driver()

        self._ui.show_order(order, button_title, button_closure)

    def _load_order(self):
        while True:
            self.main.footer.set_loading(True, "Tracking... ")

            try:
                self._order = self._sprig.track(self._last_computed_at)
                self._last_computed_at = self._order.last_computed_at
            except Exception, e:
                return self.main.footer.show_error(str(e))
            finally:
                self.main.footer.set_loading(False)

            self._show_order(self._order)
            gevent.sleep(10)
