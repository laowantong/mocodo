from pathlib import Path
import random
import re
import string

from .mocodo_error import MocodoError

try:
    from cairosvg import svg2png, svg2pdf
except:
    def svg2png(**kargs):
        raise MocodoError(13, _("PNG and PDF generation requires cairosvg to be installed")) # fmt: skip
    svg2pdf = svg2png

from .common import safe_print_for_PHP

ID_CHARACTERS = string.ascii_letters + string.digits

def main(mcd, common):
    style = common.load_style()
    mcd_uid = ''.join(random.choice(ID_CHARACTERS) for _ in range(8))
    mcd.calculate_size(style)
    geo = common.calculate_or_retrieve_geo(mcd, reuse_geo=common.params["reuse_geo"])
    description = [
        (
            "preamble",
            {
                "width": geo["width"],
                "height": geo["height"],
                "total_height": geo["height"] + (mcd.page_count > 1 and style["note_overlay_height"]),
            }
        ),
        (
            "background",
            {
                "width": geo["width"],
                "height": geo["height"],
                "background_color": style["background_color"],
            }
        ),
        *mcd.description(style, geo),
    ]
    has_note_card = False
    tabs = 0
    categories = {"": [], "Association": [], "Entity": [], "Link": [], "Notes": [], "Pager": []}
    category = ""
    for (key, mapping) in description:
        mapping["mcd_uid"] = mcd_uid
        has_note_card |= key.endswith("with_note")
        if key == "comment":
            category = mapping["text"].partition(" ")[0]
        for (k, v) in mapping.items():
            if isinstance(v, float):
                mapping[k] = int(v) if v.is_integer() else round(v, 2)
            elif isinstance(v, str):
                mapping[k] = html_escape(v)
            elif v is None:
                mapping[k] = "none"
        # print(key, mapping, end="\n")
        tabs -= (key == "end")
        categories[category].append('\t' * tabs + svg_elements[key].format_map(mapping))
        tabs += key.startswith("begin")
    if common.params["hide_notes"] or not has_note_card:
        del categories["Notes"]
    text = "\n".join(sum(categories.values(), [])) + "\n</svg>"
    path = Path(f"{common.params['output_name']}.svg")
    path.write_text(text, encoding="utf8")
    safe_print_for_PHP(common.output_success_message(path))
    if categories.pop("Notes", []) + categories.pop("Pager"): # don't use or to avoid short-circuit
        text = "\n".join(sum(categories.values(), [])) + "\n</svg>"
        text = re.sub(
            r"(?m)^<\?xml .+\n<svg .+",
            svg_elements["preamble"].format(total_height=geo["height"], **geo),
            text
        )
        text = re.sub(r"(?m)^<g class.+", "<g>", text)
        text = re.sub(r' (onmouseover|onmouseout|style|id)=".+?"', "", text)
        path = Path(f"{common.params['output_name']}_static.svg")
        path.write_text(text, encoding="utf8")
        safe_print_for_PHP(common.output_success_message(path))
    svg = bytes(text, "utf-8")
    for (format, function) in (("png", svg2png), ("pdf", svg2pdf)):
        if common.params[format]:
            path = Path(f"{common.params['output_name']}.{format}")
            function(bytestring=svg, write_to=str(path))
            safe_print_for_PHP(common.output_success_message(path))


def html_escape(
    text,
    table={
        "&": "&amp;",
        ">": "&gt;",
        "<": "&lt;",
        '"': "&quot;",
        "'": "’",  # neither &#39; nor &apos; make the job in notes
}):
    return "".join(table.get(c, c) for c in text)

svg_elements = {
    "preamble":         """<?xml version="1.0" encoding="utf-8"?>\n<svg width="{width}" height="{total_height}" viewBox="0 0 {width} {total_height}" xmlns="http://www.w3.org/2000/svg">""",
    "background":       """<rect id="frame" x="0" y="0" width="{width}" height="{height}" fill="{background_color}" stroke="none" stroke-width="0"/>""",
    "comment":          """\n<!-- {text} -->""",
    "begin_component":  """<g class="page_{page}_{mcd_uid} diagram_page" visibility="{visibility}">""",
    "begin_group":      """<g>""",
    "end":              """</g>""",
    "text":             """<text x="{x}" y="{y}" fill="{text_color}" font-family="{family}" font-size="{size}">{text}</text>""",
    "text_with_note":   """<text x="{x}" y="{y}" fill="{text_color}" font-family="{family}" font-size="{size}" onmouseover="show(evt,'{note}')" onmouseout="hide(evt)" style="cursor: pointer;">{text}</text>""",
    "line":             """<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "dash_line":        """<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{stroke_color}" stroke-width="{stroke_depth}" stroke-dasharray="{dash_width}"/>""",
    "rect":             """<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_depth}" opacity="{opacity}"/>""",
    "dash_rect":        """<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_depth}" stroke-dasharray="{dash_width}"/>""",
    "polygon":          """<polygon points="{points}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_depth}" opacity="{opacity}"/>""",
    "dot_polygon":      """<polygon points="{points}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_depth}" stroke-dasharray="0,{dash_gap}" stroke-linecap="round"/>""",
    "circle":           """<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{stroke_color}" stroke-width="{stroke_depth}" fill="{color}"/>""",
    "pager_dot":        """<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" id="pager_dot_{page}_{mcd_uid}" class="pager_dot" stroke-width="0" onclick="switch_page_visibility(evt,{page})" style="cursor: pointer;"/>""",
    "triangle":         """<polygon points="{x1} {y1} {x2} {y2} {x3} {y3}" stroke="{stroke_color}" stroke-width="{stroke_depth}" fill="{color}"/>""",
    "arrow":            """<polygon points="{x0} {y0} {x1} {y1} {x2} {y2} {x3} {y3}" fill="{stroke_color}" stroke-width="0"/>""",
    "curve":            """<path d="M{x0} {y0} C{x1} {y1} {x2} {y2} {x3} {y3}" fill="none" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "round_rect":       """<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" rx="{radius}" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "upper_round_rect": """<path d="M{x0} {y0} a{r} {r} 90 0 1 {r} {r} V{y1} h-{w} V{y2} a{r} {r} 90 0 1 {r} -{r}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "lower_round_rect": """<path d="M{x0} {y0} v{y1} a{r} {r} 90 0 1 -{r} {r} H{x1} a{r} {r} 90 0 1 -{r} -{r} V{y0} H{w}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "notes":            """<script type="text/ecmascript">
                            <![CDATA[
                            	function show(evt, text) {{
                            		var pos = (evt.target.getAttribute("y") < {height_threshold}) ? "bottom" : "top";
                            		var note = document.getElementById(pos + "_note_{mcd_uid}");
                            		note.textContent = text;
                            		note.setAttributeNS(null, "visibility", "visible");
                            		document.getElementById(pos + "_overlay_{mcd_uid}").setAttributeNS(null, "visibility", "visible");
                            	}}
                            	function hide(evt) {{
                            		document.getElementById("top_note_{mcd_uid}").setAttributeNS(null, "visibility", "hidden");
                            		document.getElementById("top_overlay_{mcd_uid}").setAttributeNS(null, "visibility", "hidden");
                            		document.getElementById("bottom_note_{mcd_uid}").setAttributeNS(null, "visibility", "hidden");
                            		document.getElementById("bottom_overlay_{mcd_uid}").setAttributeNS(null, "visibility", "hidden");
                            	}}
                            ]]>
                            </script>
                            <rect id="top_overlay_{mcd_uid}" x="0" y="0" width="100%" height="{overlay_height}" fill="{color}" stroke-width="0" opacity="{opacity}" visibility="hidden"/>
                            <text id="top_note_{mcd_uid}" text-anchor="middle" x="{x}" y="{y_top}" fill="{text_color}" font-family="{font_family}" font-size="{font_size}" visibility="hidden"></text>
                            <rect id="bottom_overlay_{mcd_uid}" x="0" y="{y}" width="100%" height="{overlay_height}" fill="{color}" stroke-width="0" opacity="{opacity}" visibility="hidden"/>
                            <text id="bottom_note_{mcd_uid}" text-anchor="middle" x="{x}" y="{y_bottom}" fill="{text_color}" font-family="{font_family}" font-size="{font_size}" visibility="hidden"></text>""".replace("    ", ""),
    "pager":            """<script type="text/ecmascript">
                            <![CDATA[
                            	function switch_page_visibility(evt, page) {{
                            		for (var i = 0; i < {page_count}; i++) {{
                            			components = document.getElementsByClassName(`page_${{i}}_{mcd_uid}`);
                            			for (var j = 0; j < components.length; j++) {{
                            				components[j].setAttributeNS(null, "visibility", i <= page ? "visible" : "hidden");
                            			}};
                            			dot = document.getElementById(`pager_dot_${{i}}_{mcd_uid}`);
                            			dot.setAttributeNS(null, "fill", i <= page ? "gray" : "lightgray");
                            		}}
                            	}}
                            ]]>
                            </script>""".replace("    ", ""),
}


if __name__ == "__main__":
    from .argument_parser import parsed_arguments
    from .common import Common
    from .mcd import Mcd

    clauses = """
        CLIENT: Réf. client, Nom, Prénom, Adresse
        PASSER, 0N CLIENT, 11 COMMANDE
        COMMANDE: Num commande, Date, Montant
        INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
        PRODUIT: Réf. produit, Libellé, Prix unitaire
    """
    params = parsed_arguments()
    common = Common(params)
    mcd = Mcd(clauses, **params)
    main(mcd, common)
