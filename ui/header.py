# -*- encoding: UTF-8

import colors
import re
import os
import urwid

PATH = os.path.dirname(os.path.realpath(__file__))
LOGO_FILEPATH = os.path.join(PATH, "../resources/logo.ans")


class HeaderUI(urwid.Pile):

    def __init__(self):
        widgets = [urwid.Divider(), self._ansi_to_header()]
        self.__super.__init__(widgets)

    def _ansi_to_header(self, logo_file=LOGO_FILEPATH):
        logo = open(logo_file).read()
        parts = re.findall("\033\[([0-9;]+)m([^\033]+)", logo, re.DOTALL)
        markup = []
        for ansi, text in parts:
            attr = "default"
            if ansi.startswith("38;5"):
                attr = "h" + ansi[5:]

            markup.append((urwid.AttrSpec(attr, ''), text))

        return urwid.Text(markup, align="center")
