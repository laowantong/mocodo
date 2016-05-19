def round_rect(x, y, w, h, r):
    beginpath()
    moveto(x + w - r, y)
    curveto(x + w, y, x + w, y + r, x + w, y + r)
    lineto(x + w, y + h - r)
    curveto(x + w, y + h - r, x + w, y + h, x + w - r, y + h)
    lineto(x + r, y + h)
    curveto(x, y + h, x, y + h - r, x, y + h - r)
    lineto(x, y + r)
    curveto(x, y + r, x, y, x + r, y)
    lineto(x + w - r, y)
    endpath()

def upper_round_rect(x, y, w, h, r):
    beginpath()
    moveto(x + w - r, y)
    curveto(x + w, y, x + w, y + r, x + w, y + r)
    lineto(x + w, y + h)
    lineto(x, y + h)
    lineto(x, y + r)
    curveto(x, y + r, x, y, x + r, y)
    lineto(x + w - r, y)
    endpath()

def lower_round_rect(x, y, w, h, r):
    beginpath()
    moveto(x + w, y)
    lineto(x + w, y + h - r)
    curveto(x + w, y + h - r, x + w, y + h, x + w - r, y + h)
    lineto(x + r, y + h)
    curveto(x, y + h, x, y + h - r, x, y + h - r)
    lineto(x, y)
    lineto(x + w, y)
    endpath()

def dash_line(x0, x1, y, w):
    nofill()
    beginpath(x0, y)
    for i in range(int(x0 + 0.5), int(x1 + 0.5), int(2 * w + 0.5)):
        lineto(min(i + w, x1), y)
        moveto(i + 2 * w, y)
    endpath()

def curve(x0, y0, x1, y1, x2, y2, x3, y3):
    nofill()
    beginpath(x0, y0)
    curveto(x1, y1, x2, y2, x3, y3)
    endpath()

def arrow(x, y, a, b):
    c = hypot(a, b)
    (cos, sin) = (a / c, b / c)
    beginpath(x, y)
    lineto(x + arrow_width * cos - arrow_half_height * sin, y - arrow_half_height * cos - arrow_width * sin)
    lineto(x + arrow_axis * cos, y - arrow_axis * sin)
    lineto(x + arrow_width * cos + arrow_half_height * sin, y + arrow_half_height * cos - arrow_width * sin)
    lineto(x, y)
    endpath()
