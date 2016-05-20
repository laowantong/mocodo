#!/usr/bin/env python
# encoding: utf-8

import os
from file_helpers import read_contents

def main(mcd, common):
    params = common.params
    style = common.load_style()
    style["transparent_color"] = None
    mcd.calculate_size(style)
    result = ["# %s\n" % common.timestamp()]
    result.append("from __future__ import division\nfrom math import hypot\n")
    result.extend(common.process_geometry(mcd, style))
    result.append("""\nfor c in colors: colors[c] = (color(*[int((colors[c]+"FF")[i:i+2],16)/255.0 for i in range(1,9,2)]) if colors[c] else None)""")
    for name in ["card_max_width", "card_max_height", "card_margin", "arrow_width", "arrow_half_height", "arrow_axis", "curvature_ratio", "curvature_gap", "card_underline_skip_height"]:
        result.append("%s = %s" % (name, style[name]))
    result.append("")
    result.append(read_contents(os.path.join(params["script_directory"], "goodies.py")))
    result.append("")
    result.append(read_contents(os.path.join(params["script_directory"], "nodebox_goodies.py")))
    result.append("\nsize(width,height)")
    result.append("autoclosepath(False)")
    result.append("background(colors['background_color'])")
    commands = {
        "stroke_depth": "strokewidth(%(stroke_depth)s)",
        "color": """fill(colors["%(color)s"])""",
        "stroke_color": """stroke(colors["%(stroke_color)s"])""",
        "rect": "rect(%(x)s,%(y)s,%(w)s,%(h)s)",
        "circle": "oval(%(cx)s-%(r)s,%(cy)s-%(r)s,2*%(r)s,2*%(r)s)",
        "lower_round_rect": "lower_round_rect(%(x)s,%(y)s,%(w)s,%(h)s,%(radius)s)",
        "upper_round_rect": "upper_round_rect(%(x)s,%(y)s,%(w)s,%(h)s,%(radius)s)",
        "round_rect": "round_rect(%(x)s,%(y)s,%(w)s,%(h)s,%(radius)s)",
        "line": "line(%(x0)s,%(y0)s,%(x1)s,%(y1)s)",
        "dash_line": "dash_line(%(x0)s,%(x1)s,%(y)s,%(dash_width)s)",
        "text": """fill(colors["%(text_color)s"])\nfont("%(family)s",%(size)s)\ntext(u"%(text)s",%(x)s,%(y)s)""",
        "straight_leg": """(card_pos,arrow_pos)=straight_leg(%(ex)s,%(ey)s,%(ew)s,%(eh)s,%(ax)s,%(ay)s,%(aw)s,%(ah)s)""",
        "straight_card": """(tx,ty)=card_pos(%(cw)s+2*card_margin,%(ch)s+2*card_margin,k[u"%(leg_identifier)s"])\nfill(colors["%(text_color)s"])\nfont("%(family)s",%(size)s)\ntext(u"%(text)s",tx+card_margin,ty-card_margin)""",
        "note_straight_card": """(tx,ty)=card_pos(%(cw)s+2*card_margin,%(ch)s+2*card_margin,k[u"%(leg_identifier)s"])\nfill(colors["%(text_color)s"])\nfont("%(family)s",%(size)s)\ntext(u"%(text)s",tx+card_margin,ty-card_margin)""",
        "straight_arrow": """arrow(*arrow_pos("%(direction)s",t[u"%(leg_identifier)s"]))""",
        "curved_leg": """(card_pos,arrow_pos)=curved_leg(%(ex)s,%(ey)s,%(ew)s,%(eh)s,%(ax)s,%(ay)s,%(aw)s,%(ah)s,%(spin)s)""",
        "curved_card": """(tx,ty)=card_pos(%(cw)s+2*card_margin,%(ch)s+2*card_margin,k[u"%(leg_identifier)s"])\nfill(colors["%(text_color)s"])\nfont("%(family)s",%(size)s)\ntext(u"%(text)s",tx+card_margin,ty-card_margin)""",
        "note_curved_card": """(tx,ty)=card_pos(%(cw)s+2*card_margin,%(ch)s+2*card_margin,k[u"%(leg_identifier)s"])\nfill(colors["%(text_color)s"])\nfont("%(family)s",%(size)s)\ntext(u"%(text)s",tx+card_margin,ty-card_margin)""",
        "curved_arrow": """arrow(*arrow_pos("%(direction)s",t[u"%(leg_identifier)s"]))""",
        "card_underline": """line(tx+card_margin,ty-card_margin-card_underline_skip_height,tx+%(w)s,ty-card_margin-card_underline_skip_height)""",
    }
    for d in mcd.description():
        try:
            result.append(commands[d["key"]] % d)
        except KeyError:
            if d["key"] == "env":
                result.append("(%s) = (%s)" % (",".join(zip(*d["env"])[0]), ",".join(zip(*d["env"])[1])))
        except TypeError:
            result.append("\n# %s" % d)
    common.dump_output_file("\n".join(result))

if __name__ == "__main__":
    from argument_parser import parsed_arguments
    from mcd import Mcd
    from common import Common
    clauses = u"""
        CLIENT: Réf. client, Nom, Prénom, Adresse
        PASSER, 0N CLIENT, 11 COMMANDE
        COMMANDE: Num commande, Date, Montant
        INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
        PRODUIT: Réf. produit, Libellé, Prix unitaire
    """.replace("  ", "").split("\n")
    params = parsed_arguments()
    params["image_format"] = "nodebox"
    common = Common(params)
    mcd = Mcd(clauses, params)
    main(mcd, common)