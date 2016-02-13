import unittest

from jsonbender import K, S


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


if __name__ == '__main__':
    unittest.main()

