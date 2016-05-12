# http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/

def damerau_levenshtein(seq1, seq2):
    """Calculate the Damerau-Levenshtein distance between sequences.

    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first sequence into the
    second. Although generally used with strings, any sequences of
    comparable objects will work.

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.

    >>> damerau_levenshtein('ba', 'abc')
    2
    >>> damerau_levenshtein('fee', 'deed')
    2

    It works with arbitrary sequences too:
    >>> damerau_levenshtein('abcd', ['b', 'a', 'c', 'd', 'e'])
    2
    """
    # codesnippet:D0DE4716-B6E6-4161-9219-2903BF8F547F
    # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1 matrix.
    # However, only the current and two previous rows are needed at once,
    # so we only store those.
    one_ago = None
    this_row = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        # Python lists wrap around for negative indices, so put the
        # leftmost column at the *end* of the list. This matches with
        # the zero-indexed strings and saves extra calculation.
        two_ago, one_ago, this_row = one_ago, this_row, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            del_cost = one_ago[y] + 1
            add_cost = this_row[y - 1] + 1
            sub_cost = one_ago[y - 1] + (seq1[x] != seq2[y])
            this_row[y] = min(del_cost, add_cost, sub_cost)
            # This block deals with transpositions
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                and seq1[x-1] == seq2[y] and seq1[x] != seq2[y]):
                this_row[y] = min(this_row[y], two_ago[y - 2] + 1)
    return this_row[len(seq2) - 1]