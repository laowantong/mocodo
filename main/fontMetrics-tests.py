#!env python
# encoding: utf-8

import unittest
from fontMetrics import *

# print tkFont.families()

widthFactor = 1.0

helv36b  = FontMetrics({"family":"Helvetica","size":36,"weight":"bold"})
helv36b2 = FontMetrics({"family":"Helvetica-Bold","size":36})
helv36b3 = FontMetrics({"family":"Helvetica-Bold","size":36,"weight":"bold"})
helv36b4 = FontMetrics({"family":"Helvetica-Bold","size":36,"weight":tkFont.BOLD})
helv36   = FontMetrics({"family":"Helvetica","size":36})
times12  = FontMetrics({"family":"Times","size":12})

class FontMetricsTest(unittest.TestCase):
	
	def testGetPixelHeight(self):
		self.assertEqual(helv36.getPixelHeight(),36)
		self.assertEqual(helv36b.getPixelHeight(),36)
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
		self.assertEqual(times12.getPixelWidth(""),0)
	

if __name__ == '__main__':
	unittest.main()
