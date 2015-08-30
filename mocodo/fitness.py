#!/usr/bin/env python
# encoding: utf-8

from itertools import product
from math import hypot
from collections import Counter
from cross import cross

def fitness(links, col_count, row_count, max_crossing = 4):
    """ Return (by closure) a function evaluating the aesthetic quality of a given layout. """
    
    def evaluate(layout):
        for (position, index) in enumerate(layout):
            coordinates[index] = divmod(position, col_count)
        segments = [(coordinates[p1], coordinates[p2]) for (p1, p2) in links]
        total_distances = 0
        short_segments = []
        for  ((y1, x1), (y2, x2)) in segments:
            distance = distances[abs(x1-x2)][abs(y1-y2)]
            if distance <= max_crossing:
                short_segments.append((x1, y1, x2, y2))
            total_distances += distance
        crossing_count = (link_count - len(short_segments)) * link_count
        for (i, (x1, y1, x2, y2)) in enumerate(short_segments):
             for (x3, y3, x4, y4) in short_segments[i+1:]:
                 crossing_count += cross((x1, y1, x2, y2, x3, y3, x4, y4))
        return (crossing_count, total_distances)
    
    distances = [[hypot(i, j) - 1 for j in range(row_count)] for i in range(col_count)]
    coordinates = [(0, 0)] * (row_count * col_count)
    link_count = len(links)
    return evaluate
