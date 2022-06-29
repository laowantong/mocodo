import itertools
import math


class Grid(list):
    
    def __init__(self, max_number_of_nodes=100, min_balance=0.5):
        """Create a list of couples of dimensions.
        
        The nth couple is the tightest balanced rectangle having at least n cells.
        A balanced rectangle satisfies: length / width > min_balance.
        [None, (1, 1), (2, 2), (2, 2), (2, 2), (3, 2), (3, 2), (3, 3), ...]
        """
        list.__init__(self)
        max_square_side = int(math.ceil(math.sqrt(max_number_of_nodes)))
        for n in range(max_square_side * max_square_side, 0, -1):
            for i in range(n, int(math.ceil(math.sqrt(n))) - 1, -1):
                if n % i == 0 and n / i / i > min_balance:
                    self.insert(0, (i, n // i))
                    break
            else:
                self.insert(0, self[0])
        self.insert(0, None)
        self[2:4] = [(2, 1), (3, 1)] # tweak the 2- and 3-box grids
    
    def get_nth_next(self, index, nth):
        """Return the nth next distinct rectangle after the index-th one."""
        acc = set()
        for i in itertools.count(index):
            acc.add(self[i])
            if len(acc) > nth:
                return self[i]
    
    def get_markdown(self):
        """Return the grid as a nicely formatted table. For the docs only."""
        (w, h) = map(max, zip(*self[1:]))
        result = \
            [
                [""] + 
                list(map(lambda i: "**%s**" % i, range(1, w + 1)))
            ] + \
            [["---"] * (w + 1)] + \
            [
                ["**%s**" % row] + 
                [""] * w for row in range(1, h + 1)
            ]
        for (n, (col, row)) in enumerate(self[1:], 1):
            result[row + 1][col] += (", %s" % n if result[row + 1][col] else str(n))
        return "\n".join(["| %s |" % " | ".join(row) for row in result])


if __name__ == "__main__":
    grid = Grid()
    print(grid.get_markdown())
