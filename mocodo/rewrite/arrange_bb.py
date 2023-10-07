import contextlib
from functools import lru_cache
from itertools import count, product
from math import hypot
from random import choice, random, shuffle

from .cross import cross
from ..mocodo_error import MocodoError
from ..argument_parser import non_negative_integer, positive_integer
from ..mcd import Mcd

def arrange(source, subargs, has_expired):

    is_organic = False
    if "wide" in subargs:
        col_count = 8
        with contextlib.suppress(Exception):
            col_count = int(subargs["wide"]) or 1
        mcd = Mcd(source)
        (q, r) = divmod(mcd.get_non_phantom_count(), col_count)
        row_count = q + bool(r)
        source = mcd.get_refitted_clauses(col_count, row_count)
    elif "balanced" in subargs:
        nth_fit = 0
        with contextlib.suppress(Exception):
            nth_fit = int(subargs["balanced"])
        mcd = Mcd(source)
        source = mcd.get_refitted_clauses(nth_fit)
    elif "current" in subargs:
        pass
    else:
        is_organic = True
    
    mcd = Mcd(source)
    layout_data = mcd.get_layout_data()
    successors = layout_data["successors"]
    col_count = layout_data["col_count"]
    row_count = layout_data["row_count"]
    multiplicity = layout_data["multiplicity"]

    min_objective = non_negative_integer(subargs.get("min_objective", 0))
    max_objective = non_negative_integer(subargs.get("max_objective", 15))
    call_limit = positive_integer(subargs.get("call_limit", 10000))
    verbose = bool(subargs.get("verbose") is not None) # -t arrange:verbose => {"verbose": ""} => True

    has_expired = has_expired or (lambda: False)

    @lru_cache
    def bounded_neighborhood(x1, y1):
        result = set()
        for x2 in range(
            max(0, x1 - radius),
            min(col_count, x1 + radius + 1),
        ):
            for y2 in range(
                max(0, y1 - radius + abs(x1 - x2)),
                min(row_count, y1 + radius - abs(x1 - x2) + 1),
            ):
                if x1 != x2 or y1 != y2:
                    result.add((x2, y2))
        return result

    @lru_cache
    def organic_neighborhood(x1, y1):
        result = set()
        for x2 in range(x1 - radius, x1 + radius + 1):
            for y2 in range(y1 - radius + abs(x1 - x2), y1 + radius - abs(x1 - x2) + 1):
                if x1 != x2 or y1 != y2:
                    result.add((x2, y2))
        return result

    @lru_cache
    def bounded_hull(coords):
        result = set()
        for (x, y) in coords:
            if x - 1 >= 0:
                result.add((x - 1, y))
            if x + 1 < col_count:
                result.add((x + 1, y))
            if y - 1 >= 0:
                result.add((x, y - 1))
            if y + 1 < row_count:
                result.add((x, y + 1))
        return result.difference(coords)

    @lru_cache
    def organic_hull(coords):
        result = set()
        for (x, y) in coords:
            result.add((x - 1, y))
            result.add((x + 1, y))
            result.add((x, y - 1))
            result.add((x, y + 1))
        return result.difference(coords)

    def recurs(box_coords, next_boxes, placed_segments, cumulated_distances):
        if cumulated_distances > objective:
            # print("cut")
            return None
        if len(next_boxes) == 0:
            return {
                "coords": box_coords,
                "crossings": 0,
                "distances": cumulated_distances,
            }
        outside_hull_count = len(next_boxes) - len(hull(frozenset(box_coords.values())))
        if outside_hull_count * outside_hull_minimal_distance + cumulated_distances > objective:
            # print("Lower bound cut")
            return None
        if has_expired():
            raise MocodoError(10, _('Layout calculation time exceeded.'))  # fmt: skip
        if next(iteration) > call_limit:
            # print("call limit exceeded")
            return None
        box_to_place = next_boxes[0]
        placed_successors = {
            box_coords[box]: box for box in successors[box_to_place] if box in box_coords
        }
        if placed_successors:
            placed_successor_coords = iter(placed_successors)
            (x1, y1) = next(placed_successor_coords)
            possible_coords = neighborhood(x1, y1).copy()
            # print(placed_successors[0], possible_coords)
            for (x1, y1) in placed_successor_coords:
                possible_coords.intersection_update(neighborhood(x1, y1))
                if not possible_coords:
                    # print("neighborhood intersection is empty")
                    return None
        else:
            # print("the box to place has no successors: all empty coords are possible")
            possible_coords = set(product(range(col_count), range(row_count)))
        possible_coords.difference_update(box_coords.values())
        if not possible_coords:
            # print("neighborhood intersection is not free")
            return None
        non_crossing_possible_coords = []
        for (x1, y1) in possible_coords:
            for ((x2, y2), (x3, y3, x4, y4)) in product(placed_successors, placed_segments):
                if cross(x1, y1, x2, y2, x3, y3, x4, y4):
                    break
            else:
                non_crossing_possible_coords.append((x1, y1))
        if not non_crossing_possible_coords:
            # print("all possible coords result in a crossing with existing segment")
            return None
        weighted_possible_coords = []
        for (x1, y1) in non_crossing_possible_coords:
            cumulated_distance = 0
            for ((x2, y2), placed_box) in placed_successors.items():
                cumulated_distance += (
                    distances[abs(x1 - x2)][abs(y1 - y2)] * multiplicity[(box_to_place, placed_box)]
                )
            weighted_possible_coords.append((cumulated_distance, random(), x1, y1))
        weighted_possible_coords.sort()
        for (cumulated_distance, __, x1, y1) in weighted_possible_coords:  # For the double underscore, see __main__.py
            box_coords[box_to_place] = (x1, y1)
            new_segments = [(x1, y1, x2, y2) for (x2, y2) in placed_successors]
            new_next_boxes = list(
                successors[box_to_place].difference(box_coords).difference(next_boxes)
            )
            if len(next_boxes) == 1 and len(new_next_boxes) == 0 and len(box_coords) != box_count:
                # print("the placed boxes have no more non placed successors")
                new_next_boxes = list(set(range(box_count)).difference(box_coords))
                if new_next_boxes:
                    new_next_boxes = [choice(new_next_boxes)]
            shuffle(new_next_boxes)
            result = recurs(
                box_coords,
                next_boxes[1:] + new_next_boxes,
                placed_segments + new_segments,
                cumulated_distances + cumulated_distance,
            )
            if result:
                return result
            del box_coords[box_to_place]

    box_count = col_count * row_count
    neighborhood = organic_neighborhood if is_organic else bounded_neighborhood
    hull = organic_hull if is_organic else bounded_hull
    radius = 3
    distances = [[hypot(i, j) - 1 for j in range(radius + 1)] for i in range(radius + 1)]
    outside_hull_minimal_distance = distances[1][2]
    if all(not successor for successor in successors):
        # print("no link: return a random layout")
        layout = list(range(box_count))
        shuffle(layout)
        result = {
            "layout": layout,
            "crossings": 0,
            "distances": 0,
        }
        mcd.set_layout(**result)
        return mcd.get_clauses()
    for objective in range(min_objective, max_objective + 1):
        if verbose:
            print("Objective %s." % objective)
        boxes = list(range(box_count))
        shuffle(boxes)
        for first_box in boxes:
            iteration = count()
            if successors[first_box]:
                if verbose:
                    print("  Starting from box %s." % first_box)
                result = recurs({first_box: (0, 0)}, list(successors[first_box]), [], 0)
                if result:
                    coords = result["coords"]
                    if is_organic:
                        min_x = min(x for (x, y) in coords.values())
                        max_x = max(x for (x, y) in coords.values())
                        min_y = min(y for (x, y) in coords.values())
                        max_y = max(y for (x, y) in coords.values())
                        for (box_index, (x, y)) in coords.items():
                            coords[box_index] = (x - min_x, y - min_y)
                        result["row_count"] = row_count = max_y - min_y + 1
                        result["col_count"] = col_count = max_x - min_x + 1
                    result["layout"] = [None] * row_count * col_count
                    for (box_index, (x, y)) in coords.items():
                        result["layout"][x + y * col_count] = box_index
                    mcd.set_layout(**result)
                    if mcd.row_count > mcd.col_count:
                        # If the layout is taller than wide, transpose it.
                        return mcd.get_diagonally_flipped_clauses()
                    else:
                        return mcd.get_clauses()
                if is_organic:
                    break
        objective += 1
    if is_organic:
        raise MocodoError(41, _('Failed to calculate a non-constrained planar layout.'))  # fmt: skip
    else:
        raise MocodoError(9, _('Failed to calculate a planar layout satisfying the given constraint.'))  # fmt: skip


if __name__ == "__main__":
    # python -m mocodo.rewrite._arrange_bb

    from time import time
    import random
    from ..argument_parser import parsed_arguments
    from ..mcd import Mcd

    clauses = """
        SUSPENDISSE: diam
        SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
        CONSECTETUER: elit, sed
        MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

        DF, 11 LOREM, 1N SUSPENDISSE
        LOREM: ipsum, dolor, sit
        TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
        DIGNISSIM: ligula, massa, varius

        DF, 11 RISUS, 0N RISUS
        AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
        RISUS: ultricies, _cras, elementum
        SEMPER, 0N RISUS, 1N DIGNISSIM
    """
    params = parsed_arguments()
    mcd = Mcd(clauses.replace("  ", ""), **params)
    starting_time = time()
    random.seed(42)
    rearrangement = arrange(mcd, {"is_organic": True}, lambda: False)
    if rearrangement:
        print()
        mcd.set_layout(**rearrangement)
        print(mcd.get_clauses())
        print()
        print("Cumulated distances:", rearrangement["distances"])
        print("Duration:", time() - starting_time)
        print()
