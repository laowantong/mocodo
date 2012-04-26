#!/Library/Frameworks/Python.framework/Versions/2.6/bin/python2.6
# encoding: utf-8

import unittest
from fontMetrics import *

# print tkFont.families()

helv36b  = FontMetricsWithTk({"family":"Helvetica","size":36,"weight":"bold"})
helv36b2 = FontMetricsWithTk({"family":"Helvetica-Bold","size":36})
helv36b3 = FontMetricsWithTk({"family":"Helvetica-Bold","size":36,"weight":"bold"})
helv36b4 = FontMetricsWithTk({"family":"Helvetica-Bold","size":36,"weight":tkFont.BOLD})
helv36   = FontMetricsWithTk({"family":"Helvetica","size":36})
times12  = FontMetricsWithTk({"family":"Times","size":12})

class FontMetricsWithTkTest(unittest.TestCase):
	
	def testHelv36GetPixelHeight(self):
		self.assertEqual(helv36.getPixelHeight(),36)
	
	def testHelv36bGetPixelHeight(self):
		self.assertEqual(helv36b.getPixelHeight(),36)
	
	def testTimes12GetPixelHeight(self):
		self.assertEqual(times12.getPixelHeight(),12)
	
	def testHelv36GetPixelWidth(self):
		self.assertEqual(helv36.getPixelWidth("My string"),146)
	
	def testHelv36bGetPixelWidth(self):
		self.assertEqual(helv36b.getPixelWidth("My string"),160)
	
	def testHelv36b2GetPixelWidth(self):
		self.assertEqual(helv36b2.getPixelWidth("My string"),161)
	
	def testHelv36b3GetPixelWidth(self):
		self.assertEqual(helv36b3.getPixelWidth("My string"),177)
	
	def testHelv36b4GetPixelWidth(self):
		self.assertEqual(helv36b4.getPixelWidth("My string"),177)
	
	def testTimes12GetPixelWidth(self):
		self.assertEqual(times12.getPixelWidth("My string"),47)
	
	def testEmptyStringGetPixelWidth(self):
		self.assertEqual(times12.getPixelWidth(""),0)

courier12 = FontMetricsWithoutTk({"family":"Courier","size":12})
proportional = FontMetricsWithoutTk({"family":"Helvetica","size":12})
prestige = FontMetricsWithoutTk({"family":"Prestige Elite Std","size":12})

class FontMetricsWithoutTkTest(unittest.TestCase):
	
	def testCourier12GetPixelHeight(self):
		self.assertEqual(courier12.getPixelHeight(),12)
	
	def testCourier12GetPixelWidth(self):
		self.assertEqual(courier12.getPixelWidth("My string"),63)
	
	def testFallbackGetPixelHeight(self):
		self.assertEqual(proportional.getPixelHeight(),12)
	
	def testFallbackGetPixelWidth(self):
		self.assertEqual(proportional.getPixelWidth("My string"),63)
	
	def testPrestigeGetPixelHeight(self):
		self.assertEqual(prestige.getPixelHeight(),13)
	
	def testPrestigeGetPixelWidth(self):
		self.assertEqual(prestige.getPixelWidth("My string"),63)
	

if __name__ == '__main__':
	unittest.main()
