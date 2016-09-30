#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path[0:0] = ["."]

import unittest
from mocodo.grid import Grid

class GridTests(unittest.TestCase):
    
    def test_constructor(self):
        grid = Grid(16)
        assert grid == [None, (1, 1), (2, 2), (2, 2), (2, 2), (3, 2), (3, 2), (3, 3), (3, 3), (3, 3), (4, 3), (4, 3), (4, 3), (5, 3), (5, 3), (5, 3), (4, 4)]
    
    def test_nth_next(self):
        grid = Grid(16)
        assert grid[3] == (2, 2)
        assert grid.get_nth_next(3, 0) == (2, 2)
        assert grid.get_nth_next(3, 1) == (3, 2)
        assert grid.get_nth_next(3, 2) == (3, 3)
        assert grid.get_nth_next(3, 3) == (4, 3)

if __name__ == '__main__':
    unittest.main()
