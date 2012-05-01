#!/usr/bin/env python
# encoding: utf-8

import sys
import codecs
try:
	import json
except ImportError:
	import simplejson as json

try:
	import Tkinter as tk
	import tkFont
	root = tk.Tk()
except:
	root = None

def fontMetricsFactory(tkinter):
	if tkinter:
		if root:
			return FontMetricsWithTk
		else:
			sys.stderr.write(u"Warning: Tkinter is not correctly installed or Mocodo is run on server side with no display. Option 'tkinter' ignored.\n")
	text = codecs.open("main/fontMetrics.json","r","utf8").read()
	FontMetricsWithoutTk.staticData = json.loads(text)
	return FontMetricsWithoutTk

class FontMetricsWithTk():
	
	def __init__(self,font):
		kargs = dict((str(k),v) for (k,v) in font.iteritems())
		kargs["size"] = -font["size"]
		self.font = tkFont.Font(**kargs)
	
	def getPixelHeight(self):
		return self.font.metrics("linespace")
	
	def getPixelWidth(self,string):
		return self.font.measure(string)


class FontMetricsWithoutTk():
	
	def __init__(self,font):
		if font["family"] not in self.staticData["fonts"]:
			sys.stderr.write(u"Warning: Missing metrics for font '%s'. If it is installed on your system, you may run updateFontMetrics.py to add it (require Tkinter). In the meantime, I will replace it by Courier New.\n" % font["family"])
			font["family"] = "Courier New"
		refSize = self.staticData["size"]
		metrics = self.staticData["fonts"][font["family"]]
		self.fontHeight = int((metrics["height"]*font["size"]+0.5)/refSize)
		self.width = dict((c,ord(x)) for (c,x) in zip(self.staticData["alphabet"],metrics.get("widths",[])))
		self.ratio = font["size"]*metrics.get("correction",1.0)/refSize
		self.defaultWidth = metrics["default"]
	
	def getPixelHeight(self):
		return self.fontHeight
	
	def getPixelWidth(self,string):
		return int(self.ratio*sum(self.width.get(c,self.defaultWidth) for c in string)+0.5)

