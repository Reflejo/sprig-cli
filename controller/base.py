class Controller(object):

    signals = []

    def __init__(self):
        self._signals = dict((signal, None) for signal in self.signals)

    def _emit(self, signal, *args):
        closure = self._signals[signal]
        if callable(closure):
            closure(*args)

    def connect_signal(self, signal, closure):
        if signal not in self._signals:
            name = self.__class__.__name__
            raise ValueError("%s doesn't support signal %s" % (name, signal))

        self._signals[signal] = closure

    def keypress(self, key):
        pass

    @property
    def ui(self):
        return self._ui
