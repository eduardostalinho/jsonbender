import unittest

from jsonbender import bend, Forall, FlatForall, Filter, Reduce, K, S


class TestK(unittest.TestCase):
    def test_k(self):
        self.assertEqual(K(1)({}), 1)
        self.assertEqual(K('string')({}), 'string')


class TestS(unittest.TestCase):
    def test_no_selector_raises_value_error(self):
        self.assertRaises(ValueError, S)

    def test_single_existing_field(self):
        self.assertEqual(S('a')({'a': 'val'}), 'val')

    def test_deep_existing_path(self):
        source = {'a': [{}, {'b': 'ok!'}]}
        self.assertEqual(S('a', 1, 'b')(source), 'ok!')


class TestBend(unittest.TestCase):
    def test_empty_mapping(self):
        self.assertDictEqual(bend({}, {'a': 1}), {})

    def test_flat_mapping(self):
        mapping = {
            'a_field': S('a', 'b'),
            'another_field': K('wow'),
        }
        source = {'a': {'b': 'ok'}}
        expected = {
            'a_field': 'ok',
            'another_field': 'wow',
        }
        self.assertDictEqual(bend(mapping, source), expected)

    def test_nested_mapping(self):
        mapping = {
            'a_field': S('a', 'b'),
            'a': {
                'nested': {
                    'field': S('f1', 'f2'),
                },
            },
        }
        source = {
            'a': {'b': 'ok'},
            'f1': {'f2': 'hi'},
        }
        expected = {
            'a_field': 'ok',
            'a': {'nested': {'field': 'hi'}},
        }
        self.assertDictEqual(bend(mapping, source), expected)


class TestOperators(unittest.TestCase):
    def test_add(self):
        self.assertEqual((S('v1') + K(2))({'v1': 5}), 7)

    def test_sub(self):
        self.assertEqual((S('v1') - K(2))({'v1': 5}), 3)

    def test_mul(self):
        self.assertEqual((S('v1') * K(2))({'v1': 5}), 10)

    def test_div(self):
        self.assertAlmostEqual((S('v1') / K(2))({'v1': 5}), 2.5, 2)


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

