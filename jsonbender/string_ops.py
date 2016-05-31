from jsonbender.core import Bender
from jsonbender._compat import iteritems


class Format(Bender):
    def __init__(self, format_string, *args, **kwargs):
        self._format_str = format_string
        self._positional_benders = args
        self._named_benders = kwargs

    def execute(self, source):
        args = [bender(source) for bender in self._positional_benders]
        kwargs = {k: bender(source)
                  for k, bender in iteritems(self._named_benders)}
        return self._format_str.format(*args, **kwargs)

