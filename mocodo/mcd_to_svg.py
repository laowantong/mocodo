from pathlib import Path

from .common import safe_print_for_PHP

def main(mcd, common):
    style = common.load_style()
    for (k, v) in style.items():
        if k.endswith("_color") and v is None:
            style[k] = "none"
    mcd.calculate_size(style)
    geo = common.calculate_or_retrieve_geo(mcd)
    has_note_card = False
    tabs = 0
    layers = {"Association": [], "Entity": [], "Link": [], "Annotations": []}
    for (key, mapping) in mcd.description(style, geo):
        has_note_card |= key.endswith("with_note")
        if key == "comment":
            layer = mapping["comment"].partition(" ")[0]
        for k in mapping:
            if isinstance(mapping[k], float):
                mapping[k] = round(mapping[k], 2)
            elif isinstance(mapping[k], str):
                mapping[k] = html_escape(mapping[k])
        tabs -= (key == "end")
        # print(key, mapping, end="\n")
        layers[layer].append('\t' * tabs + svg_elements[key].format_map(mapping))
        tabs += (key == "begin")
    if common.params["hide_annotations"] or not has_note_card:
        del layers["Annotations"]
    mapping = {
        "width": geo["width"],
        "height": geo["height"],
        "timestamp": common.timestamp(),
        "shapes": "\n".join(sum(layers.values(), [])),
        "background_color": style["background_color"] or "none",
    }
    text = template.format_map(mapping)
    path = Path(f"{common.params['output_name']}.svg")
    path.write_text(text)
    safe_print_for_PHP(common.output_success_message(path))

def html_escape(
    text,
    table={
        "&": "&amp;",
        ">": "&gt;",
        "<": "&lt;",
        '"': "&quot;",
        "'": "’",  # neither &#39; nor &apos; make the job in annotations
}):
    return "".join(table.get(c, c) for c in text)

template = """\
<svg version="1.1" baseProfile="full" width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
<desc>{timestamp}</desc>
<rect id="frame" x="0" y="0" width="{width}" height="{height}" fill="{background_color}" stroke="none" stroke-width="0"/>
{shapes}
</svg>\
"""

svg_elements = {
    "comment":                 """\n<!-- {comment} -->""",
    "begin":                   """<g id="{id}">""",
    "end":                     """</g>""",
    "text":                    """<text x="{x}" y="{y}" fill="{text_color}" font-family="{family}" font-size="{size}">{text}</text>""",
    "text_with_note":          """<text x="{x}" y="{y}" fill="{text_color}" font-family="{family}" font-size="{size}" onmouseover="show(evt,'{annotation}')" onmouseout="hide(evt)" style="cursor: pointer;">{text}</text>""",
    "line":                    """<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "dash_line":               """<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" style="fill:none;stroke:{stroke_color};stroke-width:{stroke_depth};stroke-dasharray:{dash_width};"/>""",
    "rect":                    """<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "circle":                  """<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{stroke_color}" stroke-width="{stroke_depth}" fill="{color}"/>""",
    "triangle":                """<polygon points="{x1},{y1} {x2},{y2} {x3},{y3}" stroke="{stroke_color}" stroke-width="{stroke_depth}" fill="{color}"/>""",
    "arrow":                   """<path d="M{x0} {y0} L{x1} {y1} L{x2} {y2} L{x3} {y3} Z" fill="{stroke_color}" stroke-width="0"/>""",
    "curve":                   """<path d="M{x0} {y0} C {x1} {y1} {x2} {y2} {x3} {y3}" fill="none" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "round_rect":              """<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" rx="{radius}" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "upper_round_rect":        """<path d="M{x0} {y0} a {r} {r} 90 0 1 {r} {r} V {y1} h -{w} V {y2} a {r} {r} 90 0 1 {r} -{r}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "lower_round_rect":        """<path d="M{x0} {y0} v {y1} a {r} {r} 90 0 1 -{r} {r} H {x1} a {r} {r} 90 0 1 -{r} -{r} V {y0} H {w}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_depth}"/>""",
    "annotations":             """<script type="text/ecmascript">
                                <![CDATA[
                                	function show(evt, text) {{
                                		var pos = (evt.target.getAttribute("y") < {height_threshold}) ? "bottom" : "top";
                                		var annotation = document.getElementById(pos + "_annotation_{salt}");
                                		annotation.textContent = text;
                                		annotation.setAttributeNS(null, "visibility", "visible");
                                		document.getElementById(pos + "_overlay_{salt}").setAttributeNS(null, "visibility", "visible");
                                	}}
                                	function hide(evt) {{
                                		document.getElementById("top_annotation_{salt}").setAttributeNS(null, "visibility", "hidden");
                                		document.getElementById("top_overlay_{salt}").setAttributeNS(null, "visibility", "hidden");
                                		document.getElementById("bottom_annotation_{salt}").setAttributeNS(null, "visibility", "hidden");
                                		document.getElementById("bottom_overlay_{salt}").setAttributeNS(null, "visibility", "hidden");
                                	}}
                                ]]>
                                </script>
                                <rect id="top_overlay_{salt}" x="0" y="0" width="100%" height="{overlay_height}" fill="{color}" stroke-width="0" opacity="{opacity}" visibility="hidden"/>
                                <text id="top_annotation_{salt}" text-anchor="middle" x="{x}" y="{y_top}" fill="{text_color}" font-family="{font_family}" font-size="{font_size}" visibility="hidden"></text>
                                <rect id="bottom_overlay_{salt}" x="0" y="{y}" width="100%" height="{overlay_height}" fill="{color}" stroke-width="0" opacity="{opacity}" visibility="hidden"/>
                                <text id="bottom_annotation_{salt}" text-anchor="middle" x="{x}" y="{y_bottom}" fill="{text_color}" font-family="{font_family}" font-size="{font_size}" visibility="hidden"></text>""".replace("    ", ""),
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
    """.replace(
        "  ", ""
    ).split(
        "\n"
    )
    params = parsed_arguments()
    common = Common(params)
    mcd = Mcd(clauses, **params)
    main(mcd, common)
