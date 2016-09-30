#!/usr/bin/env python
# encoding: utf-8

from .cross import cross
from math import hypot
import itertools
import cplex

MAX_LENGTH = 2

def arrange(col_count, row_count, links, multiplicity, **kwargs):
    
    def push(constraint):
        result.append("c%s: %s" % (counter.next(), constraint))
    
    summation = " + ".join
    result = ["enter %s" % filename]
    counter = itertools.count()
    
    from pprint import pprint
    
    print("Edges")
    E = list(links) # + [(n2, n1) for (n1, n2) in links]
    # pprint(E)

    print("Positions")
    P = list(itertools.product(range(col_count), range(row_count)))
    # pprint(P)

    print("Admissible segments")
    S = [((i1, j1), (i2, j2)) for ((i1, j1), (i2, j2)) in itertools.combinations(P, 2) if hypot(abs(i1-i2), abs(j1-j2))-1 <= MAX_LENGTH]
    # pprint(S)

    print("Crossing segments")
    S2X = []
    for (((i1, j1), (i2, j2)), ((i3, j3), (i4, j4))) in itertools.combinations(S, 2):
        if cross((i1, j1, i2, j2, i3, j3, i4, j4)):
            S2X.append((((i1, j1), (i2, j2)), ((i3, j3), (i4, j4))))
    S2X = set(S2X)
    # pprint(S2X)
    
    print("Adjacent segments")
    S2V = []
    for ((p1, p2), (p3, p4)) in itertools.combinations(S, 2):
        if ((p1, p2), (p3, p4)) not in S2X and len(set((p1, p2, p3, p4))) == 3:
            S2V.append(((p1, p2), (p3, p4)))
    S2V = set(S2V)
    # pprint(S2V)

    print("Adjacent edges")
    E2V = []
    for ((v1, v2), (v3, v4)) in itertools.combinations(E, 2):
        if len(set((v1, v2, v3, v4))) == 3:
            E2V.append(((v1, v2), (v3, v4)))
    E2V = set(E2V)
    # pprint(E2V)
    
    lengths = [str(round(hypot(abs(i1-i2), abs(j1-j2)),4) - 1) for ((i1, j1), (i2, j2)) in S]
    lengths = ["" if s == "1.0" else (s[:-2] + "" if s.endswith(".0") else s + "") for s in lengths]
    
    result.append("Minimize")
    result.append(" obj: " + summation("{length}x_{s[0][0]}_{s[0][1]}_{s[1][0]}_{s[1][1]}".format(length=length, s=s) for (length, s) in itertools.izip(lengths, S) if length != "0"))
    result.append("Subject To")
    
    result.append(u"\\ Each edge is assigned to exactly one segment")
    for e in E:
        push("%s = 1" % summation("y_{e[0]}_{e[1]}_{s[0][0]}_{s[0][1]}_{s[1][0]}_{s[1][1]}".format(e=e, s=s) for s in S))
    
    result.append(u"\\ Each segment is occupied by 1 segment if it is active, 0 otherwise")
    for s in S:
        push("{sigma} - x_{s[0][0]}_{s[0][1]}_{s[1][0]}_{s[1][1]} = 0".format(sigma=summation("y_{e[0]}_{e[1]}_{s[0][0]}_{s[0][1]}_{s[1][0]}_{s[1][1]}".format(e=e, s=s) for e in E), s=s))
    
    result.append(u"\\ The active segments do not cross each other")
    for (s1, s2) in S2X:
        push("x_{s1[0][0]}_{s1[0][1]}_{s1[1][0]}_{s1[1][1]} + x_{s2[0][0]}_{s2[0][1]}_{s2[1][0]}_{s2[1][1]} <= 1".format(s1=s1, s2=s2))
    
    result.append(u"\\ The non adjacent edges are not placed on adjacent segments, and vice versa")
    for (s1, s2) in itertools.combinations(S, 2):
        for (e1, e2) in itertools.combinations(E, 2):
            if ((s1, s2) in S2V) != ((e1, e2) in E2V):
                push("y_{e1[0]}_{e1[1]}_{s1[0][0]}_{s1[0][1]}_{s1[1][0]}_{s1[1][1]} + y_{e2[0]}_{e2[1]}_{s2[0][0]}_{s2[0][1]}_{s2[1][0]}_{s2[1][1]} <= 1".format(e1=e1, e2=e2, s1=s1, s2=s2))
                push("y_{e1[0]}_{e1[1]}_{s2[0][0]}_{s2[0][1]}_{s2[1][0]}_{s2[1][1]} + y_{e2[0]}_{e2[1]}_{s1[0][0]}_{s1[0][1]}_{s1[1][0]}_{s1[1][1]} <= 1".format(e1=e1, e2=e2, s1=s1, s2=s2))

    # result.append(u"\\ Each extremity of an placed edge is placed")
    # for (s1, s2) in itertools.combinations(S, 2):
    #     for (e1, e2) in itertools.combinations(E, 2):
    # for e in E:
    #     push("y_{e1[0]}_{e1[1]}_{s1[0][0]}_{s1[0][1]}_{s1[1][0]}_{s1[1][1]} + y_{e2[0]}_{e2[1]}_{s2[0][0]}_{s2[0][1]}_{s2[1][0]}_{s2[1][1]} <= 1".format(e1=e1, e2=e2, s1=s1, s2=s2))


    result.append("Binary")
    result.append(" ".join("x_{s[0][0]}_{s[0][1]}_{s[1][0]}_{s[1][1]}".format(s=s) for s in S))
    result.append(" ".join("y_{e[0]}_{e[1]}_{s[0][0]}_{s[0][1]}_{s[1][0]}_{s[1][1]}".format(e=e, s=s) for s in S for e in E))
    
    result.append("\nEnd\noptimize\ndisplay solution variables -\n")
    
    open("a.lp" % filename, "w").write("\n".join(result))
    
    problem = cplex.Cplex()
    problem.parameters.read.datacheck.set(0)
    problem.set_results_stream("cplex_python.log")
    problem.read("mocodo/a.lp")
    problem.solve()
    result = [None] * len(params["successors"])
    for (ep, assigned) in zip(problem.variables.get_names(),problem.solution.get_values()):
        if assigned and ep.startswith("x"):
            (v, x, y) = map(int,ep.split("_")[1:])
            result[v] = (x, y)
    print(result)
    print("Cumulated distances:", problem.solution.get_objective_value())
    

if __name__ == "__main__":
    from .mcd import Mcd
    from .argument_parser import parsed_arguments
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
    clauses = u"""
Item : Norm, Wash, Haul, Milk, Draw, Lady, Face, Soon, Dish, Ever, Unit
Folk :
Peer, XX> Tour, XX Folk, XX Item
Hall, 0n Tour, 11 Fold

Tour : Baby
Bind, 0n Tour, 11 Fold
Gene, 11 Fold, 1n Fold
Fold : Aids,Free, Pack

Seem, 11 Fold, 1n Fold
Teen, 11 Fold, 1n Amid
Amid : Disk, Flip, Gold
    """.replace("  ", "").split("\n")
    params = parsed_arguments()
    mcd = Mcd(clauses, params)
    params.update(mcd.get_layout_data())
    starting_time = time()
    seed(42)
    result = dump_lp("mocodo/a", **params)
    if result:
        print()
        print(mcd.get_clauses_from_layout(**result))
        print()
        print("Cumulated distances:", result["distances"])
        print("Duration:", time() - starting_time)
        print()