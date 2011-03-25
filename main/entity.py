#!/usr/bin/env python
# encoding: utf-8

from fontMetrics import FontMetrics

from attribute import *

class Entity:
	
	def __init__(self, clause):
		def cleanUp(name,attributes):
			name = name.strip()
			cartouche = (name[:-1] if name[-1].isdigit() else name)
			return (name,cartouche,outerSplit(attributes))
		
		def dispatchStrength(attributes):
			for i in range(len(attributes)):
				if attributes[i] == "":
					attributes[i] = PhantomAttribute()
				elif attributes[i].startswith("-"):
					attributes[i] = WeakAttribute(attributes[i][1:])
				elif attributes[i].startswith("_"):
					attributes[i] = StrongAttribute(attributes[i][1:])
				elif i == 0:
					attributes[i] = StrongAttribute(attributes[i])
				else:
					attributes[i] = SimpleEntityAttribute(attributes[i])
			return attributes
		
		(self.name,self.attributes) = clause.split(":")
		(self.name,self.cartouche,self.attributes) = cleanUp(self.name,self.attributes)
		self.attributes = dispatchStrength(self.attributes)
	
	def calculateSize(self,style):
		cartoucheFont = FontMetrics(style["entityCartoucheFont"])
		self.getCartoucheStringWidth = cartoucheFont.getPixelWidth
		self.cartoucheHeight = cartoucheFont.getPixelHeight()
		attributeFont = FontMetrics(style["entityAttributeFont"])
		self.attributeHeight = attributeFont.getPixelHeight()
		for attribute in self.attributes:
			attribute.calculateSize(style)
		self.w = 2*style["rectMarginWidth"] + max([a.w for a in self.attributes]+[self.getCartoucheStringWidth(self.cartouche)])
		self.h = len(self.attributes)*(self.attributeHeight+style["lineSkipHeight"])-style["lineSkipHeight"]+4*style["rectMarginHeight"]+self.cartoucheHeight
		self.w += self.w % 2
		self.h += self.h % 2
		self.style = style
	
	def description(self):
		result = ["Entity %s" % self.name]
		result.extend([
			{
				"key": u"env",
				"env": [("x","""cx[u"%s"]"""%self.name),("y","""cy[u"%s"]"""%self.name)],
			},
			{
				"key": u"begin",
				"id": u"entity-%s" % self.name,
			},
			{
				"key": u"begin",
				"id": u"frame-%s" % self.name,
			},
			{
				"key": u"strokeDepth",
				"strokeDepth": 0,
			},
			{
				"key": u"strokeColor",
				"strokeColor": "entityCartoucheColor",
			},
			{
				"key": u"color",
				"color": "entityCartoucheColor",
			},
			{
				"key": u"rect",
				"x": "%s+x" % (-self.w/2),
				"y": "%s+y" % (-self.h/2),
				"w": self.w,
				"h": self.cartoucheHeight+2*self.style["rectMarginHeight"],
			},
			{
				"key": u"strokeColor",
				"strokeColor": "entityColor",
			},
			{
				"key": u"color",
				"color": "entityColor",
			},
			{
				"key": u"rect",
				"x": "%s+x" % (-self.w/2),
				"y": "%s+y" % (-self.h/2+self.cartoucheHeight+2*self.style["rectMarginHeight"]),
				"w": self.w,
				"h": self.h - self.cartoucheHeight-2*self.style["rectMarginHeight"],
			},
			{
				"key": u"strokeColor",
				"strokeColor": "entityStrokeColor",
			},
			{
				"key": u"strokeDepth",
				"strokeDepth": self.style["boxStrokeDepth"],
			},
			{
				"key": u"color",
				"color": "transparentColor",
			},
			{
				"key": u"rect",
				"x": "%s+x" % (-self.w/2),
				"y": "%s+y" % (-self.h/2),
				"w": self.w,
				"h": self.h,
			},
			{
				"key": u"strokeDepth",
				"strokeDepth": self.style["innerStrokeDepth"],
			},
			{
				"key": u"line",
				"x0": "%s+x" % (-self.w/2),
				"y0": "%s+y" % (-self.h/2+self.cartoucheHeight+2*self.style["rectMarginHeight"]),
				"x1": "%s+x" % (self.w/2),
				"y1": "%s+y" % (-self.h/2+self.cartoucheHeight+2*self.style["rectMarginHeight"]),
			},
			{
				"key": u"end",
			},
			{
				"key": u"text",
				"family": self.style["entityCartoucheFont"]["family"],
				"size": self.style["entityCartoucheFont"]["size"],
				"text": self.cartouche,
				"textColor": "entityCartoucheTextColor",
				"x": "%s+x" % (-self.getCartoucheStringWidth(self.cartouche)/2),
				"y": "%s+y" % (-self.h/2+ self.style["rectMarginHeight"] + self.style["cartoucheTextHeightRatio"] * self.cartoucheHeight),
			},
		])
		dx = self.style["rectMarginWidth"] - self.w/2
		dy = self.cartoucheHeight + 3*self.style["rectMarginHeight"] - self.h/2
		for attribute in self.attributes:
			attribute.name = self.name
			result.extend(attribute.description(dx,dy))
			dy += self.attributeHeight + self.style["lineSkipHeight"]
		result.extend([
			{
				"key": u"end",
			},
		])
		return result
