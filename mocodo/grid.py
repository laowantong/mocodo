import math
import itertools
from collections import defaultdict

class Grid(list):
    
    def __init__(self, max_number_of_nodes=100, min_ratio=0.5):
        list.__init__(self)
        max_square_side = int(math.ceil(math.sqrt(max_number_of_nodes)))
        for n in range(max_square_side * max_square_side, 0, -1):
            for i in range(n, int(math.ceil(math.sqrt(n))) - 1, -1):
                if n % i == 0 and float(n)/i/i > min_ratio:
                    self.insert(0, (i, n/i))
                    break
            else:
                self.insert(0, self[0])
        self.insert(0, None)
    
    def get_nth_next(self, index, nth):
        acc = set()
        for i in itertools.count(index):
            acc.add(self[i])
            if len(acc) > nth:
                return self[i]
    
    def get_markdown(self):
        (w, h) = map(max, zip(*self[1:]))
        result = [[""] + map(lambda i: "**%s**" % i, range(1, w + 1))] + [["---"] * (w + 1)] + [["**%s**" % row] + [""] * w for row in range(1, h + 1)]
        for (n, (col, row)) in enumerate(self[1:], 1):
            result[row + 1][col] += ", %s" % n if result[row + 1][col] else str(n)
        return "\n".join(["| %s |" % " | ".join(row) for row in result])
