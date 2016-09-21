#!/usr/bin/env python
# -*- encoding: UTF-8

import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
gevent.monkey.patch_time()

import urwid

from controller.loop import GeventLoop
from controller import \
    LoginController, MenuController, CartController, OrderController
from ui import HeaderUI, FooterUI
from ui.footer import Spinner
from sprig import Sprig


class UIController(object):

    def __init__(self):
        self.loop = None
        self.header = None
        self.footer = None
        self.body = None
        self._sprig = Sprig()

    def exit_or_handle(self, input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()

        self.body.keypress(input)

    def show_main(self, cart=None):
        menu = MenuController(self, self._sprig, cart)
        menu.connect_signal("confirm", self.show_cart_confirmation)
        menu.connect_signal("order", self.show_order_completed)
        menu.show_menu()
        self._draw(menu)

    def show_cart_confirmation(self, cart):
        cartc = CartController(self, self._sprig, cart)
        cartc.connect_signal("order", self.show_order_completed)
        cartc.connect_signal("cancel", self.show_main)
        cartc.show_confirmation()
        self._draw(cartc)

    def show_order_completed(self, order=None):
        orderc = OrderController(self, self._sprig, order)
        orderc.connect_signal("menu", self.show_main)
        orderc.show_order()
        self._draw(orderc)

    def show_login(self):
        login = LoginController(self, self._sprig)
        login.connect_signal("login", self.show_main)
        self._draw(login)

    def _draw(self, body):
        if not self.header or not self.footer:
            self.header = HeaderUI()
            self.footer = FooterUI()

        self.body = body
        self.frame = urwid.Frame(self.body.ui, self.header, self.footer)

        if self.loop:
            self.loop.widget = self.frame

    def run(self):
        self.loop = urwid.MainLoop(self.frame,
                                   unhandled_input=self.exit_or_handle,
                                   event_loop=GeventLoop(), pop_ups=True)
        self.loop.run()


if __name__ == "__main__":
    ui = UIController()
    ui.show_login()
    ui.run()
