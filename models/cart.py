from collections import defaultdict


class Cart(object):

    def __init__(self, menu, payment, address, items=None, scheduled=False):
        self.menu = menu
        self.items = items or defaultdict(int)
        self.address = address
        self.scheduled = scheduled
        self.payment = payment

    @property
    def total(self):
        return sum(self.items.values())

    @property
    def order_is_available(self):
        for inventory in self.menu.inventories:
            for item, count in self.items.iteritems():
                if inventory.get(str(item.id), 0) < count:
                    break
            else:
                return True

        return False
