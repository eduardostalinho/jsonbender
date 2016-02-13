import unittest

from jsonbender import K
from jsonbender.list_ops import Forall, FlatForall, Filter, ListOp, Reduce


class ListOpTestCase(unittest.TestCase):
    cls = ListOp

    def assert_list_op(self, the_list, func, expected_value):
        bender = self.cls(K(the_list), func)
        self.assertEqual(bender({}), expected_value)


class TestForall(ListOpTestCase):
    cls = Forall

    def test_empty_list(self):
        self.assert_list_op([], lambda i: i*2, [])

    def test_nonempty_list(self):
        self.assert_list_op(range(1, 5), lambda i: i*2, [2, 4, 6, 8])


class TestReduce(ListOpTestCase):
    cls = Reduce

    def test_empty_list(self):
        bender = Reduce(K([]), lambda acc, i: acc + i)
        self.assertRaises(ValueError, bender, {})

    def test_nonempty_list(self):
        self.assert_list_op(range(1, 5), lambda acc, i: acc + i, 10)


class TestFilter(ListOpTestCase):
    cls = Filter

    def test_empty_list(self):
        self.assert_list_op([], lambda d: not d['ignore'], [])

    def test_nonempty_list(self):
        the_list = [{'id': 1, 'ignore': True},
                    {'id': 2, 'ignore': False},
                    {'id': 3, 'ignore': False},
                    {'id': 4, 'ignore': True}]

        expected = [{'id': 2, 'ignore': False}, {'id': 3, 'ignore': False}]
        self.assert_list_op(the_list, lambda d: not d['ignore'], expected)


class TestFlatForall(ListOpTestCase):
    cls = FlatForall

    def test_empty_list(self):
        self.assert_list_op([], lambda d: d['b'], [])

    def test_nonempty_list(self):
        self.assert_list_op([{'b': [1, 2]}, {'b': [-2, -1]}],
                            lambda d: d['b'],
                            [1, 2, -2, -1])


if __name__ == '__main__':
    unittest.main()

