#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
sys.path[0:0] = ["."]

import unittest
from mocodo.association import *

import gettext
gettext.NullTranslations().install()

# Python 2.7 compatibility
if not hasattr(unittest.TestCase, "assertRaisesRegex"):
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

class parse_test(unittest.TestCase):
    
    def test_reflexive(self):
        a = Association(u"ÊTRE AMI, 0N BANDIT, 0N BANDIT")
        self.assertEqual(a.name, u"ÊTRE AMI")
        self.assertEqual(a.cartouche, u"ÊTRE AMI")
        self.assertEqual(a.attributes, [])
        for (i, leg) in enumerate(a.legs):
            self.assertEqual(leg.cardinalities, "0,N")
            self.assertEqual(leg.entity_name, "BANDIT")
            self.assertEqual(leg.arrow, "")
            self.assertEqual(leg.annotation, None)

    def test_double(self):
        l = [
            Association("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE"),
            Association("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE:"),
            Association("EMPLOYER,01 PARTICIPANT,0N ENTREPRISE"),
            Association(" EMPLOYER , 01 PARTICIPANT, 0N   ENTREPRISE "),
        ]
        for a in l:
            self.assertEqual(a.name, "EMPLOYER")
            self.assertEqual(a.cartouche, "EMPLOYER")
            self.assertEqual(a.attributes, [])
            self.assertEqual(a.legs[0].cardinalities, "0,1")
            self.assertEqual(a.legs[0].entity_name, "PARTICIPANT")
            self.assertEqual(a.legs[0].arrow, "")
            self.assertEqual(a.legs[0].annotation, None)
            self.assertEqual(a.legs[1].cardinalities, "0,N")
            self.assertEqual(a.legs[1].entity_name, "ENTREPRISE")
            self.assertEqual(a.legs[1].arrow, "")
            self.assertEqual(a.legs[1].annotation, None)

    def test_triple(self):
        a = Association("SUIVRE, 0N DATE, 11 ÉTUDIANT, 0N ENSEIGNANT")
        self.assertEqual(a.name, "SUIVRE")
        self.assertEqual(a.cartouche, "SUIVRE")
        self.assertEqual(a.attributes, [])
        self.assertEqual(a.legs[0].cardinalities, "0,N")
        self.assertEqual(a.legs[0].entity_name, "DATE")
        self.assertEqual(a.legs[0].arrow, "")
        self.assertEqual(a.legs[0].annotation, None)
        self.assertEqual(a.legs[1].cardinalities, "1,1")
        self.assertEqual(a.legs[1].entity_name, "ÉTUDIANT")
        self.assertEqual(a.legs[1].arrow, "")
        self.assertEqual(a.legs[1].annotation, None)
        self.assertEqual(a.legs[2].cardinalities, "0,N")
        self.assertEqual(a.legs[2].entity_name, "ENSEIGNANT")
        self.assertEqual(a.legs[2].arrow, "")
        self.assertEqual(a.legs[2].annotation, None)

    def test_arrow(self):
        a = Association("EMPLOYER, 01> PARTICIPANT, 0N< ENTREPRISE")
        self.assertEqual(a.legs[0].arrow, ">")
        self.assertEqual(a.legs[1].arrow, "<")
        self.assertEqual(a.legs[0].cardinalities, "0,1")
        self.assertEqual(a.legs[1].cardinalities, "0,N")

    def test_label(self):
        a = Association("ENGENDRER, 0N [Parent] PERSONNE, 1N [Enfant] PERSONNE")
        self.assertEqual(a.legs[0].annotation, "Parent")
        self.assertEqual(a.legs[1].annotation, "Enfant")
        self.assertEqual(a.legs[0].cardinalities, "0,N")
        self.assertEqual(a.legs[1].cardinalities, "1,N")

    def test_attributes(self):
        l = [
            Association("SOUTENIR, 01 ÉTUDIANT, 0N DATE: note stage, heure soutenance"),
            Association("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage , heure soutenance "),
            Association("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage,heure soutenance "),
        ]
        for a in l:
            self.assertEqual([att.label for att in a.attributes], ["note stage", "heure soutenance"])
            self.assertEqual([att.__class__ for att in a.attributes], [SimpleAssociationAttribute, SimpleAssociationAttribute])

    def test_other_card(self):
        a = Association("SOUTENIR, XX ÉTUDIANT, XX DATE: note stage")
        self.assertTrue(not a.legs[0].cardinalities.strip())
        self.assertTrue(not a.legs[1].cardinalities.strip())
        a = Association("SOUTENIR, XY ÉTUDIANT, XY DATE: note stage")
        self.assertEqual(a.legs[0].cardinalities, "X,Y")
        self.assertEqual(a.legs[1].cardinalities, "X,Y")

    def test_numbered_association(self):
        a = Association("SOUTENIR1, 01 ÉTUDIANT, 0N DATE: note stage")
        self.assertEqual(a.name, "SOUTENIR1")
        self.assertEqual(a.cartouche, "SOUTENIR")

    def test_df(self):
        a = Association("DF, 0N CLIENT, 11 COMMANDE")
        self.assertEqual(a.name, "DF")
        self.assertEqual(a.cartouche, "DF")
        a = Association("CIF, 0N CLIENT, 11 COMMANDE", {"df": u"CIF", "card_format": u"{min_card},{max_card}"})
        self.assertEqual(a.name, "CIF")
        self.assertEqual(a.cartouche, "CIF")

    def test_included_in_foreign_key(self):
        a = Association("SUIVRE, 0N DATE, 11 /ÉTUDIANT, 0N ENSEIGNANT")
        self.assertEqual(a.legs[0].entity_name, "DATE")
        self.assertEqual(a.legs[0].may_identify, True)
        self.assertEqual(a.legs[1].entity_name, "ÉTUDIANT")
        self.assertEqual(a.legs[1].may_identify, False)
        self.assertEqual(a.legs[2].entity_name, "ENSEIGNANT")
        self.assertEqual(a.legs[2].may_identify, True)

    def test_input_errors(self):
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.2", Association, "EMPLOYER, PARTICIPANT, 0N ENTREPRISE",)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.2", Association, "EMPLOYER, 1 PARTICIPANT, 0N ENTREPRISE",)

if __name__ == '__main__':
    unittest.main()
