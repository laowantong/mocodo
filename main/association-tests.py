#!/usr/bin/env python
# encoding: utf-8

import unittest
from association import *

class parseTest(unittest.TestCase):
	
	def testReflexive(self):
		a = Association(u"ÊTRE AMI, 0N BANDIT, 0N BANDIT")
		self.assertEqual(a.name,u"ÊTRE AMI")
		self.assertEqual(a.cartouche,u"ÊTRE AMI")
		self.assertEqual(a.attributes,[])
		for (i,leg) in enumerate(a.legs):
			leg.setCardSep(",")
			self.assertEqual(leg.cardinalities,"0,N")
			self.assertEqual(leg.entityName,"BANDIT")
			self.assertEqual(leg.arrow,"")
			self.assertEqual(leg.label,"")
			self.assertEqual(leg.__class__,CurvedLeg)
			self.assertEqual(leg.count,2)
			self.assertEqual(leg.num,i)
	
	def testDouble(self):
		l = [
			Association("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE"),
			Association("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE:"),
			Association("EMPLOYER,01 PARTICIPANT,0N ENTREPRISE"),
			Association(" EMPLOYER , 01 PARTICIPANT, 0N   ENTREPRISE "),
		]
		for a in l:
			self.assertEqual(a.name,"EMPLOYER")
			self.assertEqual(a.cartouche,"EMPLOYER")
			self.assertEqual(a.attributes,[])
			a.legs[0].setCardSep(",")
			self.assertEqual(a.legs[0].cardinalities,"0,1")
			self.assertEqual(a.legs[0].entityName,"PARTICIPANT")
			self.assertEqual(a.legs[0].arrow,"")
			self.assertEqual(a.legs[0].label,"")
			self.assertEqual(a.legs[0].__class__,StraightLeg)
			a.legs[1].setCardSep(",")
			self.assertEqual(a.legs[1].cardinalities,"0,N")
			self.assertEqual(a.legs[1].entityName,"ENTREPRISE")
			self.assertEqual(a.legs[1].arrow,"")
			self.assertEqual(a.legs[1].label,"")
			self.assertEqual(a.legs[1].__class__,StraightLeg)
	
	def testTriple(self):
		a = Association("SUIVRE, 0N DATE, 11 ÉTUDIANT, 0N ENSEIGNANT")
		self.assertEqual(a.name,"SUIVRE")
		self.assertEqual(a.cartouche,"SUIVRE")
		self.assertEqual(a.attributes,[])
		a.legs[0].setCardSep(",")
		self.assertEqual(a.legs[0].cardinalities,"0,N")
		self.assertEqual(a.legs[0].entityName,"DATE")
		self.assertEqual(a.legs[0].arrow,"")
		self.assertEqual(a.legs[0].label,"")
		self.assertEqual(a.legs[0].__class__,StraightLeg)
		a.legs[1].setCardSep(",")
		self.assertEqual(a.legs[1].cardinalities,"1,1")
		self.assertEqual(a.legs[1].entityName,"ÉTUDIANT")
		self.assertEqual(a.legs[1].arrow,"")
		self.assertEqual(a.legs[1].label,"")
		self.assertEqual(a.legs[1].__class__,StraightLeg)
		a.legs[2].setCardSep(",")
		self.assertEqual(a.legs[2].cardinalities,"0,N")
		self.assertEqual(a.legs[2].entityName,"ENSEIGNANT")
		self.assertEqual(a.legs[2].arrow,"")
		self.assertEqual(a.legs[2].label,"")
		self.assertEqual(a.legs[2].__class__,StraightLeg)
	
	def testArrow(self):
		a = Association("EMPLOYER, 01> PARTICIPANT, 0N< ENTREPRISE")
		a.legs[0].setCardSep(",")
		a.legs[1].setCardSep(",")
		self.assertEqual(a.legs[0].arrow,">")
		self.assertEqual(a.legs[1].arrow,"<")
		self.assertEqual(a.legs[0].cardinalities,"0,1")
		self.assertEqual(a.legs[1].cardinalities,"0,N")
	
	def testLabel(self):
		a = Association("ENGENDRER, 0NParent PERSONNE, 1NEnfant PERSONNE")
		a.legs[0].setCardSep(",")
		a.legs[1].setCardSep(",")
		self.assertEqual(a.legs[0].label,"Parent")
		self.assertEqual(a.legs[1].label,"Enfant")
		self.assertEqual(a.legs[0].cardinalities,"0,N")
		self.assertEqual(a.legs[1].cardinalities,"1,N")
	
	def testAttributes(self):
		l = [
			Association("SOUTENIR, 01 ÉTUDIANT, 0N DATE: note stage, heure soutenance"),
			Association("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage , heure soutenance "),
			Association("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage,heure soutenance "),
		]
		for a in l:
			self.assertEqual([att.label for att in a.attributes], ["note stage", "heure soutenance"])
			self.assertEqual([att.__class__ for att in a.attributes], [SimpleAssociationAttribute,SimpleAssociationAttribute])
	
	def testOtherCard(self):
		a = Association("SOUTENIR, XX ÉTUDIANT, XX DATE: note stage")
		a.legs[0].setCardSep(",")
		a.legs[1].setCardSep(",")
		self.assertEqual(a.legs[0].cardinalities,"")
		self.assertEqual(a.legs[1].cardinalities,"")
		a = Association("SOUTENIR, XY ÉTUDIANT, XY DATE: note stage")
		a.legs[0].setCardSep(",")
		a.legs[1].setCardSep(",")
		self.assertEqual(a.legs[0].cardinalities,"X,Y")
		self.assertEqual(a.legs[1].cardinalities,"X,Y")
	
	def testNumberedAssociation(self):
		a = Association("SOUTENIR1, 01 ÉTUDIANT, 0N DATE: note stage")
		self.assertEqual(a.name,"SOUTENIR1")
		self.assertEqual(a.cartouche,"SOUTENIR")
	
	def testDF(self):
		a = Association("DF, 0N CLIENT, 11 COMMANDE")
		self.assertEqual(a.name,"DF")
		self.assertEqual(a.cartouche,"DF")
		a = Association("CIF, 0N CLIENT, 11 COMMANDE",{"df": u"CIF"})
		self.assertEqual(a.name,"CIF")
		self.assertEqual(a.cartouche,"CIF")
	
	def testIncludedInForeignKey(self):
		a = Association("SUIVRE, 0N DATE, 11 /ÉTUDIANT, 0N ENSEIGNANT")
		a.legs[0].setCardSep(",")
		self.assertEqual(a.legs[0].entityName,"DATE")
		self.assertEqual(a.legs[0].mayIdentify,True)
		a.legs[1].setCardSep(",")
		self.assertEqual(a.legs[1].entityName,"ÉTUDIANT")
		self.assertEqual(a.legs[1].mayIdentify,False)
		a.legs[2].setCardSep(",")
		self.assertEqual(a.legs[2].entityName,"ENSEIGNANT")
		self.assertEqual(a.legs[2].mayIdentify,True)
	

if __name__ == '__main__':
	unittest.main()