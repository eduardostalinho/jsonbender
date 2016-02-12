from jsonbender.engine.core import Bender


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
