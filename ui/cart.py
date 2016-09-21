import base
import urwid
import colors

from sprig.models import LineItem
from widgets import ColoredLineBox, Button, ColoredText

WARNING_TEXT = "Note that the selected combination of items is not available"\
               " right now but we'll keep trying till a driver is available."


class CartUI(base.BodyUI):

    signals = ["cancel", "order"]

    def __init__(self):
        super(CartUI, self).__init__(urwid.Divider())

    def show_confirmation(self, confirmation, cart):
        if confirmation is None:
            items = [LineItem.from_menu_item(item, count)
                     for item, count in cart.items.iteritems() if count > 0]
        else:
            items = confirmation.line_items

        address = cart.address.street_address
        self._show_confirmation(items, cart.payment, address,
                                confirmation is None)

    def set_order_enabled(self, enabled, allow_cancel=True):
        buttons = self.body[1][-1]
        order_btn_idx = len(buttons.contents) - 1
        cancel_btn_idx = 0

        buttons[order_btn_idx].enabled = enabled
        buttons[cancel_btn_idx].enabled = allow_cancel
        if allow_cancel:
            buttons.set_focus(order_btn_idx if enabled else cancel_btn_idx)

    def _show_confirmation(self, items, payment, address, scheduled=False):
        widgets = []
        widgets += [urwid.Divider()]

        # Add total as a line item
        total = LineItem({})
        total.price = sum(x.price * x.quantity for x in items)
        total.title = "Total"
        items.append(total)

        # Order Items
        for item in filter(lambda x: x.type == LineItem.TYPE_DISH, items):
            price = "%.2f" % (item.price / 100.0)
            columns = urwid.Columns([
                ("fixed", 2, urwid.Text(str(item.quantity), align="right")),
                ("fixed", 1, urwid.Divider()),
                ("weight", 1, ColoredText(item.title, colors.ITEM_MEAL)),
                ("fixed", 6, ColoredText(price, colors.PRICE, align="right")),
            ])
            widgets += [columns]

        # Total & Taxes
        widgets += [urwid.Divider()]
        for item in filter(lambda x: x.type != LineItem.TYPE_DISH, items):
            price = "%.2f" % (item.price / 100.0)
            title = item.title
            columns = urwid.Columns([
                ("weight", 1, ColoredText(title, colors.TAX, align="right")),
                ("fixed", 10, ColoredText(price, colors.PRICE, align="right")),
            ])
            widgets += [columns]

        # Payment method
        columns = urwid.Columns([
            ("weight", 0.5, ColoredText("Payment method", colors.LOW)),
            ("weight", 0.5, ColoredText(payment, colors.LOW, align="right")),
        ])
        widgets += [urwid.Divider()]
        widgets += [columns]

        # Address
        columns = urwid.Columns([
            ("weight", 0.5, ColoredText("Deliver to", colors.LOW)),
            ("weight", 0.5, ColoredText(address, colors.LOW, align="right")),
        ])
        widgets += [columns]

        # Delay warning
        if scheduled:
            warning_label = urwid.Text(WARNING_TEXT, align="center")
            widgets += [urwid.Divider()]
            widgets += [colors.wrap(warning_label, colors.WARNING)]

        # Order button
        text = "Order when ready" if scheduled else "Order"
        buttons = urwid.Columns([
            ("weight", 0.4, Button("Cancel", "cancel", delegate=self)),
            ("weight", 0.2, urwid.Divider()),
            ("weight", 0.4, Button(text, "order", delegate=self)),
        ], focus_column=2)
        widgets += [urwid.Divider()]
        widgets += [buttons]

        pile = urwid.Pile(widgets)
        pile = urwid.Padding(pile, left=2, right=2)
        pile = urwid.Columns([
            ("weight", 0.2, urwid.Divider()),
            ("weight", 0.6, ColoredLineBox(pile, title="Confirmation")),
            ("weight", 0.2, urwid.Divider()),
        ])

        self.body = pile
