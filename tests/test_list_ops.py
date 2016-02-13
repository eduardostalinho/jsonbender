import unittest

from jsonbender import bend, S, Forall, FlatForall, Filter, Reduce


class TestForall(unittest.TestCase):
    def test_empty_list(self):
        mapping = {'a': Forall(S('b'), lambda i: i*2)}
        source = {'b': []}
        self.assertDictEqual(bend(mapping, source), {'a': []})

    def test_nonempty_list(self):
        mapping = {'a': Forall(S('b'), lambda i: i*2)}
        source = {'b': range(1, 5)}
        self.assertDictEqual(bend(mapping, source), {'a': [2, 4, 6, 8]})


class TestReduce(unittest.TestCase):
    def test_empty_list(self):
        mapping = {'a': Reduce(S('b'), lambda acc, i: acc + i)}
        source = {'b': []}
        self.assertRaises(ValueError, bend, mapping, source)

    def test_nonempty_list(self):
        mapping = {'a': Reduce(S('b'), lambda acc, i: acc + i)}
        source = {'b': range(1, 5)}
        self.assertDictEqual(bend(mapping, source), {'a': 10})


class TestFilter(unittest.TestCase):
    def test_empty_list(self):
        mapping = {'a': Filter(S('b'), lambda d: not d['ignore'])}
        source = {'b': []}
        self.assertDictEqual(bend(mapping, source), {'a': []})

    def test_nonempty_list(self):
        mapping = {'a': Filter(S('b'), lambda d: not d['ignore'])}
        source = {'b': [{'id': 1, 'ignore': True},
                        {'id': 2, 'ignore': False},
                        {'id': 3, 'ignore': False},
                        {'id': 4, 'ignore': True}]}

        self.assertDictEqual(bend(mapping, source),
                             {'a': [{'id': 2, 'ignore': False},
                                    {'id': 3, 'ignore': False}]})


class TestFlatForall(unittest.TestCase):
    def test_empty_list(self):
        mapping = {'a': FlatForall(S('bs'), lambda d: d['b'])}
        source = {'bs': []}
        self.assertDictEqual(bend(mapping, source), {'a': []})

    def test_nonempty_list(self):
        mapping = {'a': FlatForall(S('bs'), lambda d: d['b'])}
        source = {
            'bs': [{'b': [1, 2]}, {'b': [-2, -1]}]
        }
        self.assertDictEqual(bend(mapping, source), {'a': [1, 2, -2, -1]})


if __name__ == '__main__':
    unittest.main()

