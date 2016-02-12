from itertools import chain

from jsonbender.engine.core import Bender


class ListOp(Bender):
    def __init__(self, bender, function):
        self._func = function
        self._bender = bender

    def op(self, func, vals):
        raise NotImplementedError()

    def execute(self, source):
        return self.op(self._func, self._bender(source))


class Forall(ListOp):
    op = map


class Reduce(ListOp):
    def op(self, func, vals):
        try:
            return reduce(func, vals)
        except TypeError as e:  # empty list with no initial value
            raise ValueError(e.message)


class Filter(ListOp):
    op = filter


class FlatForall(ListOp):
    def op(self, func, vals):
        return list(chain.from_iterable(map(func, vals)))
