#!/usr/bin/env python
# encoding: utf-8

import sys
from association import *
from entity import *
from fontMetrics import FontMetrics

def attract(rows,dx):
	l = sorted(reduce(lambda l1,l2:l1+l2,rows))
	dx = min(dx,min([min([x1-x0 for (x0,x1) in zip(row,row[1:])]+[10000]) for row in rows]+[10000])-1)
	for ref in range(len(l)):
		xRef = l[ref]
		for (j,row) in enumerate(rows):
			w = 0
			for (i,x) in enumerate(row):
				if w == 0 and xRef - dx <= x < xRef: # and (i+1==len(row) or row[i+1]>xRef):
					w = xRef - x
				row[i] += w
		l = sorted(reduce(lambda l1,l2:l1+l2,rows))


class Mcd:
	
	def __init__(self, clauses, params):
		self.entities = {}
		self.associations = {}
		self.elements = {}
		self.ordering = [[]]
		for clause in clauses:
			if clause.strip():
				s = clause.split(":")
				if "," not in s[0] and len(s) == 2:
					element = Entity(clause)
					self.entities[element.name] = element
					self.elements[element.name] = element
					self.ordering[-1].append(self.elements[element.name])
					continue
				if "," in s[0]:
					attr = s[0].split(",")[1].strip()
					element = Association(clause, params)
					self.associations[element.name] = element
					self.elements[element.name] = element
					self.ordering[-1].append(self.elements[element.name])
					continue
			else:
				self.ordering.append([])
		self.ordering = filter(None,self.ordering)
		for association in self.associations.values():
			for leg in association.legs:
				leg.setEntity(self.entities)
				leg.setCardSep(params["sep"])
		self.cardLongestString = "0%sN" % params["sep"]
	
	def calculateSize(self,style):
		def applyAttraction():
			attractedRows = [[box.x+box.w/2 for box in row] for row in self.ordering]
			attract(attractedRows,style["attraction"])
			for (row,attractedRow) in zip(self.ordering,attractedRows):
				for (box,attractedX) in zip(row,attractedRow):
					dx = attractedX-box.w/2 - box.x
					box.x += dx
			self.w = 0
			for row in self.ordering:
				self.w = max(self.w,row[-1].x+row[-1].w)
			self.w += style["marginSize"]
		#
		def cancelExcessiveIndentation():
			dx = min([row[0].x for row in self.ordering]) - style["marginSize"]
			for row in self.ordering:
				for box in row:
					box.x -= dx
			self.w -= dx
		#
		style["cardMaxHeight"] = FontMetrics(style["cardFont"]).getPixelHeight()
		style["cardMaxWidth"] = FontMetrics(style["cardFont"]).getPixelWidth(self.cardLongestString)
		self.w = 0
		verticalOffset = style["marginSize"]
		widths = []
		for row in self.ordering:
			horizontalOffset = style["marginSize"]
			for box in row:
				box.calculateSize(style)
				box.x = horizontalOffset
				horizontalOffset += box.w + style["cardMaxWidth"] + 2 * style["cardMargin"]
			widths.append(row[-1].x + row[-1].w + style["marginSize"])
			self.w = max(self.w,widths[-1])
			maxBoxHeight = max(box.h for box in row)
			for box in row:
				box.y = verticalOffset + (maxBoxHeight-box.h)/2
			verticalOffset += maxBoxHeight + style["cardMaxHeight"] + 2 * style["cardMargin"]
		self.h = verticalOffset - style["cardMaxHeight"] - 2 * style["cardMargin"] + style["marginSize"]
		maxWidth = max(widths)
		for (row,width) in zip(self.ordering,widths):
			for box in row:
				box.x += (maxWidth - width) / 2
		applyAttraction()
		cancelExcessiveIndentation()
	
	def description(self):
		result = []
		for element in self.associations.values():
			result.extend(element.description())
		for element in self.entities.values():
			result.extend(element.description())
		return result
	
