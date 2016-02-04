import unittest

from jsonbender.engine import bend, K, S


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



if __name__ == '__main__':
    unittest.main()

