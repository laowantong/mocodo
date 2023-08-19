import re

def create_name_to_index():
    """
    Return a function that maps names to unique numbers.
    Used to generate short "names" for Graphviz nodes.
    """
    cache = {}
    def name_to_index(name):
        if name not in cache:
            cache[name] = len(cache) + 1
        return cache[name]
    return name_to_index


def minify_graphviz(text):
    # Suppress comments
    text = re.sub(r"(?m)^ *//.*$", "", text)
    # Suppress empty lines
    text = re.sub(r"(?m)^\s*\n", "", text)
    # Suppress leading spaces
    text = re.sub(r"(?m)^\s+", "", text)
    # Suppress newline before delimiters
    text = re.sub(r"\n([]<>])", r"\1", text)
    # Factorize edges
    while True:
        (text, n) = re.subn(r"(?m)(\d+) (-[->]) ([^[\n]+)\n\1 -- ", r"\1 \2 \3,", text)
        if n == 0:
            break
    # Suppress spaces around arrows
    text = re.sub(r"(?m)(\d+) (-[->]) ", r"\1\2", text)
    # Suppress spaces before opening brackets
    text = re.sub(r"(?m)^(edge|node) *\[", r"\1[", text)
    # Suppress newlines after opening brackets
    text = re.sub(r"\[\n", r"[", text)
    # Supress spaces after \d+ -> \d+
    text = re.sub(r"(?m)^([\d>-]+) +", r"\1", text)
    return text


NODE_OPTIONS_TEMPLATE = """
      shape=none
      fontcolor="{cell_font_color}"
      fontsize={cell_font_size}
      fontname="Helvetica"
""" # This constant is public

TABLE_TEMPLATE = """<table
        border="0"
        cellborder="1"
        cellspacing="0"
        bgcolor="{cell_bg_color}"
        color="{stroke_color}"
        cellpadding="4"
    >
        TABLE_CONTENT_PLACEHOLDER
    </table>
"""

HEADER_TEMPLATE = """<tr>
            <td bgcolor="{header_bg_color}" colspan="COL_COUNT_PLACEHOLDER">
                <font
                    color="{header_font_color}"
                    point-size="{header_font_size}"
                >HEADER_TEXT_PLACEHOLDER</font>
            </td>
        </tr>
"""

SPECIAL_FONT_TEMPLATE = """<font face="Courier">TEXT_PLACEHOLDER</font>"""

ROW_TEMPLATE = """        <tr>{cells}</tr>"""


def row_format_to_td_templates(
    row_format, # a LaTeX-like table format string (e.g. "|l|c|r|")
    ALIGN={
        "l": ' align="left"',
        "c": "",
        "r": ' align="right"',
    },
):
    """
    Return a list of td element templates from a LaTeX-table-like format string.
    NB: an uppercase letter means "use the special font".
    """
    acc = []
    row_format = f" {row_format} "
    for (i, symbol) in enumerate(row_format[1:-1], 1):
        text = "TEXT_PLACEHOLDER"
        if symbol.isupper():
            text = SPECIAL_FONT_TEMPLATE
            symbol = symbol.lower()
        if symbol in ALIGN:
            align = ALIGN[symbol]
            sides = ' sides="TB'
            if row_format[i - 1] == "|":
                sides += "L"
            if row_format[i + 1] == "|":
                sides += "R"
            sides += '"'
            if sides == ' sides="TBLR"':
                sides = ""
            acc.append(f"<td{align}{sides}>{text}</td>")
    return acc

def table_as_label(header_text, rows, row_format, style):
    """Return a table has an HTML-like Graphviz label."""
    header = HEADER_TEMPLATE.format(**style)
    header = header.replace("HEADER_TEXT_PLACEHOLDER", header_text)
    td_templates = row_format_to_td_templates(row_format)
    header = header.replace("COL_COUNT_PLACEHOLDER", str(len(td_templates)))
    trs = []
    for row in rows:
        cells = []
        for (text, td_template) in zip(row, td_templates):
            cells.append(td_template.replace("TEXT_PLACEHOLDER", text))
        trs.append(ROW_TEMPLATE.format(cells="".join(cells)))
    trs = "\n".join(trs)
    table = TABLE_TEMPLATE.format(**style)
    table = table.replace("TABLE_CONTENT_PLACEHOLDER", header + trs)
    return table

if __name__ == "__main__":
    header_text = "CLIENT"
    rows = [
        ["PK", "id. client", "varchar(8)"],
        ["", "nom", "varchar(30)"],
        ["", "prénom", "varchar(30)"],
        ["", "âge", "int"],
    ]
    row_format = "|cl|L|"
    style = {
        "cell_bg_color": "#c0d4ff",
        "stroke_color": "#578dff",
        "header_bg_color": "#97b8ff",
        "header_font_color": "#131114",
        "header_font_size": 14,
        "cell_font_color": "#3e3c42",
        "cell_font_size": 12,
    }
    node_options = NODE_OPTIONS_TEMPLATE.format(**style)
    table = table_as_label(header_text, rows, row_format, style)
    print("digraph {")
    print(f"node [{node_options}]")
    print(f'1 [label=<{table}>]')
    print("}")
