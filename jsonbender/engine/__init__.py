from itertools import chain


class Bender(object):
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


class BinaryOperator(Bender):
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


class K(Bender):
    def __init__(self, value):
        self._val = value

    def execute(self, source):
        return self._val


class S(Bender):
    def __init__(self, *path):
        if not path:
            raise ValueError('No path given')
        self._path = path

    def execute(self, source):
        for key in self._path:
            source = source[key]
        return source


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


def bend(mapping, source):
    res = {}
    for k, value in mapping.iteritems():
        if isinstance(value, Bender):
            newv = value(source)
        else:
            newv = bend(value, source)
        res[k] = newv
    return res

