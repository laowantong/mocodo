def invert_dict(d):
    return {v: k for (k, vs) in d.items() for v in vs}
