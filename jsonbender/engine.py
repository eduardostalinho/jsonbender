def K(value):
    def execute(source):
        return value
    return execute


def S(*path):
    if not path:
        raise ValueError('No path given')

    def execute(source):
        for key in path:
            source = source[key]
        return source
    return execute


def bend(mapping, source):
    return {k: execute(source) for k, execute in mapping.iteritems()}

