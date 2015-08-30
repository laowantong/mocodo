#!/usr/bin/env python
# encoding: utf-8

class memoize(dict):
    def __init__(self, func):
        self.func = func
 
    def __call__(self, *args):
        return self[args]
 
    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result

crossed_strings = frozenset(["-++-","-++0","-+0-","-0+-","0++-","+--+","0--+","+0-+","+-0+","+--0"])

@memoize
def cross((x1, y1, x2, y2, x3, y3, x4, y4)):
    """ Tests whether the segments ((x1,y1), (x2,y2)) and ((x3,y3), (x4,y4)) intersect.
        Two segments sharing exactly one extremity are NOT considered as interesecting. """
    a = (x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)
    b = (x4-x3)*(y2-y3) - (y4-y3)*(x2-x3)
    c = (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)
    d = (x2-x1)*(y4-y1) - (y2-y1)*(x4-x1)
    if a or b or c or d:
        return "".join("+" if x>0 else ("-" if x<0 else "0") for x in (a,b,c,d)) in crossed_strings
    else: # the segments are collinear
        if x1 == x2:  # both segments are vertical
            if y1 < y2:
                if y3 < y4:
                    return y2 > y3 and y1 < y4
                else:
                    return y2 > y4 and y1 < y3
            else:
                if y3 < y4:
                    return y1 > y3 and y2 < y4
                else:
                    return y1 > y4 and y2 < y3
        else:
            if x1 < x2:
                if x3 < x4:
                    return x2 > x3 and x1 < x4
                else:
                    return x2 > x4 and x1 < x3
            else:
                if x3 < x4:
                    return x1 > x3 and x2 < x4
                else:
                    return x1 > x4 and x2 < x3
