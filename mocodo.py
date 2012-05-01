#!/usr/bin/env python
# encoding: utf-8


"""
mocodo.py

Created by Aristide Grange on 2010-04-03.
"""

import sys
import getopt
import os
try:
	import json
except ImportError:
	import simplejson as json
from main.common import *

print(sys.version)
if sys.version >= "3":
	print "Mocodo does not work under Python %s." % sys.version
	print "Please install Python 2.7 or 2.6 (or 2.5 + simplejson)."
	sys.exit()

help_message = '''
Mocodo est un traceur de Modèles Conceptuels de Données.
À partir d'une liste ordonnée d'entités et d'associations,
il génère une représentation du MCD dans différents formats,
actuellement:
- SVG, le dialecte de XML dédié au dessin vectoriel;
- NodeBox 2, une application Mac OS X de création d'images 2D
à l'aide de Python: http://nodebox.net/code/index.php/Home.
Pour les instructions, merci de vous reporter au site:
http://code.google.com/p/mocodo/ ou à la documentation incluse.
'''

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def recreateDefaultParamsFile():
	if sys.platform.lower().startswith("darwin"):
		if os.path.exists("/Applications/NodeBox/NodeBox.app") or os.path.exists("/Applications/NodeBox.app"):
			params = json.loads(open("pristine/macNodebox.json").read())
		else:
			params = json.loads(open("pristine/mac.json").read())
	elif sys.platform.lower().startswith("win"):
		params = json.loads(open("pristine/windows.json").read())
	else:
		params = json.loads(open("pristine/linux.json").read())
	open("default.json","w").write(json.dumps(params, sort_keys=True, indent=4))

def recreateDefaultMcd():
	open("sandbox.mcd","w").write(open("pristine/sandbox.mcd").read())

def main():
	argv = sys.argv
	try:
		try:
			(opts,args) = getopt.getopt(argv[1:], "hvo:i:c:s:e:m:a:", ["help", "version", "output=", "input=", "colors=", "shapes=", "df=", "sep=", "cleanup", "encoding=", "table=", "attraction=", "extract", "tkinter"])
		except getopt.error, msg:
			raise Usage(msg)
		if "--cleanup" in [option for (option,value) in opts]:
			recreateDefaultParamsFile()
			recreateDefaultMcd()
			return
		if not os.path.exists("default.json"):
			recreateDefaultParamsFile()
		params = json.loads(open("default.json").read())
		if params["input"] == "sandbox.mcd" and not os.path.exists("sandbox.mcd"):
			recreateDefaultMcd()
		# option processing
		for (option,value) in opts:
			if   option in ("-h", "--help"):       raise Usage(help_message)
			elif option in ("-v", "--version"):    raise Usage("version %s" % version)
			elif option in ("-o", "--output"):     params["output"] = value
			elif option in ("-i", "--input"):      params["input"] = value
			elif option in ("-c", "--colors"):     params["colors"] = value
			elif option in ("-s", "--shapes"):     params["shapes"] = value
			elif option in ("-e", "--encoding"):   params["encoding"] = value
			elif option in ("-m", "--table"):      params["table"] = value
			elif option in ("-a", "--attraction"): params["attraction"] = value
			elif option == "--df":                 params["df"] = unicode(value)
			elif option == "--sep":                params["sep"] = value
			elif option == "--extract":            params["extract"] = True
			elif option == "--tkinter":            params["tkinter"] = True
		# launching
		if params["output"].endswith("svg.py"):
			import mcd2svg
			mcd2svg.main(params)
			__import__(params["output"][:-3])
		elif params["output"].endswith("nodebox.py"):
			import mcd2nodebox
			mcd2nodebox.main(params)
			os.system("open -a NodeBox %s" % params["output"])
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	path = sys.path[0]
	if os.path.isdir(path):
		os.chdir(path)
	else:
		os.chdir(os.path.dirname(path))
	sys.exit(main())
