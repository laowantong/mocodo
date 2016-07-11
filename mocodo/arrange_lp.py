#!/usr/bin/env python
# encoding: utf-8

from dump_lp import dump_lp

def arrange(col_count, row_count, successors, multiplicity, **kwargs):
    dump_lp("filename", col_count, row_count, successors, multiplicity, 2)
    result = None
    return result
    
if __name__ == "__main__":
    from mcd import Mcd
    from argument_parser import parsed_arguments
    from time import time
    from random import seed
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
    """.replace("  ", "").split("\n")
    params = parsed_arguments()
    mcd = Mcd(clauses, params)
    params.update(mcd.get_layout_data())
    starting_time = time()
    seed(42)
    result = arrange(**params)
    if result:
        print
        print mcd.get_clauses_from_layout(**result)
        print
        print "Cumulated distances:", result["distances"]
        print "Duration:", time() - starting_time
        print 
