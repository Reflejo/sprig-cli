import base
import urwid
import colors

from controller.utils import pretty_date
from sprig.models import LineItem, Order
from widgets import ColoredLineBox, Button, ColoredText


class OrderUI(base.BodyUI):

    def __init__(self):
        super(OrderUI, self).__init__(urwid.Divider())

    def show_order(self, order, cta_title, cta_closure):
        widgets = []
        widgets += [urwid.Divider()]

        # Order Items
        for item in order.menu_items:
            quantity = str(item.cart_quantity)
            columns = urwid.Columns([
                ("fixed", 2, urwid.Text(quantity, align="right")),
                ("fixed", 1, urwid.Divider()),
                ("weight", 1, ColoredText(item.title, colors.ITEM_MEAL)),
            ])
            widgets += [columns]

        # Driver name
        if order.driver_name:
            driver_name = "Driver's name: %s" % order.driver_name
            driver_phone = "Driver's phone: %s" % order.driver_phone_number

            if order.status == Order.STATUS_UNRATED:
                eta_tpl = "Delivered: %s"
            else:
                eta_tpl = "Estimated Time: %s"

            ETA = eta_tpl % pretty_date(order.customer_eta * 60)
            widgets += [urwid.Divider()]
            widgets += [ColoredText(driver_name, colors.LOW)]
            widgets += [ColoredText(driver_phone, colors.LOW)]
            widgets += [ColoredText(ETA, colors.LOW)]

        # Address
        address = [(colors.DELIVER_LABEL, "Delivering to ")]
        address += [(colors.DELIVER_ADDRESS, order.address.street_address)]
        widgets += [urwid.Divider()]
        widgets += [urwid.Text(address)]

        # Track driver button
        cta = Button(cta_title, cta_closure)
        if order.driver_location and cta:
            columns = urwid.Columns([
                ("weight", 0.2, urwid.Divider()),
                ("weight", 0.6, cta),
                ("weight", 0.2, urwid.Divider()),
            ])
            widgets += [urwid.Divider()]
            widgets += [columns]
        else:
            widgets += [urwid.Divider()]
            widgets += [urwid.Text("Waiting for driver...", align="center")]

        pile = urwid.Pile(widgets)
        pile = urwid.Padding(pile, left=2, right=2)
        pile = urwid.Columns([
            ("weight", 0.2, urwid.Divider()),
            ("weight", 0.6, ColoredLineBox(pile, title="Food on your way!")),
            ("weight", 0.2, urwid.Divider()),
        ])

        self.body = pile

    def set_button(self, title, closure):
        self._button = urwid.Button(title, closure)
