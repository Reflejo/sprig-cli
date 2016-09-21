# -*- encoding: UTF-8
import base
import colors
import urwid

from widgets import Button


class MenuUI(base.BodyUI):

    signals = ["order", "increment", "decrement", "view_photo", "describe"]

    def __init__(self):
        self.items = []

        pile = urwid.Pile([])
        super(MenuUI, self).__init__(pile, valign="middle")

    def set_items(self, items):
        widgets = []
        self.items = sorted(items, key=lambda x: not x.is_meal)
        for item in self.items:
            tcolor = colors.ITEM_MEAL if item.is_meal else colors.ITEM_NOMEAL
            order = Button("+", "increment", item, self)
            remove = Button("-", "decrement", item, self)
            see_photo = Button("❏", "view_photo", item, self)

            title = Button(item.title, "describe", item, self, left="",
                           right="", align="left", color=tcolor,
                           focus=colors.ITEM_FOCUS)

            columns = urwid.Columns([
                ("fixed", 2, urwid.Text("")),
                ("weight", 0.7, title),
                ("fixed", 5, order),
                ("fixed", 5, remove),
                ("fixed", 2, urwid.Divider()),
                ("fixed", 5, see_photo),
            ], focus_column=2)
            widgets.append(columns)

        widgets += [urwid.Divider()]
        widgets += [urwid.Divider()]

        self.body = urwid.Columns([
            ("weight", 0.1, urwid.Divider()),
            ("weight", 0.8, urwid.Pile(widgets)),
            ("weight", 0.1, urwid.Divider()),
        ])

    def set_order_visible(self, visible, scheduled=False):
        text = "Order when ready" if scheduled else "Order"
        size = len(text) + 4

        columns = urwid.Columns([
            ("weight", 1, urwid.Divider()),
            ("fixed", size, Button(text, "order", scheduled, self))
        ])
        row = columns if visible else urwid.Divider()
        self.body[1].contents[-1] = row, ("weight", 1)

    def set_item_count(self, item, count, available=True):
        idx = self.items.index(item)
        _, count_pos = self.body[1][idx].contents[0]
        button, _ = self.body[1][idx].contents[1]
        if not available:
            color = colors.ITEM_UNAVAILABLE
        elif count > 0:
            color = colors.ITEM_SELECTED
        elif item.is_meal:
            color = colors.ITEM_MEAL
        else:
            color = colors.ITEM_NOMEAL

        button.set_color(color)

        count_string = str(count) if count else ""
        count_label = colors.wrap(urwid.Text(count_string), color)
        self.body[1][idx].contents[0] = count_label, count_pos

    def show_closed(self):
        fonts = urwid.get_all_fonts()

        text = urwid.Text("Kitchen is closed, come back tomorrow!",
                          align="center")
        self.body = colors.wrap(text, colors.ERROR)
