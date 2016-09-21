import urwid

BOX = urwid.AttrSpec("h65", "")
TITLE_BOX = urwid.AttrSpec("g93, bold", "")
LOGIN_FIELDS_FOCUS = urwid.AttrSpec("dark green", "")
SPINNER = urwid.AttrSpec("#a06", "")
ERROR = urwid.AttrSpec("light red", "")
ITEM_MEAL = urwid.AttrSpec("h65", "")
ITEM_NOMEAL = urwid.AttrSpec("h66", "")
ITEM_FOCUS = urwid.AttrSpec("#6d6", "")
ITEM_SELECTED = urwid.AttrSpec("white, bold", "")
ITEM_UNAVAILABLE = urwid.AttrSpec("#800, bold", "")
BUTTONS = urwid.AttrSpec("h64", "")
BUTTONS_FOCUS = urwid.AttrSpec("white", "h64")
BUTTON_DISABLED = urwid.AttrSpec("g74", "")
WARNING = urwid.AttrSpec("dark red", "")
TITLE = urwid.AttrSpec("h64, bold", "")
PRICE = urwid.AttrSpec("white", "")
TAX = urwid.AttrSpec("h66", "")
LOW = urwid.AttrSpec("g50", "")
DELIVER_LABEL = urwid.AttrSpec("#080, bold", "")
DELIVER_ADDRESS = urwid.AttrSpec("#6d0, bold", "")
DIALOG_BODY = urwid.AttrSpec("", "black")
DIALOG_SHADOW = urwid.AttrSpec("", "g7")
PROPERTY = urwid.AttrSpec("#6d6", "")
PROPERTY_NAME = urwid.AttrSpec("#088", "")


def wrap(widget, color=None, focus=None):
    assert focus or color, "You should provide a fg or bg color"
    return urwid.AttrWrap(widget, color, focus)
