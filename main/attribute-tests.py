#!/usr/bin/python
# encoding: utf-8

import unittest
from attribute import *

class OuterSplitTest(unittest.TestCase):
	
	def testRun(self):
		self.assertEqual(outerSplit(""),[])
		self.assertEqual(outerSplit("aaa,bbb,ccc"),["aaa","bbb","ccc"])
		self.assertEqual(outerSplit("aaa , bbb , ccc"),["aaa","bbb","ccc"])
		self.assertEqual(outerSplit("aaa [ddd, eee],bbb,ccc"),["aaa [ddd, eee]","bbb","ccc"])
		self.assertEqual(outerSplit("aaa,bbb,"),["aaa","bbb", ""])
		self.assertEqual(outerSplit("aaa [,],bbb,ccc"),["aaa [,]","bbb","ccc"])
		self.assertEqual(outerSplit("aaa [ddd, eee] ,bbb,ccc"),["aaa [ddd, eee]","bbb","ccc"])

if __name__ == '__main__':
	unittest.main()