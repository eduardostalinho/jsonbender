import unittest

from jsonbender import K
from jsonbender.string_ops import Format


class TestFormat(unittest.TestCase):
    def test_format(self):
        bender = Format('{} {} {} {noun}.',
                        K('This'), K('is'), K('a'),
                        noun=K('test'))
        self.assertEqual(bender({}), 'This is a test.')


if __name__ == '__main__':
    unittest.main()

