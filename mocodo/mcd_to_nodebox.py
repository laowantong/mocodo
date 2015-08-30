#!/usr/bin/env python
# encoding: utf-8

import os

def main(mcd, common):
    params = common.params
    style = common.load_style()
    style["transparent_color"] = None
    mcd.calculate_size(style)
    result = ["# %s\n" % common.timestamp()]
    result.extend(common.process_geometry(mcd, style))
    result.append("""\nfor c in colors: colors[c] = (color(*[int((colors[c]+"FF")[i:i+2],16)/255.0 for i in range(1,9,2)]) if colors[c] else None)""")
    result.append("card_max_width = %(card_max_width)s\ncard_max_height = %(card_max_height)s\ncard_margin = %(card_margin)s\narrow_width = %(arrow_width)s\narrow_half_height = %(arrow_half_height)s\narrow_axis = %(arrow_axis)s" % style)
    result.append(open(os.path.join(params["script_directory"], "goodies.py")).read())
    result.append(open(os.path.join(params["script_directory"], "nodebox_goodies.py")).read())
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
        "arrow": """arrow(%(x)s,%(y)s,%(a)s,%(b)s)""",
        "line_arrow": """line_arrow(%(x0)s,%(y0)s,%(x1)s,%(y1)s,t[u"%(leg_identifier)s"])""",
        "dash_line": "dash_line(%(x0)s,%(x1)s,%(y)s,%(dash_width)s)",
        "curve": "curve(%(x0)s,%(y0)s,%(x1)s,%(y1)s,%(x2)s,%(y2)s,%(x3)s,%(y3)s)",
        "curve_arrow": """curve_arrow(%(x0)s,%(y0)s,%(x1)s,%(y1)s,%(x2)s,%(y2)s,%(x3)s,%(y3)s,1-t[u"%(leg_identifier)s"])""",
        "text": """fill(colors["%(text_color)s"]);font("%(family)s",%(size)s);text(u"%(text)s",%(x)s,%(y)s)""",
        "card": """(tx,ty)=card_pos(%(ex)s,%(ey)s,%(ew)s,%(eh)s,%(ax)s,%(ay)s,k[u"%(leg_identifier)s"]);fill(colors["%(text_color)s"]);font("%(family)s",%(size)s);text(u"%(text)s",tx,ty)""",
        "annotated_card": """(tx,ty)=card_pos(%(ex)s,%(ey)s,%(ew)s,%(eh)s,%(ax)s,%(ay)s,k[u"%(leg_identifier)s"]);fill(colors["%(text_color)s"]);font("%(family)s",%(size)s);text(u"%(text)s",tx,ty)""",
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