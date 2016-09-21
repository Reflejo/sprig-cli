# -*- encoding: UTF-8

import colors
import urwid

from widgets import PopUp


class ItemDescription(PopUp):

    shown_properties = [
        ("Calories", "calories"),
        ("Sugar", "sugar"),
        ("Fiber", "fiber"),
        ("Sodium", "sodium"),
        ("Fat", "fat"),
        ("Protein", "protein"),
        ("Carbs", "carbohydrates"),
    ]

    width = 50

    def __init__(self, item):
        ui = self.ui_for_item(item)
        vertical, horizontal = self.body_delta
        height = ui.rows((self.width - vertical, )) + horizontal
        self.__super.__init__(ui, self.width, height, title=item.title)

    def _property_column(self, name, value):
        name = urwid.Text(name)
        value = urwid.Text(value, align="right")
        return urwid.Columns([
            ("weight", 0.5, colors.wrap(name, colors.PROPERTY_NAME)),
            ("fixed", 1, urwid.Divider()),
            ("weight", 0.5, colors.wrap(value, colors.PROPERTY)),
        ])

    def ui_for_item(self, item):
        cols = [self._property_column(name, getattr(item, key))
                for name, key in self.shown_properties if getattr(item, key)]

        details = urwid.Text(item.details, align="center")
        properties = urwid.GridFlow(cols, 18, 6, 0, "left")
        sections = urwid.Pile([
            urwid.Divider(),
            urwid.Padding(colors.wrap(details, colors.LOW), left=1, right=1),
            colors.wrap(urwid.Divider('─', top=1, bottom=1), colors.BOX),
            urwid.Padding(properties, left=2),
        ])

        return sections
