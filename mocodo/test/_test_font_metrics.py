#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
sys.path[0:0] = ["."]

import unittest
from mocodo.font_metrics import *

import tkFont

params = {}
params["tkinter"] = True
FontMetrics = font_metrics_factory(params)

helv36 = FontMetrics({"family": "Helvetica", "size": 36})
helv36b = FontMetrics({"family": "Helvetica", "size": 36, "weight": "bold"})
helv36b2 = FontMetrics({"family": "Helvetica-Bold", "size": 36})
helv36b3 = FontMetrics({"family": "Helvetica-Bold", "size": 36, "weight": "bold"})
helv36b4 = FontMetrics({"family": "Helvetica-Bold", "size": 36, "weight": tkFont.BOLD})
times12 = FontMetrics({"family": "Times", "size": 12})


class FontMetricsWithTkTest(unittest.TestCase):

    def test_helv36_get_pixel_height(self):
        self.assertEqual(helv36.get_pixel_height(), 36)

    def test_helv36_get_pixel_width(self):
        self.assertEqual(helv36.get_pixel_width("My string"), 146)

    def test_helv36b_get_pixel_height(self):
        self.assertEqual(helv36b.get_pixel_height(), 36)

    def test_helv36b_get_pixel_width(self):
        self.assertEqual(helv36b.get_pixel_width("My string"), 160)

    def test_helv36b2_get_pixel_width(self):
        self.assertEqual(helv36b2.get_pixel_width("My string"), 161)

    def test_helv36b3_get_pixel_width(self):
        self.assertEqual(helv36b3.get_pixel_width("My string"), 177)

    def test_helv36b4_get_pixel_width(self):
        self.assertEqual(helv36b4.get_pixel_width("My string"), 177)

    def test_times12_get_pixel_height(self):
        self.assertEqual(times12.get_pixel_height(), 12)

    def test_times12_get_pixel_width(self):
        self.assertEqual(times12.get_pixel_width("My string"), 47)

    def test_empty_string_get_pixel_width(self):
        self.assertEqual(times12.get_pixel_width(""), 0)


if __name__ == '__main__':
    unittest.main()
