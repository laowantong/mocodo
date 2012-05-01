#!/usr/bin/env python
# encoding: utf-8

import fontMetrics

import re

findallOuterCommas = re.compile(r'[^,]+\[.*?\][^,]*|[^,]+').findall
def outerSplit(s):
	return [s.replace(", ",",").strip() for s in findallOuterCommas(s.replace(",",", "))]

searchLabelAndType = re.compile(r"^(.*?)(?: *\[(.*)\])?$").search


class Attribute:
	
	def __init__(self, attribute):
		(self.label,self.attributeType) = searchLabelAndType(attribute).groups()
		self.boxType = "entity"
		self.fontType = "entityAttributeFont"
	
	def calculateSize(self,style):
		self.attributeFont = style[self.fontType]
		font = fontMetrics.FontMetrics(self.attributeFont)
		self.w = font.getPixelWidth(self.label)
		self.h = font.getPixelHeight()
		self.style = style
	
	def description(self,dx,dy):
		return [
			{
				"key": u"text",
				"text": self.label,
				"textColor": self.boxType + "AttributeTextColor",
				"x": "%s+x" % (dx),
				"y": "%s+y" % (dy+self.style["attributeTextHeightRatio"] * self.h),
				"family": self.attributeFont["family"],
				"size": self.attributeFont["size"],
			}
		]

class SimpleEntityAttribute(Attribute):
	
	def __init__(self, attribute):
		Attribute.__init__(self, attribute)
	
	def getCategory(self):
		return "simple"
	

class SimpleAssociationAttribute(Attribute):
	
	def __init__(self, attribute):
		Attribute.__init__(self, attribute)
		self.boxType = "association"
		self.fontType = "associationAttributeFont"
	

class StrongAttribute(Attribute):
	
	def __init__(self, attribute):
		Attribute.__init__(self, attribute)
	
	def getCategory(self):
		return "strong"
	
	def description(self,dx,dy):
		return Attribute.description(self,dx,dy) + [
			{
				"key": u"strokeDepth",
				"strokeDepth": self.style["underlineDepth"],
			},
			{
				"key": u"strokeColor",
				"strokeColor": "entityAttributeTextColor",
			},
			{
				"key": u"line",
				"x0": "%s+x" % (dx),
				"y0": "%s+y" % (dy + self.h + self.style["underlineSkipHeight"]),
				"x1": "%s+x" % (dx + self.w),
				"y1": "%s+y" % (dy + self.h + self.style["underlineSkipHeight"]),
			}
		]
	

class WeakAttribute(Attribute):
	
	def __init__(self, attribute):
		Attribute.__init__(self, attribute)
	
	def getCategory(self):
		return "weak"
	
	def description(self,dx,dy):
		return Attribute.description(self,dx,dy) + [
			{
				"key": u"strokeDepth",
				"strokeDepth": self.style["underlineDepth"],
			},
			{
				"key": u"strokeColor",
				"strokeColor": "entityAttributeTextColor",
			},
			{
				"key": u"dashLine",
				"x0": "%s+x" % (dx),
				"x1": "%s+x" % (dx + self.w),
				"y": "%s+y" % (dy + self.h + self.style["underlineSkipHeight"]),
				"dashWidth": self.style["dashWidth"],
			}
		]

class PhantomAttribute(Attribute):
	
	def __init__(self):
		Attribute.__init__(self, "")
	
	def getCategory(self):
		return "phantom"
	
	def description(self, dx, dy):
		return []
