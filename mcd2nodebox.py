#!/usr/bin/python2.6
# encoding: utf-8

from main.mcd import *
from main.common import *

def main(params):
	common = Common(params)
	style = common.loadStyle()
	style[u"transparentColor"] = u"#00000000"
	mcd = Mcd(common.loadInputFile(),params)
	mcd.calculateSize(style)
	result = ["# %s\n" % common.timeStamp()]
	result.append("(width,height) = (%s,%s)" % (mcd.w,mcd.h))
	result.extend(common.prettyDict("cx",[(box.name,box.x+box.w/2) for row in mcd.ordering for box in row]))
	result.extend(common.prettyDict("cy",[(box.name,box.y+box.h/2) for row in mcd.ordering for box in row]))
	result.extend(common.prettyDict("k",[(leg.identifier(),leg.value()) for row in mcd.ordering for box in row if box.__class__ is Association for leg in box.legs]))
	result.extend(common.prettyDict("t",[(leg.identifier(),0.5) for row in mcd.ordering for box in row if box.__class__ is Association for leg in box.legs if leg.arrow]))
	result.extend(common.prettyDict("colors ",[((c,style[c]) if style[c] else (c,None)) for c in sorted(style.keys()) if c.endswith("Color")]))
	result.append("""\nfor c in colors: colors[c] = (color(*[int((colors[c]+"FF")[i:i+2],16)/255.0 for i in range(1,9,2)]) if colors[c] else None)""")
	result.append("cardMaxWidth = %(cardMaxWidth)s\ncardMaxHeight = %(cardMaxHeight)s\ncardMargin = %(cardMargin)s\narrowWidth = %(arrowWidth)s\narrowHalfHeight = %(arrowHalfHeight)s\narrowAxis = %(arrowAxis)s" % style)
	result.append(open("main/goodies.py").read())
	result.append(open("main/nodeboxgoodies.py").read())
	result.append("\nsize(width,height)")
	result.append("autoclosepath(False)")
	result.append("background(colors['backgroundColor'])")
	commands = {
		"strokeDepth": "strokewidth(%(strokeDepth)s)",
		"color": """fill(colors["%(color)s"])""",
		"strokeColor": """stroke(colors["%(strokeColor)s"])""",
		"rect": "rect(%(x)s,%(y)s,%(w)s,%(h)s)",
		"circle": "oval(%(cx)s-%(r)s,%(cy)s-%(r)s,2*%(r)s,2*%(r)s)",
		"lowerRoundRect": "lowerRoundRect(%(x)s,%(y)s,%(w)s,%(h)s,%(radius)s)",
		"upperRoundRect": "upperRoundRect(%(x)s,%(y)s,%(w)s,%(h)s,%(radius)s)",
		"roundRect": "roundRect(%(x)s,%(y)s,%(w)s,%(h)s,%(radius)s)",
		"line": "line(%(x0)s,%(y0)s,%(x1)s,%(y1)s)",
		"lineArrow": """lineArrow(%(x0)s,%(y0)s,%(x1)s,%(y1)s,t[u"%(legIdentifier)s"])""",
		"dashLine": "dashLine(%(x0)s,%(x1)s,%(y)s,%(dashWidth)s)",
		"curve": "curve(%(x0)s,%(y0)s,%(x1)s,%(y1)s,%(x2)s,%(y2)s,%(x3)s,%(y3)s)",
		"curveArrow": """curveArrow(%(x0)s,%(y0)s,%(x1)s,%(y1)s,%(x2)s,%(y2)s,%(x3)s,%(y3)s,1-t[u"%(legIdentifier)s"])""",
		"text": """fill(colors["%(textColor)s"]);font("%(family)s",%(size)s);text(u"%(text)s",%(x)s,%(y)s)""",
		"card": """(tx,ty)=cardPos(%(ex)s,%(ey)s,%(ew)s,%(eh)s,%(ax)s,%(ay)s,k[u"%(legIdentifier)s"]);fill(colors["%(textColor)s"]);font("%(family)s",%(size)s);text(u"%(text)s",tx,ty)""",
	}
	for d in mcd.description():
		try:
			result.append(commands[d["key"]] % d)
		except KeyError:
			if d["key"] == "env":
				result.append("(%s) = (%s)" % (",".join(zip(*d["env"])[0]),",".join(zip(*d["env"])[1])))
		except TypeError:
			result.append("\n# %s" % d)
	common.dumpOutputFile("\n".join(result))
	common.dumpMldFiles(mcd)
	

if __name__=="__main__":
	params = json.loads(open("default.json").read())
	params["output"] = params["output"].replace(".svg",".py")
	main(params)
