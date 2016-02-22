import json
import unittest

from aloha import aloha_put


def unicodify(v):
    if isinstance(v, str):
        return v.decode('ascii')
    elif isinstance(v, dict):
        return unicodify_r(v)
    elif isinstance(v, list):
        return map(unicodify, v)
    else:
        return v


def unicodify_r(d):
    newd = {}
    for k, v in d.iteritems():
        newd[unicodify(k)] = unicodify(v)
    return newd


class TestRealWorld(unittest.TestCase):
    maxDiff = None

    def test_(self):
        in_ = json.load(open('in.json'))
        x_out = json.load(open('out.json'))
        out = aloha_put(in_)
        del out['PromiseDateTime']
        del x_out['PromiseDateTime']
        self.assertDictEqual(unicodify(out), unicodify(x_out))


if __name__ == '__main__':
    unittest.main()

