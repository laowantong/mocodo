#!/usr/bin/env python
# encoding: utf-8

from .cross import cross
from math import hypot
import os
import itertools

MAX_LENGTH = 2

def dump_lp(path, col_count, row_count, links, successors, multiplicity, **kwargs):
    
    def push(constraint):
        result.append("c%s: %s" % (counter.next(), constraint))
    
    summation = " + ".join
    result = []
    counter = itertools.count()
    
    V = range(len(successors)) #
    
    # print "Edges"
    E = list(links)
    # pprint(E)

    # print "Positions"
    P = list(itertools.product(range(col_count), range(row_count)))
    # pprint(P)

    # print "Admissible segments"
    S = [((i1, j1), (i2, j2)) for ((i1, j1), (i2, j2)) in itertools.combinations(P, 2) if hypot(abs(i1-i2), abs(j1-j2))-1 <= MAX_LENGTH]
    # pprint(S)

    # print "Crossing segments"
    S2X = []
    for (((i1, j1), (i2, j2)), ((i3, j3), (i4, j4))) in itertools.combinations(S, 2):
        if cross(i1, j1, i2, j2, i3, j3, i4, j4):
            S2X.append((((i1, j1), (i2, j2)), ((i3, j3), (i4, j4))))
    S2X = set(S2X)
    # pprint(S2X)
    
    lengths = [str(hypot(abs(i1-i2), abs(j1-j2)) - 1) for ((i1, j1), (i2, j2)) in S]
    lengths = ["" if s == "1.0" else (s[:-2] + " " if s.endswith(".0") else s + " ") for s in lengths]
    
    result.append("Minimize")
    result.append(" obj: " + summation("{length}y_{s[0][0]}_{s[0][1]}_{s[1][0]}_{s[1][1]}".format(length=length, s=s) for (length, s) in zip(lengths, S) if length != "0"))
    result.append("Subject To")
    
    result.append(u"\\ constraint:each_vertex_is_placed_at_exactly_one_position")
    for v in V:
        push("%s = 1" % summation("x_{v}_{p[0]}_{p[1]}".format(v=v, p=p) for p in P))
    
    result.append(u"\\ constraint:at_most_one_vertex_per_position")
    for p in P:
        push("%s <= 1" % summation("x_{v}_{p[0]}_{p[1]}".format(v=v, p=p) for v in V))
    
    result.append(u"\\ constraint:as_much_active_segments_around_a_point_as_successors_of_the_vertex_placed_on_this_point")
    for p in P:
        for v in V:
            push("%s - %s >= 0" % (
                summation("y_{s[0][0]}_{s[0][1]}_{s[1][0]}_{s[1][1]}".format(s=s) for s in S if s[0]==p or s[1]==p),
                "{n}x_{v}_{p[0]}_{p[1]}".format(v=v, p=p, n=len(successors[v]))
                )
            )
    
    result.append(u"\\ constraint:if_two_adjacent_vertices_are_placed_then_the_corresponding_segment_is_active")
    for (v1, v2) in E:
        for (p1, p2) in S:
            push("x_{v1}_{p1[0]}_{p1[1]} + x_{v2}_{p2[0]}_{p2[1]} + x_{v2}_{p1[0]}_{p1[1]} + x_{v1}_{p2[0]}_{p2[1]} - y_{p1[0]}_{p1[1]}_{p2[0]}_{p2[1]} <= 1".format(v1=v1, p1=p1, v2=v2, p2=p2))
    
    result.append(u"\\ constraint:two_adjacent_vertices_cannot_be_placed_on_points_too_far_away")
    for (v1, v2) in E:
        for (p1, p2) in set(itertools.combinations(P, 2)).difference(S):
            push("x_{v1}_{p1[0]}_{p1[1]} + x_{v2}_{p2[0]}_{p2[1]} + x_{v2}_{p1[0]}_{p1[1]} + x_{v1}_{p2[0]}_{p2[1]} <= 1".format(v1=v1, p1=p1, v2=v2, p2=p2))
    
    result.append(u"\\ as much active segments as edges")
    push("%s = %s" % (
        summation("y_{p1[0]}_{p1[1]}_{p2[0]}_{p2[1]}".format(p1=p1, p2=p2) for (p1, p2) in S),
        len(E)
        )
    )
    
    result.append(u"\\ The active segments do not cross each other")
    for (s1, s2) in S2X:
        push("y_{s1[0][0]}_{s1[0][1]}_{s1[1][0]}_{s1[1][1]} + y_{s2[0][0]}_{s2[0][1]}_{s2[1][0]}_{s2[1][1]} <= 1".format(s1=s1, s2=s2))
    
    result.append(u"\\ symmetry static cuts")
    push("%s - %s <= 0" % (
        summation("{order}x_0_{i}_{j}".format(order=i+j*col_count, i=i, j=j) for (i, j) in P),
        " - ".join("{order}x_1_{i}_{j}".format(order=i+j*col_count, i=i, j=j) for (i, j) in P),
    ))
    push("%s - %s <= 0" % (
        summation("{order}x_0_{i}_{j}".format(order=i+j*col_count, i=i, j=j) for (i, j) in P),
        " - ".join("{order}x_2_{i}_{j}".format(order=i+j*col_count, i=i, j=j) for (i, j) in P),
    ))

    result.append("Binary")
    result.append(" ".join("x_{v}_{p[0]}_{p[1]}".format(v=v, p=p) for v in V for p in P))
    result.append(" ".join("y_{s[0][0]}_{s[0][1]}_{s[1][0]}_{s[1][1]}".format(s=s) for s in S))
    
    result.append("\nEnd")
    # result.append("\noptimize\ndisplay solution variables -\n")
    
    with open("%s.lp" % path, "w") as f:
        f.write("\n".join(result))

def solve_with_cplex(path):
    import cplex
    problem = cplex.Cplex()
    problem.parameters.read.datacheck.set(0)
    problem.set_results_stream("%s_cplex.log" % path)
    problem.read(("%s.lp" % path).encode("utf8")) # unicode conversion required by CPLEX (undocumented)
    problem.solve()
    if problem.solution.get_status() != 103: # No solution exists
        return {
            "distances": problem.solution.get_objective_value(),
            "names": problem.variables.get_names(),
            "assigned": problem.solution.get_values(),
        }

def solve_with_gurobi(path):
    import gurobipy
    problem = gurobipy.read("%s.lp" % path)
    problem.setParam("OutputFlag", False)
    problem.optimize()
    if problem.status != gurobipy.GRB.Status.INFEASIBLE:
        return {
            "distances": problem.objVal,
            "names": [var.varName for var in problem.getVars()],
            "assigned": [var.X for var in problem.getVars()],
        }


def arrange(**params):
    (folder, filename) = os.path.split(params["output_name"])
    folder = os.path.join(folder, "cache")
    if not os.path.isdir(folder):
        os.mkdir(folder)
    path = os.path.join(folder, filename)
    dump_lp(path, **params)
    solution = None
    if params["engine"] == "cplex":
        solution = solve_with_cplex(path)
    elif params["engine"] == "gurobi":
        solution = solve_with_gurobi(path)
    if not solution:
        return
    result = {}
    result["crossings"] = 0
    result["distances"] = solution["distances"]
    result["layout"] = [None] * params["col_count"] * params["row_count"]
    for (name, assigned) in zip(solution["names"], solution["assigned"]):
        if assigned and name.startswith("x"):
            (v, x, y) = map(int, name.split("_")[1:])
            result["layout"][x + y * params["col_count"]] = v
    return result
