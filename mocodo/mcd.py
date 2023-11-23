import itertools
from collections import defaultdict
from hashlib import md5
import json
from pathlib import Path

from .association import Association
from .attribute import Attribute
from .constraint import Constraint
from .diagram_link import DiagramLink
from .entity import Entity
from .grid import Grid
from .inheritance import Inheritance
from .mocodo_error import MocodoError
from .phantom import Phantom
from .tools.string_tools import raw_to_bid
from .tools.parser_tools import extract_clauses

def cmp(x, y):
    return (x > y) - (x < y)

SYS_MAXINT = 9223372036854775807 # an integer larger than any practical list or string index

class Mcd:

    def __init__(self, source, get_font_metrics=None, **params):
        
        def calculate_uid():
            h = md5(source.encode("utf-8")).hexdigest()
            if params.get("uid_suffix"):
                return f"{h[:8]}_{params['uid_suffix']}"
            else:
                return h[:8]

        def create():
            self.entities = {}
            self.associations = {}
            self.constraints = []
            self.inheritances = []
            mcd_has_cif = False
            self.commented_lines = []
            self.constraint_clauses = []
            seen = set()
            self.rows = [[]]
            pages = defaultdict(list)
            for clause in extract_clauses(source):
                indentation = clause.get("indent", "")
                if clause["type"] == "break":
                    self.rows.append([])
                    continue
                if clause["type"] == "comment":
                    if not self.rows[-1]:
                        self.commented_lines.append(clause["text"])
                    continue
                if clause["type"] == "phantoms":
                    phantoms = [Phantom() for _ in range(clause["count"])]
                    if self.rows[-1]:
                        self.rows[-1].extend(phantoms)
                    else:
                        self.rows.append(phantoms)
                    continue
                if clause["type"] == "constraint":
                    element = Constraint(clause)
                    if element.name_view == "CIF":
                        mcd_has_cif = True
                    self.constraints.append(element)
                    pages[indentation].append(element)
                    self.constraint_clauses.append(clause)
                    continue
                if clause["type"] == "inheritance":
                    element = Inheritance(clause, **params)
                    self.inheritances.append(element)
                    pages[indentation].append(element)
                else:
                    if clause["type"] == "association":
                        element = Association(clause, **params)
                        if element.bid in self.associations:
                            raise MocodoError(7, _('Duplicate association "{name}". If you want to make two associations appear with the same name, you must suffix it with a number.').format(name=element.raw_name)) # fmt: skip
                        self.associations[element.bid] = element
                        pages[indentation].append(element)
                    elif clause["type"] == "entity":
                        element = Entity(clause)
                        if element.bid in self.entities:
                            raise MocodoError(6, _('Duplicate entity "{name}". If you want to make two entities appear with the same name, you must suffix it with a number.').format(name=element.raw_name)) # fmt: skip
                        self.entities[element.bid] = element
                        pages[indentation].append(element)
                    else:
                        raise NotImplementedError
                    if element.bid in seen:
                        raise MocodoError(8, _('One entity and one association share the same name "{name}".').format(name=element.raw_name)) # fmt: skip
                    seen.add(element.bid)
                self.rows[-1].append(element)
            if not seen:
                raise MocodoError(4, _('The ERD "{title}" is empty.').format(title=params["title"])) # fmt: skip
            self.rows = [row for row in self.rows if row]
            self.col_count = max(len(row) for row in self.rows)
            self.row_count = len(self.rows)
            self.page_count = len(pages)
            for (i, (indentation, elements)) in enumerate(sorted(pages.items(), key=lambda x: x[0])):
                for element in elements:
                    element.page = i
            self.header = "\n".join(self.commented_lines) + "\n\n" if self.commented_lines else ""
            for association in self.associations.values():
                association.register_mcd_has_cif(mcd_has_cif)
        
        def add_legs():
            for association in self.associations.values():
                for leg in association.legs:
                    if leg.entity_bid in self.entities:
                        entity = self.entities[leg.entity_bid]
                    elif leg.entity_bid in self.associations:
                        raise MocodoError(18, _('Association "{association}" linked to another association "{entity}"!').format(association=association.bid, entity=leg.entity_bid)) # fmt: skip
                    else:
                        raise MocodoError(1, _('Association "{association}" linked to an unknown entity "{entity}"!').format(association=association.bid, entity=leg.entity_bid)) # fmt: skip
                    leg.register_entity(entity)
            for inheritance in self.inheritances:
                for leg in inheritance.legs:
                    if leg.entity_bid in self.entities:
                        entity = self.entities[leg.entity_bid]
                    elif leg.entity_bid in self.associations:
                        raise MocodoError(44, _('Inheritance "{inheritance}" linked to an association "{entity}"!').format(inheritance=inheritance.bid, entity=leg.entity_bid))
                    else:
                        raise MocodoError(42, _('Inheritance "{inheritance}" linked to an unknown entity "{entity}"!').format(inheritance=inheritance.bid, entity=leg.entity_bid))
                    leg.register_entity(entity)
            for constraint in self.constraints:
                for leg in constraint.legs:
                    if leg.bid in self.associations:
                        box = self.associations[leg.bid]
                    elif leg.bid in self.entities:
                        box = self.entities[leg.bid]
                    else:
                        raise MocodoError(40, _('Constraint "{constraint}" linked to an unknown entity or association "{box}"!').format(constraint=constraint.bid, box=leg.bid)) # fmt: skip
                    leg.register_box(box)
                for coord in constraint.coords:
                    if isinstance(coord, (float, int)):
                        continue
                    bid = raw_to_bid(coord)
                    if bid in self.associations or bid in self.entities:
                        continue
                    raise MocodoError(43, _('Constraint "{constraint}" aligned with an unknown entity or association "{box}"!').format(constraint=constraint.bid, box=bid)) # fmt: skip
        
        def add_attributes():
            strengthening_legs = dict((entity_bid, []) for entity_bid in self.entities)
            for association in self.associations.values():
                for leg in association.legs:
                    if leg.kind == "strengthening":
                        strengthening_legs[leg.entity_bid].append(leg)
            children = set()
            for inheritance in self.inheritances:
                for leg in inheritance.legs[1:]: # the first leg is the parent
                    children.add(leg.entity_bid) # the other legs are its children
            Attribute.id_gutter_strong_string = params["id_gutter_strong_string"]
            Attribute.id_gutter_weak_string = params["id_gutter_weak_string"]
            Attribute.id_gutter_alts = params["id_gutter_alts"]
            for (entity_bid, entity) in self.entities.items():
                entity.add_attributes(
                    legs_to_strengthen=strengthening_legs[entity_bid],
                    is_child=entity_bid in children,
                    fk_format=params.get("fk_format", "#{label}")
                )
            self.has_alt_identifier = any(entity.has_alt_identifier for entity in self.entities.values())

        def check_weak_entities_without_discriminator():
            too_weak_entities = defaultdict(int)
            for association in self.associations.values():
                for leg in association.legs:
                    if leg.kind != "strengthening":
                        continue
                    for attribute in leg.entity.attributes:
                        if attribute.kind == "weak":
                            break
                    else: # the weak entity has no discriminator.
                        # Ensure the max cards of the other legs are 1
                        for other_leg in association.legs:
                            if other_leg is leg:
                                continue
                            if other_leg.card[1] != "1":
                                # Otherwise, accumulate them
                                too_weak_entities[leg.entity.bid] += 1
            for (too_weak_entity, count) in too_weak_entities.items():
                if count < 2: # one isolated "too weak entity"
                    raise MocodoError(50, _('The weak entity "{entity}" should have a discriminator.').format(entity=too_weak_entity)) # fmt: skip
        
        def set_id_gutter_visibility():
            flag = params["id_gutter_visibility"]
            is_visible = flag == "on" or (flag == "auto" and self.has_alt_identifier)
            for entity in self.entities.values():
                entity.set_id_gutter_visibility(is_visible)
        
        def tweak_straight_cards():
            coordinates = {}
            for (j, row) in enumerate(self.rows):
                for (i, box) in enumerate(row):
                    coordinates[box] = (i, j)
            d = defaultdict(list)
            tweakable_legs = {}
            for association in self.associations.values():
                if association.is_invisible:
                    continue
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
                    if attribute.primary_entity_bid:
                        self.diagram_links.append(DiagramLink(self.entities, entity, attribute))
            
        def may_center():
            for row in self.rows:
                n = self.col_count - len(row)
                if n:
                    row[0:0] = [Phantom() for i in range(n // 2)]
                    row.extend(Phantom() for i in range(n // 2 + n % 2))
        
        def make_boxes():
            i = itertools.count()
            self.boxes = []
            for row in self.rows:
                for box in row:
                    box.index = next(i)
                    self.boxes.append(box)
                    box.register_boxes(self.boxes)
            self.box_count = len(self.boxes)

        # The following keys are actually created by __main__.py.
        # Using `get` instead of `[]` is for testing purposes only.
        params.setdefault("id_gutter_strong_string", "ID")
        params.setdefault("id_gutter_weak_string", "id")
        params.setdefault("id_gutter_alts", dict(zip("123456789", "123456789")))
        params.setdefault("id_gutter_visibility", "auto")

        self.get_font_metrics = get_font_metrics
        Phantom.reset_counter()
        Association.reset_df_counter()
        Inheritance.reset_counter()
        Constraint.reset_counter()
        self.uid = calculate_uid()
        create()
        self.update_footer()
        add_legs()
        add_attributes()
        check_weak_entities_without_discriminator()
        set_id_gutter_visibility()
        add_diagram_links()
        may_center()
        make_boxes()
        tweak_straight_cards()
        self.title = params.get("title", "Untitled")
    
    def update_footer(self):
        constraint_sources = [constraint.source for constraint in self.constraints]
        self.footer = "\n\n" + "\n".join(constraint_sources) if constraint_sources else ""

    def get_layout_data(self):
        successors = [set() for i in range(self.box_count)] # use `set` to deduplicate reflexive associations
        multiplicity = defaultdict(int) # but count the multiplicity (1 or 2) of each link
        for inheritance in self.inheritances:
            for leg in inheritance.legs:
                successors[inheritance.index].add(leg.entity.index)
                successors[leg.entity.index].add(inheritance.index)
                multiplicity[(inheritance.index, leg.entity.index)] += 1
                multiplicity[(leg.entity.index, inheritance.index)] += 1
        if self.associations:
            for association in self.associations.values():
                for leg in association.legs:
                    successors[association.index].add(leg.entity.index)
                    successors[leg.entity.index].add(association.index)
                    multiplicity[(association.index, leg.entity.index)] += 1
                    multiplicity[(leg.entity.index, association.index)] += 1
        else:
            for diagram_link in self.diagram_links:
                fei = diagram_link.foreign_entity.index
                pei = diagram_link.primary_entity.index
                if fei != pei:
                    successors[fei].add(pei)
                    successors[pei].add(fei)
                    multiplicity[(fei, pei)] += 1
                    multiplicity[(pei, fei)] += 1
        links = tuple((node, child) for (node, children) in enumerate(successors) for child in children if node < child)
        return {
            "links": links,
            "successors": successors,
            "col_count": self.col_count,
            "row_count": self.row_count,
            "multiplicity": dict(multiplicity)
        }
    
    def get_layout(self):
        return [box.index for row in self.rows for box in row]
    
    def get_row_text(self, row):
        return "\n".join(box.source for box in row)
    
    def get_non_phantom_count(self):
        return sum(box.kind != "phantom" for box in self.boxes)

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
        return result + self.footer

    def get_vertically_flipped_clauses(self):
        for constraint in self.constraints:
            constraint.invert_coords_horizontal_mirror()
        self.update_footer()
        return self.header + "\n\n".join(self.get_row_text(row) for row in self.rows[::-1]) + self.footer
    
    def get_horizontally_flipped_clauses(self):
        for constraint in self.constraints:
            constraint.invert_coords_vertical_mirror()
        self.update_footer()
        return self.header + "\n\n".join(self.get_row_text(row[::-1]) for row in self.rows) + self.footer
    
    def get_diagonally_flipped_clauses(self):
        for constraint in self.constraints:
            constraint.invert_coords_diagonal_mirror()
        self.update_footer()
        return self.header + "\n\n".join(self.get_row_text(row) for row in zip(*self.rows)) + self.footer
    
    def get_refitted_clauses(self, nth_fit_or_col_count, row_count=None):
        if row_count:
            col_count = nth_fit_or_col_count
        else:
            nth_fit = nth_fit_or_col_count
            grid = Grid(len(self.boxes) + 100) # make sure there are enough precalculated grids
            start = len(self.entities) + len(self.associations) # number of nonempty boxes
            (col_count, row_count) = grid.get_nth_next(start, nth_fit)
        result = []
        i = 0
        for box in self.boxes:
            if box.kind != "phantom":
                if i % col_count == 0 and i:
                    result.append("")
                result.append("  " * box.page + box.source.rstrip())
                i += 1
        for i in range(i, col_count * row_count):
            if i % col_count == 0 and i:
                result.append("")
            result.append(":")
        return self.header + "\n".join(result) + self.footer


    def calculate_or_retrieve_geo(self, params):
        geo_path = Path(f"{params['output_name']}_geo.json")
        if geo_path.is_file() and params["scale"] == 1 and params["reuse_geo"]:
            try:
                web_geo = json.loads(geo_path.read_text(encoding="utf8"))
            except:
                raise MocodoError(33, _('Unable to reuse the geometry file "{filename}".').format(filename=geo_path)) # fmt: skip
            # convert lists of couples to dicts
            geo = {}
            for (k, v) in web_geo.items():
                if isinstance(v, list):
                    geo[k] = dict(v)
                else:
                    geo[k] = v
            return geo
        geo = {
            "width": self.w,
            "height": self.h,
            "cx": {
                box.bid: box.x + box.w // 2
                for row in self.rows
                for box in row
                if box.kind != "phantom"
            },
            "cy": {
                box.bid: box.y + box.h // 2
                for row in self.rows
                for box in row
                if box.kind != "phantom"
            },
            "shift": {
                leg.lid: 0
                for row in self.rows
                for box in row
                for leg in box.legs
                if hasattr(leg, "card_view")},
            "ratio": {
                leg.lid: 1.0
                for row in self.rows
                for box in row
                for leg in box.legs
                if leg.arrow
            },
        }
        web_geo = {k: list(v.items()) if isinstance(v, dict) else v for (k, v) in geo.items()}
        text = json.dumps(web_geo, indent=2, ensure_ascii=False)
        text = text.replace("\n      ", " ")
        text = text.replace("\n    ]", " ]")
        text = text + "\n"
        try:
            geo_path.write_text(text, encoding="utf8")
        except IOError:
            raise MocodoError(34, _('Unable to save geometry file "{filename}".').format(filename=geo_path)) # fmt: skip
        return geo


    def calculate_size(self, style):

        def increase_margins_in_presence_of_clusters():
            if not self.associations: # relational diagram or MCD without associations
                return
            factor = 1 + max(a.peg_count for a in self.associations.values())
            style["margin"] *= factor
            style["card_margin"] *= factor

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
            for constraint in self.constraints:
                constraint.calculate_size(style, self.get_font_metrics)
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
        for constraint in self.constraints:
            constraint.register_center(geo)
        result = []
        for element in self.entities.values():
            result.extend(element.description(style, geo))
        for element in self.associations.values():
            result.extend(element.description(style, geo))
        for element in self.inheritances:
            result.extend(element.description(style, geo))
        for element in self.diagram_links:
            result.extend(element.description(style, geo))
        for element in self.constraints:
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
            if entity.is_invisible:
                continue
            (ie, je) = coordinates[entity]
            segments["i", ie].append((je, je, entity, entity))
            segments["j", je].append((ie, ie, entity, entity))
        for association in self.associations.values():
            if association.is_invisible:
                continue
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
                if e1.bid == e2.bid and a1.bid == a2.bid: # reflexive association
                    continue
                if l2 < r1:
                    result.append((e1.bid, a1.bid, e2.bid, a2.bid))
        return result

if __name__=="__main__":
    from .argument_parser import parsed_arguments
    source = """
        CLIENT: Réf. client, Nom, Prénom, Adresse
        PASSER, 0N CLIENT, 11 COMMANDE
        COMMANDE: Num commande, Date, Montant
        INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
        PRODUIT: Réf. produit, Libellé, Prix unitaire
    """.replace("  ", "").split("\n")
    params = parsed_arguments()
    mcd = Mcd(source, **params)
    print(mcd.get_horizontally_flipped_clauses())
