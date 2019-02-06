#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from fibonacci import Fibonacci


class SingletonTest(unittest.TestCase):

    def test_id(self):
        fib1 = Fibonacci()
        fib2 = Fibonacci()
        self.assertEqual(id(fib1), id(fib2))


class FibonacciTest(unittest.TestCase):

    def setUp(self):
        self._fib = Fibonacci()

    def test_generator(self):
        x = self._fib.generate(1, 4)
        self.assertEqual(next(x), 0)
        self.assertEqual(next(x), 1)
        self.assertEqual(next(x), 1)
        self.assertEqual(next(x), 2)
        self.assertRaises(StopIteration, next, x)

    def test_minimal(self):
        self.assertEqual(self._fib.sequence(0,0), [])
        self.assertEqual(self._fib.sequence(0,1), [0])
        self.assertEqual(self._fib.sequence(0,2), [0, 1])

    def test_normal(self):
        self.assertEqual(self._fib.sequence(1, 5), [1, 1, 2, 3, 5])

    def test_large(self):
        x = self._fib.sequence(0, 100)
        self.assertEqual(len(x), 100)
        self.assertEqual(x[97], 83621143489848422977)
        self.assertEqual(x[98], 135301852344706746049)
        self.assertEqual(x[99], 218922995834555169026)

    def test_xlarge(self):
        """Result is too long so just verify the first and last 32 digits of
        the last number
        """
        x = self._fib.sequence(0, ss100000)
        self.assertEqual(len(x), 100000)
        s = str(x[99999])
        self.assertEqual(len(s), 20899)
        self.assertEqual(s[:32], '16052857682729819697035016991663')
        self.assertEqual(s[-32:], '35545120747688390605016278790626')


if __name__ == '__main__':
    unittest.main()
