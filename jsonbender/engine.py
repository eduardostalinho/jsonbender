class Bender(object):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    def __call__(self, source):
        return self.execute(source)

    def execute(self, source):
        raise NotImplementedError()


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


def bend(mapping, source):
    res = {}
    for k, value in mapping.iteritems():
        if isinstance(value, Bender):
            newv = value(source)
        else:
            newv = bend(value, source)
        res[k] = newv
    return res

