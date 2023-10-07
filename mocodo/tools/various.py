def invert_dict(d):
    return {v: k for (k, vs) in d.items() for v in vs}

def first_missing_positive(l):
    return min(set(range(1, len(l) + 2)).difference(l))
