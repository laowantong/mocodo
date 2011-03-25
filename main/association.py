#!/usr/bin/env python
# encoding: utf-8

from fontMetrics import FontMetrics

from attribute import *
from leg import *

class Association:
	
	def __init__(self, clause, params = {"df": u"DF"}):
		def cleanUp(name,legs,attributes):
			name = name.strip()
			cartouche = (name[:-1] if name[-1].isdigit() else name)
			(cards,entities) = zip(*[i.strip().split(" ",1) for i in legs.split(",")])
			return (name,cartouche,cards,list(entities),outerSplit(attributes))
		
		(name,legsAndAttributes) = clause.split(",",1)
		(legs,attributes) = (legsAndAttributes.split(":")+[""])[:2]
		(self.name,self.cartouche,cards,entities,attributes) = cleanUp(name,legs,attributes)
		self.attributes = [SimpleAssociationAttribute(attribute) for attribute in attributes]
		entities = [(e.strip(),entities.count(e),entities[:i].count(e)) for (i,e) in enumerate(entities)]
		self.legs = [(StraightLeg(self,card,entity) if count == 1 else CurvedLeg(self,card,entity,count,num)) for (card,(entity,count,num)) in zip(cards,entities)]
		self.dfLabel = params["df"]
		self.checkDfStrategy(self.cartouche == self.dfLabel)
	
	def calculateSize(self,style):
		self.style = style
		cartoucheFont = FontMetrics(style["associationCartoucheFont"])
		self.getCartoucheStringWidth = cartoucheFont.getPixelWidth
		self.cartoucheHeight = cartoucheFont.getPixelHeight()
		attributeFont = FontMetrics(style["associationAttributeFont"])
		self.attributeHeight = attributeFont.getPixelHeight()
		self.calculateSizeDependingOnDf()
		self.w += self.w % 2
		self.h += self.h % 2
		for leg in self.legs:
			leg.calculateSize(style)
	
	def checkDfStrategy(self, isDf):
			
		def calculateSizeWhenDf():
			self.w = self.h = max(self.style["roundRectMarginWidth"]*2+self.getCartoucheStringWidth(self.dfLabel),self.style["roundRectMarginWidth"]*2+self.cartoucheHeight)
		
		def calculateSizeWhenNotDf():
			for attribute in self.attributes:
				attribute.calculateSize(self.style)
			self.w = 2*self.style["roundRectMarginWidth"] + max([a.w for a in self.attributes]+[self.getCartoucheStringWidth(self.cartouche)])
			self.h = max(1,len(self.attributes))*(self.attributeHeight+self.style["lineSkipHeight"])-self.style["lineSkipHeight"]+2*self.style["rectMarginHeight"]+2*self.style["roundRectMarginHeight"]+self.cartoucheHeight
		
		def descriptionWhenDf():
			return [
				{
					"key": u"strokeDepth",
					"strokeDepth": self.style["boxStrokeDepth"],
				},
				{
					"key": u"strokeColor",
					"strokeColor": "associationStrokeColor",
				},
				{
					"key": u"color",
					"color": "associationCartoucheColor",
				},
				{
					"key": u"circle",
					"cx": "x",
					"cy": "y",
					"r": self.w/2.0,
				},
				{
					"key": u"text",
					"text": self.dfLabel,
					"textColor": "associationCartoucheTextColor",
					"x": "%s+x" % (self.style["roundRectMarginWidth"]-self.w/2),
					"y": "%s+y" % (self.style["roundRectMarginHeight"]-self.h/2 + self.style["dfTextHeightRatio"] * self.cartoucheHeight),
					"family": self.style["associationCartoucheFont"]["family"],
					"size": self.style["associationCartoucheFont"]["size"],
				},
			]
		
		def descriptionWhenNotDf():
			result = [
				{
					"key": u"strokeDepth",
					"strokeDepth": 0,
				},
				{
					"key": u"strokeColor",
					"strokeColor": "associationCartoucheColor",
				},
				{
					"key": u"color",
					"color": "associationCartoucheColor",
				},
				{
					"key": u"upperRoundRect",
					"radius": self.style["roundCornerRadius"],
					"x": "%s+x" % (-self.w/2),
					"y": "%s+y" % (-self.h/2),
					"w": self.w,
					"h": self.attributeHeight + self.style["roundRectMarginHeight"] + self.style["rectMarginHeight"],
				},
				{
					"key": u"strokeColor",
					"strokeColor": "associationColor",
				},
				{
					"key": u"color",
					"color": "associationColor",
				},
				{
					"key": u"lowerRoundRect",
					"radius": self.style["roundCornerRadius"],
					"x": "%s+x" % (-self.w/2),
					"y": "%s+y" % (self.attributeHeight + self.style["roundRectMarginHeight"] + self.style["rectMarginHeight"]-self.h/2),
					"w": self.w,
					"h": self.h - (self.attributeHeight + self.style["roundRectMarginHeight"] + self.style["rectMarginHeight"]),
				},
				{
					"key": u"color",
					"color": "transparentColor",
				},
				{
					"key": u"strokeColor",
					"strokeColor": "associationStrokeColor",
				},
				{
					"key": u"strokeDepth",
					"strokeDepth": self.style["boxStrokeDepth"],
				},
				{
					"key": u"roundRect",
					"radius": self.style["roundCornerRadius"],
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
					"y0": "%s+y" % (self.attributeHeight + self.style["roundRectMarginHeight"] + self.style["rectMarginHeight"]-self.h/2),
					"x1": "%s+x" % (self.w/2),
					"y1": "%s+y" % (self.attributeHeight + self.style["roundRectMarginHeight"] + self.style["rectMarginHeight"]-self.h/2),
				},
				{
					"key": u"text",
					"text": self.cartouche,
					"textColor": "associationCartoucheTextColor",
					"x": "%s+x" % (-self.getCartoucheStringWidth(self.cartouche)/2),
					"y": "%s+y" % (-self.h/2+ self.style["rectMarginHeight"] + self.style["cartoucheTextHeightRatio"] * self.cartoucheHeight),
					"family": self.style["associationCartoucheFont"]["family"],
					"size": self.style["associationCartoucheFont"]["size"],
				}
			]
			dx = self.style["roundRectMarginWidth"] - self.w/2
			dy = self.style["roundRectMarginHeight"] + self.cartoucheHeight + 2*self.style["rectMarginHeight"] - self.h/2
			for attribute in self.attributes:
				attribute.name = self.name
				result.extend(attribute.description(dx,dy))
				dy += self.attributeHeight + self.style["lineSkipHeight"]
			return result
		
		if isDf:
			self.calculateSizeDependingOnDf = calculateSizeWhenDf
			self.descriptionDependingOnDf = descriptionWhenDf
		else:
			self.calculateSizeDependingOnDf = calculateSizeWhenNotDf
			self.descriptionDependingOnDf = descriptionWhenNotDf
	
	def setDfLabel(self,dfLabel):
		self.setDfLabelDependingOnDf(dfLabel)
	
	def description(self):
		return self.legDescriptions() + [
			{
				"key": u"begin",
				"id": u"association-%s" % self.name,
			},
			] + self.descriptionDependingOnDf() + [
			{
				"key": u"end",
			},
			]
	
	def legDescriptions(self):
		result = [
			"Association %s" % self.name,
			{
				"key": u"env",
				"env": [("x","""cx[u"%s"]"""%self.name),("y","""cy[u"%s"]"""%self.name)],
			},
		]
		for leg in self.legs:
			result.extend(leg.description())
		return result
	
	def legIdentifiers(self):
		for leg in self.legs:
			yield leg.identifier()
	