from functools import partial

from jsonbender._compat import iteritems


class Bender(object):

    """
    Base bending class. All selectors and transformations should directly or
    indirectly derive from this. Should not be instantiated.

    Whenever a bender is activated (by the bend() function), the execute()
    method is called with the source as it's single argument.
    All bending logic should be there.

    Subclasses must implement __init__() and execute() methods.
    """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    def __call__(self, source):
        return self.execute(source)

    def execute(self, source):
        raise NotImplementedError()

    def __add__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Sub(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __div__(self, other):
        return Div(self, other)

    def __rshift__(self, other):
        return Compose(self, other)

    def __lshift__(self, other):
        return Compose(other, self)

    def __getitem__(self, index):
        return self >> GetItem(index)


class GetItem(Bender):
    def __init__(self, index):
        self._index = index

    def execute(self, value):
        return value[self._index]


class Compose(Bender):
    def __init__(self, first, second):
        self._first = first
        self._second = second

    def execute(self, source):
        return self._second(self._first(source))


class BinaryOperator(Bender):

    """
    Base class for binary bending operators. Should not be directly
    instantiated.

    Whenever a bin op is activated, the op() method is called with both
    *values* (that is, the benders are implicitly activated).

    Subclasses must implement the op() method, which takes two values and
    should return the desired result.
    """

    def __init__(self, bender1, bender2):
        self._bender1 = bender1
        self._bender2 = bender2

    def op(self, v1, v2):
        raise NotImplementedError()

    def execute(self, source):
        return self.op(self._bender1(source), self._bender2(source))


class Add(BinaryOperator):
    def op(self, v1, v2):
        return v1 + v2


class Sub(BinaryOperator):
    def op(self, v1, v2):
        return v1 - v2


class Mul(BinaryOperator):
    def op(self, v1, v2):
        return v1 * v2


class Div(BinaryOperator):
    def op(self, v1, v2):
        return float(v1) / float(v2)


class BendingException(Exception):
    pass


def bend(mapping, source):
    """
    The main bending function.

    mapping: the map of benders
    source: a dict to be bent

    returns a new dict according to the provided map.
    """
    res = {}
    for k, value in iteritems(mapping):
        if isinstance(value, Bender):
            try:
                newv = value(source)
            except Exception as e:
                m = 'Error for key {}: {}'.format(k, str(e))
                raise BendingException(m)
        elif isinstance(value, list):
            newv = map(lambda v: bend(v, source), value)
        else:
            newv = bend(value, source)
        res[k] = newv
    return res

