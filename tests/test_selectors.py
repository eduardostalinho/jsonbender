import unittest

from jsonbender import F, K, S


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


class TestF(unittest.TestCase):
    def test_f(self):
        self.assertEqual(F(len)(range(5)), 5)

    def test_curry_kwargs(self):
        f = F(sorted, key=lambda d: d['v'])
        source = [{'v': 2}, {'v': 3}, {'v': 1}]
        self.assertEqual(f(source), [{'v': 1}, {'v': 2}, {'v': 3}])

    def test_composition(self):
        s = S('val')
        f = F(len)
        source = {'val': 'hello'}
        self.assertEqual((f << s)(source), 5)
        self.assertEqual((s >> f)(source), 5)


if __name__ == '__main__':
    unittest.main()

