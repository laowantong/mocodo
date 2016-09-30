#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
sys.path[0:0] = ["."]

from mocodo.arrange_ga import *

import unittest
from mocodo.mcd import Mcd
from mocodo.argument_parser import parsed_arguments
from time import time
from random import seed

# WARNING: by default, this should fail for Python 3.
# Set PYTHONHASHSEED to 0 before launching the tests.
# cf. http://stackoverflow.com/questions/38943038/difference-between-python-2-and-3-for-shuffle-with-a-given-seed/

class ArrangeGA(unittest.TestCase):
    
    def test_run(self):
        clauses = u"""
            SUSPENDISSE: diam
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            CONSECTETUER: elit, sed
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

            DF1, 11 LOREM, 1N SUSPENDISSE
            LOREM: ipsum, dolor, sit
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            DIGNISSIM: ligula, massa, varius

            DF, 11 RISUS, 0N RISUS
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            RISUS: ultricies, _cras, elementum
            SEMPER, 0N RISUS, 1N DIGNISSIM
        """.replace("  ", "")
        params = parsed_arguments()
        mcd = Mcd(clauses.split("\n"), params)
        params.update(mcd.get_layout_data())
        params["crossover_rate"] = 0.9
        params["max_generations"] = 50
        params["mutation_rate"] = 0.06
        params["plateau"] = 30
        params["population_size"] = 100
        params["sample_size"] = 7
        params["timeout"] = None
        params["verbose"] = False
        seed(1 if sys.version_info.major == 2 else 67)
        rearrangement = arrange(**params)
        self.assertEqual(rearrangement, {
            'distances': 3.3005630797457695,
            'crossings': 1,
            'layout': [9, 5, 4, 0, 2, 1, 11, 8, 3, 7, 6, 10]
        })
        expected = u"""
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            LOREM: ipsum, dolor, sit
            DF1, 11 LOREM, 1N SUSPENDISSE
            SUSPENDISSE: diam

            CONSECTETUER: elit, sed
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            SEMPER, 0N RISUS, 1N DIGNISSIM
            DF, 11 RISUS, 0N RISUS

            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            DIGNISSIM: ligula, massa, varius
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            RISUS: ultricies, _cras, elementum
        """.strip().replace("  ", "")
        mcd.set_layout(**rearrangement)
        result = mcd.get_clauses()
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
