import sys

PY2 = sys.version_info[0] == 2

if not PY2:
    iteritems = lambda d: iter(d.items())
else:
    iteritems = lambda d: d.iteritems()
