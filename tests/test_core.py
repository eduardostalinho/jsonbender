import unittest

from jsonbender import bend, BendingException, S, K


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

    def test_nested_mapping_with_lists(self):
        mapping = {
            'a_field': S('a', 'b'),
            'a': [{
                'nested': {
                    'field': S('f1', 'f2'),
                },
            }],
        }
        source = {
            'a': {'b': 'ok'},
            'f1': {'f2': 'hi'},
        }
        expected = {
            'a_field': 'ok',
            'a': [{'nested': {'field': 'hi'}}],
        }
        self.assertDictEqual(bend(mapping, source), expected)

    def test_bending_exception_is_raised_when_something_bad_happens(self):
        mapping = {'a': S('nonexistant')}
        source = {}
        self.assertRaises(BendingException, bend, mapping, source)


class TestOperators(unittest.TestCase):
    def test_add(self):
        self.assertEqual((S('v1') + K(2))({'v1': 5}), 7)

    def test_sub(self):
        self.assertEqual((S('v1') - K(2))({'v1': 5}), 3)

    def test_mul(self):
        self.assertEqual((S('v1') * K(2))({'v1': 5}), 10)

    def test_div(self):
        self.assertAlmostEqual((S('v1') / K(2))({'v1': 5}), 2.5, 2)


class TestGetItem(unittest.TestCase):
    def test_getitem(self):
        bender = S('val')[2:8:2]
        self.assertEqual(bender({'val': range(10)}), [2, 4, 6])


if __name__ == '__main__':
    unittest.main()
