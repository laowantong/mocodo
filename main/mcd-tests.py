#!/usr/bin/env python
# encoding: utf-8

import unittest
from mcd import *

import gettext
gettext.NullTranslations().install()

params = {
	"df": u"DF",
	"sep": u",",
}

import os
os.chdir("..")

class McdTest(unittest.TestCase):
	
	def testEntityRecognition(self):
		clauses = [
			u"PROJET: num. projet, nom projet, budget projet",
			u"PROJET ABC: num. projet, nom projet, budget projet",
			u"PROJET CDE:",
		]
		mcd = Mcd(clauses,params)
		self.assertEqual(len(mcd.elements),len(clauses))
		for element in mcd.elements.values():
			self.assertEqual(element.__class__, Entity)
	
	def testAssociationRecognition(self):
		entities = [u"FONCTION:", u"DÉPARTEMENT:", u"EMPLOYÉ:", u"PERSONNE:", u"ÉTUDIANT:", u"DATE:", u"CLIENT:", u"COMMANDE:", u"BANDIT:", u"EMPLOYÉ ABC:"]
		associations = [
			u"ASSUMER, 1N EMPLOYÉ, 1N FONCTION: date début, date fin",
			u"DIRIGER, 11 DÉPARTEMENT, 01 EMPLOYÉ",
			u"ENGENDRER, 0NParent PERSONNE, 1NEnfant PERSONNE",
			u"SOUTENIR, XX ÉTUDIANT, XX DATE: note stage",
			u"DF, 0N CLIENT, 11 COMMANDE",
			u"DF2, 0N CLIENT, 11 COMMANDE",
			u"ÊTRE AMI, 0N BANDIT, 0N BANDIT",
			u"ASSURER2, 1N EMPLOYÉ ABC, 1N FONCTION: date début, date fin",
		]
		clauses = entities + associations
		mcd = Mcd(clauses,params)
		self.assertEqual(len(mcd.elements),len(clauses))
		for element in mcd.elements.values():
			if element.name+":" not in entities:
				self.assertEqual(element.__class__, Association)
	
	def testOrdering(self):
		clauses = u"""
			BARATTE: -piston, racloir, fusil
			MARTEAU, 0N BARATTE, 11 TINET: ciseaux
			TINET: fendoir, grattoir
			CROCHET: égrenoir, _gorgeoir, bouillie
			
			DF, 11 BARATTE, 1N ROULEAU
			BALANCE, 0N ROULEAU, 0N TINET: charrue
			BANNETON, 01 CROCHET, 11 FLÉAU, 1N TINET: pulvérisateur
			PORTE, 11 CROCHET, 0N CROCHET
			
			ROULEAU: tribulum
			HERSE, 1N FLÉAU, 1N FLÉAU
			
			FLÉAU: battadère, van, mesure
		""".split("\n")
		mcd = Mcd(clauses,params)
		self.assertEqual([element.name for element in mcd.ordering[0]],[u"BARATTE", u"MARTEAU", u"TINET", u"CROCHET"])
		self.assertEqual([element.name for element in mcd.ordering[1]],[u"DF", u"BALANCE", u"BANNETON", u"PORTE"])
		self.assertEqual([element.name for element in mcd.ordering[2]],[u"ROULEAU", u"HERSE"])
		self.assertEqual([element.name for element in mcd.ordering[3]],[u"FLÉAU"])
	
	def testInputErrors(self):
		clauses = [
			u"PROJET: num. projet, nom projet, budget projet",
			u"ASSUMER, 1N PROJET, 1N INDIVIDU",
		]
		self.assertRaisesRegexp(RuntimeError,"Mocodo Err.1",Mcd,clauses,params)
	

class AttractTest(unittest.TestCase):
	
	def setUp(self):
		self.l = [
			[49,145,268,373],
			[38,134,247,352],
			[55,171,278,377],
		]
	
	def testNoAttraction(self):
		attract(self.l,0)
		expected = [
			[49,145,268,373],
			[38,134,247,352],
			[55,171,278,377],
		]
		self.assertEqual(self.l,expected)
	
	def testTooWeakAttraction(self):
		attract(self.l,3)
		expected = [
			[49,145,268,373],
			[38,134,247,352],
			[55,171,278,377],
		]
		self.assertEqual(self.l,expected)
	
	def testWeakAttraction(self):
		attract(self.l,5)
		expected = [
			[49,145,268,377],
			[38,134,247,352],
			[55,171,278,377],
		]
		self.assertEqual(self.l,expected)
	
	def testNormalAttraction(self):
		attract(self.l,50)
		expected = [
			[55, 171, 294, 399],
			[55, 171, 294, 399],
			[55, 171, 294, 399],
		]
		self.assertEqual(self.l,expected)
	
	def testTooStrongAttraction(self):
		attract(self.l,500)
		expected = [
			[55, 171, 294, 399],
			[55, 171, 294, 399],
			[55, 171, 294, 399],
		]
		self.assertEqual(self.l,expected)
	


if __name__ == '__main__':
	unittest.main()