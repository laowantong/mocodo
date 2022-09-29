from email.policy import default
import itertools
import re
from collections import defaultdict

from .association import Association
from .diagram_link import DiagramLink
from .entity import Entity
from .grid import Grid
from .mocodo_error import MocodoError
from .phantom import Phantom

def cmp(x, y):
    return (x > y) - (x < y)

SYS_MAXINT = 9223372036854775807 # an integer larger than any practical list or string index

class Mcd:

    def __init__(self, clauses, get_font_metrics=None, **params):
        
        def parse_clauses():
            self.entities = {}
            self.associations = {}
            seen = set()
            self.rows = [[]]
            self.header = ""
            pages = defaultdict(list)
            for clause in clauses:
                indentation = len(clause) - len(clause.lstrip())
                clause = clause.strip(" \n\r\t")
                if not clause:
                    self.rows.append([])
                    continue
                if clause.startswith("%"):
                    if not self.rows[-1]:
                        self.header += "%s\n" % clause
                    continue
                if clause == ":" * len(clause):
                    self.rows[-1].extend(Phantom(next(phantom_counter)) for _ in clause)
                    continue
                if clause.startswith(":"):
                    raise MocodoError(19, _('The clause "{clause}" starts with a colon.').format(clause=clause)) # fmt: skip
                clause = re.sub("\[.+?\]", substitute_forbidden_symbols_between_brackets, clause)
                if "," in clause.split(":", 1)[0] or re.match(r"\s*(/\w*\\)", clause):
                    element = Association(clause, **params)
                    if element.name in self.associations:
                        raise MocodoError(7, _('Duplicate association "{name}". If you want to make two associations appear with the same name, you must suffix it with a number.').format(name=element.name)) # fmt: skip
                    self.associations[element.name] = element
                    pages[indentation].append(element)
                elif ":" in clause:
                    element = Entity(clause)
                    if element.name in self.entities:
                        raise MocodoError(6, _('Duplicate entity "{name}". If you want to make two entities appear with the same name, you must suffix it with a number.').format(name=element.name)) # fmt: skip
                    self.entities[element.name] = element
                    pages[indentation].append(element)
                else:
                    raise MocodoError(21, _('"{clause}" does not constitute a valid declaration of an entity or association.').format(clause=clause)) # fmt: skip
                if element.name in seen:
                    raise MocodoError(8, _('One entity and one association share the same name "{name}".').format(name=element.name)) # fmt: skip
                seen.add(element.name)
                self.rows[-1].append(element)
            if not seen:
                raise MocodoError(4, _('The ERD is empty.')) # fmt: skip
            self.rows = [row for row in self.rows if row]
            self.col_count = max(len(row) for row in self.rows)
            self.row_count = len(self.rows)
            self.page_count = len(pages)
            for (i, (indentation, elements)) in enumerate(sorted(pages.items(), key=lambda x: x[0])):
                for element in elements:
                    element.page = i
        
        def add_legs():
            for association in self.associations.values():
                for leg in association.legs:
                    try:
                        entity = self.entities[leg.entity_name]
                    except KeyError:
                        if leg.entity_name in self.associations:
                            raise MocodoError(20, _('Association "{association}" linked to another association "{entity}"!').format(association=association.name, entity=leg.entity_name)) # fmt: skip
                        else:
                            raise MocodoError(1, _('Association "{association}" linked to an unknown entity "{entity}"!').format(association=association.name, entity=leg.entity_name)) # fmt: skip
                    leg.register_entity(entity)
        
        def add_attributes():
            legs_to_strengthen = dict((entity_name, []) for entity_name in self.entities)
            children = set()
            for association in self.associations.values():
                for leg in association.legs:
                    if association.kind.startswith("inheritance") and leg.card == "XX":
                        children.add(leg.entity_name)
                    if leg.kind == "strengthening":
                        legs_to_strengthen[leg.entity_name].append(leg)
            for (entity_name, legs) in legs_to_strengthen.items():
                self.entities[entity_name].add_attributes(legs, entity_name in children)
        
        def tweak_straight_cards():
            coordinates = {}
            for (j, row) in enumerate(self.rows):
                for (i, box) in enumerate(row):
                    coordinates[box] = (i, j)
            d = defaultdict(list)
            tweakable_legs = {}
            for association in self.associations.values():
                for leg in association.legs:
                    (ei, ej) = coordinates[leg.entity]
                    (ai, aj) = coordinates[leg.association]
                    vector = (cmp(ai, ei), cmp(aj, ej))
                    vector = (" SN"[cmp(aj, ej)] + " EW"[cmp(ai, ei)]).strip()
                    d[leg.entity].append(vector)
                    tweakable_legs[(leg.entity, vector)] = leg
            flex = params.get("flex", 0)
            for (entity, vectors) in d.items():
                for vector in vectors:
                    leg = tweakable_legs[(entity, vector)]
                    if not leg.card_view.strip():
                        continue
                    elif vector == "E":
                        if vectors.count("E") == 1 and "SE" in vectors and "NE" not in vectors:
                            leg.twist = True
                    elif vector == "S":
                        if vectors.count("S") == 1 and "SE" in vectors and "SW" not in vectors:
                            leg.twist = True
                    elif vector == "W":
                        if vectors.count("W") == 1 and "SW" in vectors and "NW" not in vectors:
                            leg.twist = True
                    elif vector == "N":
                        if vectors.count("N") == 1 and "NE" in vectors and "NW" not in vectors:
                            leg.twist = True
                    elif flex == 0:
                        continue
                    elif vector == "SE" and vectors.count("SE") == 1:
                        if vectors.count("E") > 1:
                            leg.set_spin_strategy(flex)
                        elif vectors.count("S") > 1:
                            leg.set_spin_strategy(-flex)
                    elif vector == "SW" and vectors.count("SW") == 1:
                        if vectors.count("S") > 1:
                            leg.set_spin_strategy(flex)
                        elif vectors.count("W") > 1:
                            leg.set_spin_strategy(-flex)
                    elif vector == "NW" and vectors.count("NW") == 1:
                        if vectors.count("W") > 1:
                            leg.set_spin_strategy(flex)
                        elif vectors.count("N") > 1:
                            leg.set_spin_strategy(-flex)
                    elif vector == "NE" and vectors.count("NE") == 1:
                        if vectors.count("N") > 1:
                            leg.set_spin_strategy(flex)
                        elif vectors.count("E") > 1:
                            leg.set_spin_strategy(-flex)
        
        def add_diagram_links():
            self.diagram_links = []
            for entity in self.entities.values():
                for attribute in entity.attributes:
                    if attribute.primary_entity_name:
                        self.diagram_links.append(DiagramLink(self.entities, entity, attribute))
            
        def may_center():
            for row in self.rows:
                n = self.col_count - len(row)
                if n:
                    row[0:0] = [Phantom(next(phantom_counter)) for i in range(n // 2)]
                    row.extend(Phantom(next(phantom_counter)) for i in range(n // 2 + n % 2))
        
        def make_boxes():
            i = itertools.count()
            self.boxes = []
            for row in self.rows:
                for box in row:
                    box.identifier = next(i)
                    self.boxes.append(box)
                    box.register_boxes(self.boxes)
            self.box_count = len(self.boxes)
        
        def substitute_forbidden_symbols_between_brackets(text):
            """Neutralize Mocodo syntax separators in the text between brackets."""
            return text.group().replace(",", "<<<safe-comma>>>").replace(":", "<<<safe-colon>>>")
        
        self.get_font_metrics = get_font_metrics
        phantom_counter = itertools.count()
        parse_clauses()
        add_legs()
        add_attributes()
        add_diagram_links()
        may_center()
        make_boxes()
        tweak_straight_cards()
        self.title = params.get("title", "Untitled")
    
    def get_layout_data(self):
        successors = [set() for i in range(self.box_count)] # use `set` to deduplicate reflexive associations
        multiplicity = defaultdict(int) # but count the multiplicity (1 or 2) of each link
        if self.associations:
            for association in self.associations.values():
                for leg in association.legs:
                    successors[association.identifier].add(leg.entity.identifier)
                    successors[leg.entity.identifier].add(association.identifier)
                    multiplicity[(association.identifier, leg.entity.identifier)] += 1
                    multiplicity[(leg.entity.identifier, association.identifier)] += 1
        else:
            for diagram_link in self.diagram_links:
                fei = diagram_link.foreign_entity.identifier
                pei = diagram_link.primary_entity.identifier
                if fei != pei:
                    successors[fei].add(pei)
                    successors[pei].add(fei)
                    multiplicity[(fei, pei)] += 1
                    multiplicity[(pei, fei)] += 1
        return {
            "links": tuple((node, child) for (node, children) in enumerate(successors) for child in children if node < child),
            "successors": successors,
            "col_count": self.col_count,
            "row_count": self.row_count,
            "multiplicity": dict(multiplicity)
        }
    
    def get_layout(self):
        return [box.identifier for row in self.rows for box in row]
    
    def get_row_text(self, row):
        result = []
        for box in row:
            clause = "  " * box.page + box.clause
            clause = clause.replace("<<<safe-comma>>>", ",")
            clause = clause.replace("<<<safe-colon>>>", ":")
            result.append(clause)
        return "\n".join(result)
    
    def set_layout(self, layout, col_count=None, row_count=None, **kwargs):
        if col_count and row_count:
            (self.col_count, self.row_count) = (col_count, row_count)
        def get_or_create_box(index):
            return Phantom() if layout[index] is None else self.boxes[layout[index]]
        i = itertools.count()
        self.rows = [[get_or_create_box(next(i)) for x in range(self.col_count)] for y in range(self.row_count)]
        def suppress_empty_rows(y):
            while self.rows: # there's at least one row
                for box in self.rows[y]:
                    if box.kind != "phantom":
                        return
                del self.rows[y]
                self.row_count -= 1
        suppress_empty_rows(0)
        suppress_empty_rows(-1)
        def suppress_empty_cols(x):
            while self.rows[0]: # there's at least one column
                for row in self.rows:
                    if row[x].kind != "phantom":
                        return
                for row in self.rows:
                    del row[x]
                self.col_count -= 1
        suppress_empty_cols(0)
        suppress_empty_cols(-1)
    
    def get_clauses(self):
        result = self.header
        if self.associations:
            result += "\n\n".join(self.get_row_text(row) for row in self.rows)
        else:
            result += "\n\n".join(":\n" + "\n:\n".join(self.get_row_text(row).split("\n")) + "\n:" for row in self.rows)
        return result
    
    def get_clauses_horizontal_mirror(self):
        return self.header + "\n\n".join(self.get_row_text(row) for row in self.rows[::-1])
    
    def get_clauses_vertical_mirror(self):
        return self.header + "\n\n".join(self.get_row_text(row[::-1]) for row in self.rows)
    
    def get_clauses_diagonal_mirror(self):
        return self.header + "\n\n".join(self.get_row_text(row) for row in zip(*self.rows))
    
    def get_reformatted_clauses(self, nth_fit):
        grid = Grid(len(self.boxes) + 100) # make sure there are enough precalculated grids
        start = len(self.entities) + len(self.associations) # number of nonempty boxes
        if nth_fit < 0:
            if (self.col_count, self.row_count) in grid: # the current grid is among precalculated ones
                start = self.col_count * self.row_count # start from the completed grid
            nth_fit = 1 # and calculate the next one
        (col_count, row_count) = grid.get_nth_next(start, nth_fit)
        result = []
        i = 0
        for box in self.boxes:
            if box.kind != "phantom":
                if i % col_count == 0 and i:
                    result.append("")
                result.append("  " * box.page + box.clause)
                i += 1
        for i in range(i, col_count * row_count):
            if i % col_count == 0 and i:
                result.append("")
            result.append(":")
        return self.header + "\n".join(result)
    
    def calculate_size(self, style):

        def increase_margins_in_presence_of_clusters():
            for association in self.associations.values():
                if association.kind == "cluster":
                    style["margin"] *= 2
                    style["card_margin"] *= 2
                    break

        def card_max_width():
            get_pixel_width = self.get_font_metrics(style["card_font"]).get_pixel_width
            cardinalities = {"0,N"} # default value, in case there is no cardinalities at all
            for association in self.associations.values():
                for leg in association.legs:
                    cardinalities.add(leg.card_view.strip("_"))
            return max(map(get_pixel_width, cardinalities))
        #
        def calculate_sizes():
            for row in self.rows:
                for (i, box) in enumerate(row):
                    box.calculate_size(style, self.get_font_metrics)
                    max_box_width_per_column[i] = max(box.w, max_box_width_per_column[i])
            for diagram_link in self.diagram_links:
                diagram_link.calculate_size(style, self.get_font_metrics)
        #
        def make_horizontal_layout():
            self.w = style["margin"]
            for row in self.rows:
                horizontal_offset = style["margin"]
                for (i, box) in enumerate(row):
                    box.x = horizontal_offset + (max_box_width_per_column[i] - box.w) // 2
                    horizontal_offset += max_box_width_per_column[i] + join_width
                self.w = max(self.w, horizontal_offset)
            self.w += style["margin"] - join_width
        #
        def compress_horizontally():
            dx = 0
            for i in range(1, self.col_count):
                dx = SYS_MAXINT
                for row in self.rows:
                    b1 = row[i-1]
                    b2 = row[i]
                    space = b2.x - b1.x - b1.w - join_width
                    dx = min(dx, space)
                for row in self.rows:
                    row[i].x -= dx
            self.w -= dx
        #
        def make_vertical_layout():
            vertical_offset = style["margin"]
            for row in self.rows:
                max_box_height = max(box.h for box in row)
                for box in row:
                    box.y = vertical_offset + (max_box_height - box.h) // 2
                vertical_offset += max_box_height + join_height
            self.h = vertical_offset + style["margin"] - join_height
        #
        def compress_vertically():
            dy = 0
            for j in range(1, self.row_count):
                dy = SYS_MAXINT
                for (i2, b2) in enumerate(self.rows[j]):
                    y1_max = 0
                    for (i1, b1) in enumerate(self.rows[j-1]):
                        if (i1 == i2) or (b1.x < b2.x < b1.x + b1.w + join_width) or (b1.x - join_width < b2.x + b2.w < b1.x + b1.w):
                            y1_max = max(y1_max, b1.y + b1.h)
                    space = b2.y - y1_max - join_height
                    dy = min(dy, space)
                for box in self.rows[j]:
                    box.y -= dy
            self.h -= dy
        #

        increase_margins_in_presence_of_clusters()
        style["card_max_width"] = card_max_width()
        style["card_max_height"] = self.get_font_metrics(style["card_font"]).get_pixel_height()
        join_width  = 2 * style["card_margin"] + style["card_max_width"]
        join_height = 2 * style["card_margin"] + style["card_max_height"]
        max_box_width_per_column = [0] * self.col_count
        calculate_sizes()
        make_horizontal_layout()
        compress_horizontally()
        make_vertical_layout()
        compress_vertically()
    
    def description(self, style, geo):
        for box in self.boxes:
            box.register_center(geo)
        result = []
        for element in self.entities.values():
            result.extend(element.description(style, geo))
        for element in self.associations.values():
            result.extend(element.description(style, geo))
        for element in self.diagram_links:
            result.extend(element.description(style, geo))
        result.append(("comment", {"text": "Notes"}))
        result.append(
            (
                "notes",
                {
                    "height_threshold": geo["height"] - style["note_overlay_height"] - style["card_margin"],
                    "overlay_height": style["note_overlay_height"],
                    "x": geo["width"] // 2,
                    "y_top": style["note_baseline"],
                    "y_bottom": geo["height"] - style["note_overlay_height"] + style["note_baseline"],
                    "y": geo["height"] - style["note_overlay_height"],
                    "color": style["note_color"],
                    "text_color": style["note_text_color"],
                    "opacity": style["note_opacity"],
                    "font_family": style["note_font"]["family"],
                    "font_size": style["note_font"]["size"],
                }
            )
        )
        if self.page_count > 1:
            diameter = style["note_overlay_height"] / 4
            result.append(("comment", {"text": "Pager"}))
            for i in range(self.page_count):
                result.append(
                    (
                        "pager_dot",
                        {
                            "cx": geo["width"] / 2 - (self.page_count - 1 - 2 * i) * diameter,
                            "cy": geo["height"] + 2 * diameter,
                            "r": diameter / 2,
                            "color": "lightgray" if i else "gray",
                            "page": i,
                        }
                    )
                )
            result.append(("pager", {"page_count": self.page_count}))
        return result
    
    def get_overlaps(self):
        """
        Detect the cases when two legs overlap each other or when a leg overlaps a box.
        
        The detection is based on the assumption that the boxes are arranged in a grid
        (and doesn't take into account any tweaks that may have been applied to the box
        centers). To unify the detection, the boxes are treated as zero-length legs.
        Only horizontal and vertical overlaps are detected.
        """
        coordinates = {}
        for (j, row) in enumerate(self.rows):
            for (i, box) in enumerate(row):
                coordinates[box] = (i, j)
        segments = defaultdict(list)
        for entity in self.entities.values():
            (ie, je) = coordinates[entity]
            segments["i", ie].append((je, je, entity, entity))
            segments["j", je].append((ie, ie, entity, entity))
        for association in self.associations.values():
            (ia, ja) = coordinates[association]
            segments[("i", ia)].append((ja, ja, association, association))
            segments[("j", ja)].append((ia, ia, association, association))
            for leg in association.legs:
                (ie, je) = coordinates[leg.entity]
                if ia == ie:
                    segments[("i", ia)].append((*sorted([ja, je]), association, leg.entity))
                elif ja == je:
                    segments[("j", ja)].append((*sorted([ia, ie]), association, leg.entity))
        result = []
        for quadruples in segments.values():
            quadruples.sort()
            for (l1, r1, e1, a1), (l2, r2, e2, a2) in zip(quadruples, quadruples[1:]):
                if e1.name == e2.name and a1.name == a2.name: # reflexive association
                    continue
                if l2 < r1:
                    result.append((e1.name, a1.name, e2.name, a2.name))
        return result

if __name__=="__main__":
    from .argument_parser import parsed_arguments
    clauses = """
        CLIENT: Réf. client, Nom, Prénom, Adresse
        PASSER, 0N CLIENT, 11 COMMANDE
        COMMANDE: Num commande, Date, Montant
        INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
        PRODUIT: Réf. produit, Libellé, Prix unitaire
    """.replace("  ", "").split("\n")
    params = parsed_arguments()
    mcd = Mcd(clauses, **params)
    print(mcd.get_clauses_vertical_mirror())
