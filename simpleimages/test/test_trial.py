import unittest


class MyFuncTestCase(unittest.TestCase):
    def testBasic(self):
        self.assertEqual('hi', 'hi')
