#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
sys.path[0:0] = ["."]

import unittest
from mocodo.entity import *

class EntityTest(unittest.TestCase):

    def test_default(self):
        entities = [
            Entity("PARTICIPANT: numero, nom, adresse"),
            Entity("PARTICIPANT:numero,nom,adresse"),
            Entity(" PARTICIPANT: numero, nom, adresse "),
            Entity("PARTICIPANT :numero ,nom ,adresse"),
        ]
        for e in entities:
            e.set_strengthen_legs([])
            self.assertEqual(e.name, "PARTICIPANT")
            self.assertEqual(e.cartouche, "PARTICIPANT")
            self.assertEqual([a.label for a in e.attributes], ["numero", "nom", "adresse"])
            self.assertEqual([a.get_category() for a in e.attributes], ["strong", "simple", "simple"])

    def test_data_types(self):
        e = Entity("PARTICIPANT: numero [type1], nom [type2] , adresse[type3]")
        e.set_strengthen_legs([])
        self.assertEqual([a.label for a in e.attributes], ["numero", "nom", "adresse"])
        self.assertEqual([a.data_type for a in e.attributes], ["type1", "type2", "type3"])
        e = Entity("PARTICIPANT: numero [type a,b,c], nom [type2], adresse [type3]")
        e.set_strengthen_legs([])
        self.assertEqual([a.data_type for a in e.attributes], ["type a,b,c", "type2", "type3"])
        e = Entity("PARTICIPANT: numero [], nom, adresse [type3]")
        e.set_strengthen_legs([])
        self.assertEqual([a.data_type for a in e.attributes], ["", None, "type3"])
        e = Entity("PARTICIPANT: numero [, nom, adresse")
        e.set_strengthen_legs([])
        self.assertEqual([a.data_type for a in e.attributes], [None, None, None])

    def test_numbered_entity(self):
        e = Entity("PARTICIPANT5: numero, nom, adresse")
        e.set_strengthen_legs([])
        self.assertEqual(e.name, "PARTICIPANT5")
        self.assertEqual(e.cartouche, "PARTICIPANT")

    def test_blank(self):
        e = Entity("MOT-CLEF: mot-clef, ,")
        e.set_strengthen_legs([])
        self.assertEqual([a.label for a in e.attributes], ["mot-clef", "", ""])
        self.assertEqual([a.get_category() for a in e.attributes], ["strong", "phantom", "phantom"])

    def test_all_blank(self):
        e = Entity("BLANK: , ,")
        e.set_strengthen_legs([])
        self.assertEqual([a.label for a in e.attributes], ["", "", ""])
        self.assertEqual([a.get_category() for a in e.attributes], ["phantom", "phantom", "phantom"])

    def test_no_identifier_at_first_position(self):
        e = Entity("POSITION: _abscisse, ordonnee")
        e.set_strengthen_legs([])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.get_category() for a in e.attributes], ["simple", "simple"])

    def test_multiple_strong_identifier(self):
        e = Entity("POSITION: abscisse, _ordonnee")
        e.set_strengthen_legs([])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.get_category() for a in e.attributes], ["strong", "strong"])

    def test_weak_identifier(self):
        e = Entity("LIVRE: Num. exemplaire, Etat du livre, Date d'achat")
        e.set_strengthen_legs([None])
        self.assertEqual([a.label for a in e.attributes], ["Num. exemplaire", "Etat du livre", "Date d'achat"])
        self.assertEqual([a.get_category() for a in e.attributes], ["weak", "simple", "simple"])

    def test_weak_composite_identifier(self):
        e = Entity("POSITION: abscisse, _ordonnee, foobar")
        e.set_strengthen_legs([None])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee", "foobar"])
        self.assertEqual([a.get_category() for a in e.attributes], ["weak", "weak", "simple"])

if __name__ == '__main__':
    unittest.main()
