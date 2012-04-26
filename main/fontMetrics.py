#!/usr/bin/env python
# encoding: utf-8

try:
	import Tkinter as tk
	import tkFont
	root = tk.Tk()
except:
	import sys
	sys.stderr.write(u"Warning: Tkinter is not correctly installed or Mocodo is run on server side with no display. All proportional fonts are replaced by Courier.\n")
	root = None

def FontMetrics(font):
	if root is None:
		return FontMetricsWithoutTk(font)
	return FontMetricsWithTk(font)

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
		monospaceFonts = {
			u"@BatangChe": (128, 256),
			u"@DFKai-SB": (128, 256),
			u"@DotumChe": (128, 256),
			u"@FangSong": (128, 256),
			u"@GulimChe": (128, 256),
			u"@GungsuhChe": (128, 256),
			u"@KaiTi": (128, 256),
			u"@MS Gothic": (128, 256),
			u"@MS Mincho": (128, 256),
			u"@MingLiU": (128, 256),
			u"@MingLiU-ExtB": (128, 256),
			u"@MingLiU_HKSCS": (128, 256),
			u"@MingLiU_HKSCS-ExtB": (128, 256),
			u"@NSimSun": (128, 256),
			u"@SimHei": (128, 256),
			u"@SimSun": (128, 256),
			u"@SimSun-ExtB": (128, 256),
			u"Andale Mono": (154, 299),
			u"Ayuthaya": (154, 355),
			u"BatangChe": (128, 256),
			u"Bookshelf Symbol 7": (256, 256),
			u"Braille": (213, 256),
			u"Consolas": (141, 300),
			u"Courier": (154, 290),
			u"Courier 10 Pitch": (154, 297),
			u"Courier New": (154, 290),
			u"Courier New Bold": (154, 290),
			u"Courier New Bold Italic": (154, 290),
			u"Courier New Italic": (154, 290),
			u"DFKai-SB": (128, 256),
			u"DejaVu Sans Mono": (154, 298),
			u"DotumChe": (128, 256),
			u"Estrangelo Edessa": (128, 256),
			u"FangSong": (128, 256),
			u"ForMateKonaVe Regular": (154, 298),
			u"FreeMono": (154, 257),
			u"GB18030 Bitmap": (256, 320),
			u"Gautami": (128, 445),
			u"GulimChe": (128, 256),
			u"GungsuhChe": (128, 256),
			u"HAN NOM A": (128, 255),
			u"HAN NOM B": (128, 255),
			u"HanaMinA Regular": (256, 259),
			u"HanaMinB Regular": (256, 263),
			u"Hoefler Text Ornaments": (256, 259),
			u"Inconsolata": (154, 299),
			u"JiaguRic A": (128, 281),
			u"JiaguRic B": (128, 281),
			u"KaiTi": (128, 256),
			u"KufiStandardGK": (128, 361),
			u"LM Mono 10 Italic": (134, 341),
			u"LM Mono 10 Regular": (134, 341),
			u"LM Mono 12 Regular": (132, 341),
			u"LM Mono 8 Regular": (136, 342),
			u"LM Mono 9 Regular": (134, 341),
			u"LM Mono Caps 10 Oblique": (134, 333),
			u"LM Mono Caps 10 Regular": (134, 333),
			u"LM Mono Light 10 Bold": (134, 345),
			u"LM Mono Light 10 Bold Oblique": (134, 345),
			u"LM Mono Light 10 Oblique": (134, 336),
			u"LM Mono Light 10 Regular": (134, 336),
			u"LM Mono Light Cond 10 Oblique": (90, 336),
			u"LM Mono Light Cond 10 Regular": (90, 336),
			u"LM Mono Slanted 10 Regular": (134, 341),
			u"Latha": (128, 351),
			u"Letter Gothic Std": (154, 311),
			u"Liberation Mono": (154, 290),
			u"Lucida Console": (154, 256),
			u"MS Gothic": (128, 256),
			u"MS Mincho": (128, 256),
			u"MV Boli": (256, 413),
			u"Mangal": (128, 430),
			u"Marlett": (256, 256),
			u"Menlo Bold": (154, 298),
			u"Menlo Bold Italic": (154, 298),
			u"Menlo Italic": (154, 298),
			u"Menlo Regular": (154, 298),
			u"MingLiU": (128, 256),
			u"MingLiU-ExtB": (128, 256),
			u"MingLiU_HKSCS": (128, 256),
			u"MingLiU_HKSCS-ExtB": (128, 256),
			u"Miriam Fixed": (154, 253),
			u"Monaco": (154, 320),
			u"Monospace": (154, 299),
			u"NSimSun": (128, 256),
			u"Nimbus Mono L": (154, 282),
			u"OCR A Std": (184, 272),
			u"Orator Std": (154, 342),
			u"Osaka−等幅": (128, 268),
			u"PC¸ív": (128, 258),
			u"Prestige Elite Std": (154, 290),
			u"QXyingbikai": (256, 280),
			u"QXyingbixing": (256, 280),
			u"Raavi": (128, 425),
			u"Ricsung New B": (128, 281),
			u"Rod": (154, 251),
			u"Shruti": (128, 430),
			u"SimHei": (128, 256),
			u"SimSun": (128, 256),
			u"SimSun-ExtB": (128, 256),
			u"Simplified Arabic Fixed": (154, 280),
			u"TeX Gyre Cursor": (154, 307),
			u"TeX Gyre Cursor Bold": (154, 345),
			u"TeX Gyre Cursor Bold Italic": (154, 349),
			u"TeX Gyre Cursor Italic": (154, 307),
			u"Tex Gyre Cursor": (154, 307),
			u"TextMateJ Regular": (154, 298),
			u"Tlwg Typist": (154, 318),
			u"Tlwg Typo": (154, 318),
			u"TlwgMono": (154, 316),
			u"TlwgTypewriter": (154, 328),
			u"Tunga": (128, 425),
			u"Ubuntu Mono": (128, 257),
			u"WST_Czec": (50, 192),
			u"WST_Engl": (50, 192),
			u"WST_Fren": (50, 192),
			u"WST_Germ": (50, 192),
			u"WST_Ital": (50, 192),
			u"WST_Span": (50, 192),
			u"WST_Swed": (50, 192),
			u"Wingdings 2": (228, 270),
			u"pangzhonghua": (128, 256),
			u"文泉驛等寬微米黑": (154, 301),
		}
		actualFont = (font["family"] if font["family"] in monospaceFonts else u"Courier")
		font["family"] = actualFont
		(self.fontWidth,self.fontHeight) = monospaceFonts[actualFont]
		self.fontWidth = self.fontWidth*font["size"]/256.0
		self.fontHeight = int((self.fontHeight*font["size"]+0.5)/256)
	
	def getPixelHeight(self):
		return self.fontHeight
	
	def getPixelWidth(self,string):
		return int(self.fontWidth * len(string))
