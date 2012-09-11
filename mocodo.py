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

class MocodoError(Exception):
	pass

if sys.version >= "3":
	raise MocodoError(_("Mocodo does not work under Python %s.\nPlease install Python 2.7 or 2.6 (or 2.5 + simplejson).") % sys.version)

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

import gettext
import locale
import re

def initLocalization(language = ""):
	if language == "":
		if sys.platform.lower().startswith("darwin") and os.system("defaults read -g AppleLanguages > /tmp/languages.txt")==0:
			language = re.search("\W*(\w+)",open("/tmp/languages.txt").read()).group(1)
		else:
			try:
				language = locale.getdefaultlocale()[0][:2]
			except:
				pass
	try:
		trans = gettext.GNUTranslations(open("res/messages_%s.mo" % language,"rb") )
	except IOError:
		trans = gettext.NullTranslations()
	trans.install(unicode=True)


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
	open("sandbox.mcd","w").write(open("pristine/sandbox.mcd").read())

def main():
	try:
		try:
			(opts,args) = getopt.getopt(sys.argv[1:], "l:o:i:c:s:e:m:a:hxv", "cleanup,help,extract,tkinter,version,default=,language=,output=,input=,colors=,shapes=,encodings=,tables=,attraction=,df=,sep=".split(","))
		except getopt.error, msg:
			raise Usage(msg)
		initialDir = os.getcwd()
		if os.path.dirname(sys.argv[0]):
			os.chdir(os.path.dirname(sys.argv[0]))
		opts = dict(opts)
		if "--cleanup" in opts:
			return recreateDefaultParamsFile()
		if not os.path.exists("default.json"):
			recreateDefaultParamsFile()
		if "--default" in opts:
			defaultPath = os.path.join(initialDir,opts["--default"])
		else:
			defaultPath = "default.json"
		params = json.loads(open(defaultPath).read())
		# option processing
		for (option,value) in opts.iteritems():
			if   option in ("-h", "--help"):       raise Usage(help_message)
			elif option in ("-x", "--extract"):    params["extract"] = True
			elif option in ("-v", "--version"):    raise Usage("version %s" % version)
			elif option in ("-o", "--output"):     params["output"] = value
			elif option in ("-i", "--input"):      params["input"] = value
			elif option in ("-c", "--colors"):     params["colors"] = value
			elif option in ("-s", "--shapes"):     params["shapes"] = value
			elif option in ("-e", "--encodings"):  params["encodings"] = value.split(",")
			elif option in ("-m", "--tables"):     params["tables"] = value.split(",")
			elif option in ("-a", "--attraction"): params["attraction"] = value
			elif option in ("-l", "--language"):   params["language"] = value
			elif option == "--tkinter":            params["tkinter"] = True
			elif option == "--df":                 params["df"] = unicode(value)
			elif option == "--sep":                params["sep"] = value
		params["dirRootExt"] = os.path.join(initialDir,params["input"])
		params["dirRoot"] = os.path.splitext(params["dirRootExt"])[0]
		(params["dir"],params["root"]) = os.path.split(params["dirRoot"])
		initLocalization(params.get("language",""))
		del params["input"]
		del params["language"]
		# launching
		try:
			if params["output"]=="svg":
				import main.mcd2svg
				main.mcd2svg.main(params)
				os.chdir(params["dir"])
				sys.path.append(params["dir"])
				__import__("%(root)s-svg" % params)
			elif params["output"]=="nodebox":
				import main.mcd2nodebox
				main.mcd2nodebox.main(params)
				os.chdir(params["dir"])
				os.system("""open -a NodeBox "%(root)s-nodebox.py" """ % params)
		except RuntimeError, err:
			msg = str(err)
			if msg.startswith("Mocodo Err."):
				try:
					print >> sys.stderr, msg
				except UnicodeDecodeError:
					print >> sys.stderr, msg.decode("utf8")
			else:
				raise
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())
