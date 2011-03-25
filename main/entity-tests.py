#!/usr/bin/env python
# encoding: utf-8

import unittest
from entity import *


class EntityTest(unittest.TestCase):
	
	def testDefault(self):
		entities = [
			Entity("PARTICIPANT: numero, nom, adresse"),
			Entity("PARTICIPANT:numero,nom,adresse"),
			Entity(" PARTICIPANT: numero, nom, adresse "),
			Entity("PARTICIPANT :numero ,nom ,adresse"),
			Entity("PARTICIPANT: _numero, nom, adresse"),
		]
		for e in entities:
			self.assertEqual(e.name,"PARTICIPANT")
			self.assertEqual(e.cartouche,"PARTICIPANT")
			self.assertEqual([a.label for a in e.attributes], ["numero","nom","adresse"])
			self.assertEqual([a.getCategory() for a in e.attributes], ["strong","simple","simple"])
	
	def testAttributeTypes(self):
		e = Entity("PARTICIPANT: numero [type1], nom [type2] , adresse[type3]")
		self.assertEqual([a.label for a in e.attributes], ["numero","nom","adresse"])
		self.assertEqual([a.attributeType for a in e.attributes], ["type1","type2","type3"])
		e = Entity("PARTICIPANT: numero [type a,b,c], nom [type2], adresse [type3]")
		self.assertEqual([a.attributeType for a in e.attributes], ["type a,b,c","type2","type3"])
		e = Entity("PARTICIPANT: numero [], nom, adresse [type3]")
		self.assertEqual([a.attributeType for a in e.attributes], ["",None,"type3"])
		e = Entity("PARTICIPANT: numero [, nom, adresse")
		self.assertEqual([a.attributeType for a in e.attributes], [None,None,None])
	
	def testNumberedEntity(self):
		e = Entity("PARTICIPANT5: numero, nom, adresse")
		self.assertEqual(e.name,"PARTICIPANT5")
		self.assertEqual(e.cartouche,"PARTICIPANT")
	
	def testBlank(self):
		e = Entity("MOT-CLEF: mot-clef, ,")
		self.assertEqual([a.label for a in e.attributes], ["mot-clef","",""])
		self.assertEqual([a.getCategory() for a in e.attributes], ["strong","phantom","phantom"])
	
	def testAllBlank(self):
		e = Entity("BLANK: , ,")
		self.assertEqual([a.label for a in e.attributes], ["","",""])
		self.assertEqual([a.getCategory() for a in e.attributes], ["phantom","phantom","phantom"])
	
	def testWeak(self):
		e = Entity("LIVRE: -Num. exemplaire, État du livre, Date d'achat")
		self.assertEqual([a.label for a in e.attributes], ["Num. exemplaire","État du livre", "Date d'achat"])
		self.assertEqual([a.getCategory() for a in e.attributes], ["weak","simple","simple"])
	
	def testWeakWithOtherMinus(self):
		e = Entity("LIVRE: -Num.-exemplaire, État-du-livre, Date-d'achat")
		self.assertEqual([a.label for a in e.attributes], ["Num.-exemplaire","État-du-livre", "Date-d'achat"])
		self.assertEqual([a.getCategory() for a in e.attributes], ["weak","simple","simple"])
	
	def testMultipleStrongIdentifier(self):
		e = Entity("POSITION: _abscisse, _ordonnée")
		self.assertEqual([a.label for a in e.attributes], ["abscisse","ordonnée"])
		self.assertEqual([a.getCategory() for a in e.attributes], ["strong","strong"])
		e = Entity("POSITION: abscisse, _ordonnée")
		self.assertEqual([a.label for a in e.attributes], ["abscisse","ordonnée"])
		self.assertEqual([a.getCategory() for a in e.attributes], ["strong","strong"])
	
	def testMultipleWeakIdentifier(self):
		e = Entity("POSITION: -abscisse, -ordonnée")
		self.assertEqual([a.label for a in e.attributes], ["abscisse","ordonnée"])
		self.assertEqual([a.getCategory() for a in e.attributes], ["weak","weak"])

if __name__ == '__main__':
	unittest.main()