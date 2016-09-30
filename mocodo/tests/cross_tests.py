#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
sys.path[0:0] = ["."]

import unittest
from mocodo.cross import cross

class CrossTests(unittest.TestCase):

    def test_non_parallel_normal_intersection(self):
        self.assertTrue(cross(4,4, 7,4, 4,3, 6,5))
        self.assertTrue(cross(2,1, 4,3, 1,2, 5,1))
        self.assertTrue(cross(1,4, 7,4, 4,1, 4,7))
        self.assertTrue(cross(0,0, 0,5,-1,2, 1,2))
        self.assertTrue(cross(0,0, 0,5, 1,0,-1,4))

    def test_non_parallel_intersection_is_one_extremity(self):
        self.assertTrue(cross(2,0, 3,1, 3,0, 3,3))
        self.assertTrue(cross(5,0, 0,5, 3,2, 5,4))
        self.assertTrue(cross(0,0, 0,5, 7,5, -7,-5))
        self.assertTrue(cross(3,0, 3,3, 2,0, 3,1))
        self.assertTrue(cross(2,0, 3,1, 3,0, 3,3))
        self.assertTrue(cross(3,3, 3,0, 3,1, 2,0))
        self.assertTrue(cross(3,1, 2,0, 3,3, 3,0))
        self.assertTrue(cross(3,0, 3,3, 3,2, 2,3))

    def test_non_parallel_intersection_is_two_extremities(self):
        """ This is not considered as a valid intersection. """
        self.assertTrue(not cross(0,0, 0,5, 0,0, 5,0))
        self.assertTrue(not cross(0,0, 0,1, 0,1, 1,1))

    def test_non_parallel_no_intersection(self):
        self.assertTrue(not cross(2,2, 8,2, 3,3, 9,6))
        self.assertTrue(not cross(1,2, 5,6, 3,2, 8,5))
        self.assertTrue(not cross(0,0, 0,5, 1,2, 4,2))
        self.assertTrue(not cross(0,0, 0,5, 1,0, 4,6))
        self.assertTrue(not cross(0,0, 1,0, 3,0, 3,3))
        self.assertTrue(not cross(0,0, 1,0, 0,1, 0,2))

    def test_parallel_no_intersection(self):
        self.assertTrue(not cross(1,2, 5,6, 3,2, 5,4))
        self.assertTrue(not cross(3,3, 5,3, 4,4, 6,4))
        self.assertTrue(not cross(3,3, 4,3, 5,4, 6,4))
        self.assertTrue(not cross(0,0, 5,0, 1,1, 5,1))

    def test_colinear_intersection_is_two_extremities(self):
        """ This is not considered as a valid intersection. """
        self.assertTrue(not cross(0,0, 1,2, 1,2, 2,4))

    def test_colinear_no_intersection(self):
        self.assertTrue(not cross(3,3, 4,3, 5,3, 6,3))

    def test_colinear_intersection_is_partial_segment(self):
        self.assertTrue(cross(0,0, 4,2, 2,1, 6,3))

    def test_colinear_intersection_is_partial_segment_horizontal(self):
        self.assertTrue(cross(3,3, 5,3, 4,3, 6,3))

    def test_colinear_intersection_is_partial_segment_vertical(self):
        self.assertTrue(cross(3,3, 3,5, 3,4, 3,6))

    def test_colinear_intersection_is_complete_segment_horizontal(self):
        self.assertTrue(cross(0,2, 2,2,-2,2, 4,2))
        self.assertTrue(cross(0,2, 2,2, 0,2, 4,2))
        self.assertTrue(cross(0,2, 2,2,-2,2, 2,2))
        self.assertTrue(cross(0,2, 2,2, 1,2, 2,2))
        self.assertTrue(cross(2,2, 0,2, 1,2, 2,2))
        self.assertTrue(cross(0,2, 2,2, 2,2, 1,2))
        self.assertTrue(cross(2,2, 0,2, 2,2, 1,2))
        self.assertTrue(cross(1,2, 2,2, 0,2, 2,2))
        self.assertTrue(cross(1,2, 2,2, 2,2, 0,2))
        self.assertTrue(cross(2,2, 1,2, 0,2, 2,2))
        self.assertTrue(cross(2,2, 1,2, 2,2, 0,2))

    def test_colinear_intersection_is_complete_segment_vertical(self):
        self.assertTrue(cross(2,0, 2,2, 2,-2, 2,4))
        self.assertTrue(cross(2,0, 2,2, 2, 0, 2,4))
        self.assertTrue(cross(2,0, 2,2, 2,-2, 2,2))

    def test_colinear_intersection_is_complete_segment(self):
        self.assertTrue(cross(0,0, 6,3, 2,1, 4,2))
        self.assertTrue(cross(0,0, 6,3, 2,1, 6,3))
        self.assertTrue(cross(0,0, 6,3, 0,0, 4,2))

if __name__ == '__main__':
    unittest.main()
