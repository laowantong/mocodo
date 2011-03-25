#!/usr/bin/env python
# encoding: utf-8

import Tkinter as tk
import tkFont
root = tk.Tk()

class FontMetrics():
	
	def __init__(self,font):
		kargs = dict((str(k),v) for (k,v) in font.iteritems())
		kargs["size"] = -font["size"]
		self.font = tkFont.Font(**kargs)
	
	def getPixelHeight(self):
		return self.font.metrics("linespace")
	
	def getPixelWidth(self,string):
		return self.font.measure(string)
	

