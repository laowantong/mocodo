#!/usr/bin/env python
# encoding: utf-8

import fontMetrics

import sys

class Leg:
	
	def __init__(self,association,card,entityName):
		self.association = association
		self.mayIdentify = not entityName.startswith("/")
		if not self.mayIdentify:
			entityName = entityName[1:]
		self.entityName = entityName
		self.arrow = (card[-1] if card[-1] in "<>" else "")
		self.label = (card[2:] if card[2:] not in "<>" else "")
		self.cards = card
	
	def calculateSize(self,style):
		font = fontMetrics.FontMetrics(style["cardFont"])
		self.h = font.getPixelHeight()
		self.style = style
	
	def setEntity(self,entities):
		try:
			self.entity = entities[self.entityName]
		except KeyError:
			sys.stderr.write(u"Warning: association %s linked to an unknown entity %s!\n" % (repr(self.association.name),repr(self.entityName)))
	
	def setCardSep(self,cardSep):
		self.cardinalities = ("" if self.cards.startswith("XX") else self.cards[0] + cardSep + self.cards[1])
	

class StraightLeg(Leg):
	
	def __init__(self,association,card,entityName):
		Leg.__init__(self,association,card,entityName)
		self.num = 0
	
	def description(self):
		return [
			{
				"key": u"strokeDepth",
				"strokeDepth": self.style["legStrokeDepth"],
			},
			{
				"key": u"env",
				"env": [("ex","""cx[u"%s"]"""%self.entity.name),("ey","""cy[u"%s"]"""%self.entity.name)],
			},
			{
				"key": u"strokeColor",
				"strokeColor": "legStrokeColor",
			},
			{
				"key": u"line",
				"x0": "ex",
				"y0": "ey",
				"x1": "x",
				"y1": "y",
			},
			{
				"key": u"card",
				"text": self.cardinalities,
				"textColor": "cardTextColor",
				"ex": "ex",
				"ey": "%s+ey" % (self.style["cardTextHeightRatio"] * self.h),
				"ew": self.entity.w / 2,
				"eh": self.entity.h / 2,
				"ax": "x",
				"ay": "%s+y" % (self.style["cardTextHeightRatio"] * self.h),
				"legIdentifier": "%s,%s" % (self.association.name,self.entityName),
				"family": self.style["cardFont"]["family"],
				"size": self.style["cardFont"]["size"],
			},
		] + {
			">": [
						{
							"key": u"color",
							"color": "legStrokeColor",
						},
						{
							"key": u"strokeDepth",
							"strokeDepth": 0,
						},
						{
							"key": u"lineArrow",
							"x0": "ex",
							"y0": "ey",
							"x1": "x",
							"y1": "y",
							"legIdentifier": "%s,%s" % (self.association.name,self.entityName),
						}
				],
			"<": [
						{
							"key": u"color",
							"color": "legStrokeColor",
						},
						{
							"key": u"strokeDepth",
							"strokeDepth": 0,
						},
						{
							"key": u"lineArrow",
							"x0": "x",
							"y0": "y",
							"x1": "ex",
							"y1": "ey",
							"legIdentifier": "%s,%s" % (self.association.name,self.entityName),
						}
				],
			"": []
		}[self.arrow]
	
	def identifier(self):
		return "%s,%s" % (self.association.name,self.entityName)
	
	def value(self):
		return 1.0


class CurvedLeg(Leg):
	
	def __init__(self,association,card,entityName,count,num):
		Leg.__init__(self,association,card,entityName)
		self.count = count
		self.num = num
		self.spin = float(2*self.num)/(self.count-1)-1
	
	def description(self):
		x0,y0 = (self.entity.x + self.entity.w / 2,self.entity.y + self.entity.h / 2)
		x3,y3 = (self.association.x + self.association.w / 2,self.association.y + self.association.h / 2)
		return [
			{
				"key": u"strokeDepth",
				"strokeDepth": self.style["legStrokeDepth"],
			},
			{
				"key": u"env",
				"env": [("ex","""cx[u"%s"]"""%self.entity.name),("ey","""cy[u"%s"]"""%self.entity.name)],
			},
			{
				"key": u"strokeColor",
				"strokeColor": "legStrokeColor",
			},
			{
				"key": u"curve",
				"x0": "ex",
				"y0": "ey",
				"x1": "(3*ex+x+(y-ey)*%s)/4" % self.spin,
				"y1": "(3*ey+y+(x-ex)*%s)/4" % self.spin,
				"x2": "(3*x+ex+(y-ey)*%s)/4" % self.spin,
				"y2": "(3*y+ey+(x-ex)*%s)/4" % self.spin,
				"x3": "x",
				"y3": "y",
			},
			{
				"key": u"card",
				"text": self.cardinalities,
				"textColor": "cardTextColor",
				"ex": "ex",
				"ey": "%s+ey" % (self.style["cardTextHeightRatio"] * self.h),
				"ew": self.entity.w / 2,
				"eh": self.entity.h / 2,
				"ax": "x",
				"ay": "%s+y" % (self.style["cardTextHeightRatio"] * self.h),
				"legIdentifier": self.identifier(),
				"family": self.style["cardFont"]["family"],
				"size": self.style["cardFont"]["size"],
			},
		] + {
			">": [
						{
							"key": u"color",
							"color": "legStrokeColor",
						},
						{
							"key": u"strokeDepth",
							"strokeDepth": 0,
						},
						{
							"key": u"curveArrow",
							"x0": "ex",
							"y0": "ey",
							"x1": "(3*ex+x+(y-ey)*%s)/4" % self.spin,
							"y1": "(3*ey+y+(x-ex)*%s)/4" % self.spin,
							"x2": "(3*x+ex+(y-ey)*%s)/4" % self.spin,
							"y2": "(3*y+ey+(x-ex)*%s)/4" % self.spin,
							"x3": "x",
							"y3": "y",
							"legIdentifier": self.identifier(),
						}
				],
			"<": [
						{
							"key": u"color",
							"color": "legStrokeColor",
						},
						{
							"key": u"strokeDepth",
							"strokeDepth": 0,
						},
						{
							"key": u"curveArrow",
							"x3": "ex",
							"y3": "ey",
							"x2": "(3*ex+x+(y-ey)*%s)/4" % self.spin,
							"y2": "(3*ey+y+(x-ex)*%s)/4" % self.spin,
							"x1": "(3*x+ex+(y-ey)*%s)/4" % self.spin,
							"y1": "(3*y+ey+(x-ex)*%s)/4" % self.spin,
							"x0": "x",
							"y0": "y",
							"legIdentifier": self.identifier(),
						}
				],
			"": []
		}[self.arrow]
	
	def identifier(self):
		return "%s,%s,%s" % (self.association.name,self.entityName,self.spin)
	
	def value(self):
		return 2*self.spin*self.count
	
