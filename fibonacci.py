#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Fibonacci sequence (starts from first_idx and ends at end_idx) generator.

Usage:
>>> from fibonacci import Fibonacci
>>> f = Fibonacci()
>>> g = f.generate(1, 5)
>>> next(g)
0
>>> next(g)
1
>>> f.sequence(1, 5)
[1, 1, 2, 3, 5]
"""

__all__ = ['Fibonacci']


try:
    xrange
except NameError:
    xrange = range


def singleton(cls):
    """A singleton decorator for classes"""
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class Fibonacci(object):

    def __init__(self):
        self._results = [0, 1, 2]	

    def __compute(self, n1, n2):
        for i in xrange(len(self._results), n2):
            self._results.append(self._results[i-1] + self._results[i-2])

    def generate(self, n1, n2):
        """Returns a python `generator` represents the numbers in the
        Fibonacci sequence (starts from n1 to n2).  Python generator is more memory
        efficient for iteration.
        """
        self.__compute(n1, n2)

        for i in xrange(n1, n2):
            yield self._results[i]

    def sequence(self, n1, n2):
        """Returns the numbers in the Fibonacci sequence as a list"""
        self.__compute(n1, n2)
	
	if n1 == 0:
            return self._results[n1:n2]
	else:
	    return self._results[n1-1:n2]


if __name__ == '__main__':  # pragma: no cover
    import sys
    import cProfile

    # Act as a simple command line tool and take a number from command line
    try:
        n1 = int(sys.argv[1])
	n2 = int(sys.argv[2])
    except:
        raise SystemExit('Please provide a positive integer')

    fib = Fibonacci()
    statement = 'seq = fib.sequence(n1, n2)'

    # Too bad cProfile does not support dumping to stderr.  Here is the trick:
    #
    # a) If stdout is redirected to a file or `wc -c`, just print the results
    # b) Otherwise just dump the profiling data
    #
    if sys.stdout.isatty():
        cProfile.run(statement)
    else:
        exec(statement)
        print(seq)
