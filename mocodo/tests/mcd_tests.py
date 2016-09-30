#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
sys.path[0:0] = ["."]

import unittest
from mocodo.mcd import *
from mocodo.argument_parser import parsed_arguments

import gettext
gettext.NullTranslations().install()

params = parsed_arguments()

import os

# Python 2.7 compatibility
if not hasattr(unittest.TestCase, "assertRaisesRegex"):
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

class McdTest(unittest.TestCase):

    def test_entity_recognition(self):
        clauses = [
            u"PROJET: num. projet, nom projet, budget projet",
            u"PROJET ABC: num. projet, nom projet, budget projet",
            u"PROJET CDE:",
        ]
        mcd = Mcd(clauses, params)
        self.assertEqual(mcd.box_count, len(clauses))
        for box in mcd.boxes:
            self.assertEqual(box.kind, "entity")

    def test_association_recognition(self):
        entities = [u"FONCTION:", u"DÉPARTEMENT:", u"EMPLOYÉ:", u"PERSONNE:",
                    u"ÉTUDIANT:", u"DATE:", u"CLIENT:", u"COMMANDE:", u"BANDIT:", u"EMPLOYÉ ABC:"]
        associations = [
            u"ASSUMER, 1N EMPLOYÉ, 1N FONCTION: date début, date fin",
            u"DIRIGER, 11 DÉPARTEMENT, 01 EMPLOYÉ",
            u"ENGENDRER, 0N [Parent] PERSONNE, 1N [Enfant] PERSONNE",
            u"SOUTENIR, XX ÉTUDIANT, XX DATE: note stage",
            u"DF, 0N CLIENT, 11 COMMANDE",
            u"DF2, 0N CLIENT, 11 COMMANDE",
            u"ÊTRE AMI, 0N BANDIT, 0N BANDIT",
            u"ASSURER2, 1N EMPLOYÉ ABC, 1N FONCTION: date début, date fin",
        ]
        clauses = entities + associations
        mcd = Mcd(clauses, params)
        self.assertEqual(mcd.box_count, len(clauses))
        for box in mcd.boxes:
            self.assertEqual(box.kind, "entity" if box.name + ":" in entities else "association")

    def test_rows(self):
        clauses = u"""
            BARATTE: piston, racloir, fusil
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
        mcd = Mcd(clauses, params)
        self.assertEqual([element.name for element in mcd.rows[0]], [u"BARATTE", u"MARTEAU", u"TINET", u"CROCHET"])
        self.assertEqual([element.name for element in mcd.rows[1]], [u"DF", u"BALANCE", u"BANNETON", u"PORTE"])
        self.assertEqual([element.name for element in mcd.rows[2]], [u" 0", u"ROULEAU", u"HERSE", u" 1"])
        self.assertEqual([element.name for element in mcd.rows[3]], [u" 2", u"FLÉAU", u" 3", u" 4"])

    def test_layout(self):
        clauses = [
            u"BARATTE: piston, racloir, fusil",
            u"MARTEAU, 0N BARATTE, 11 TINET: ciseaux",
            u"TINET: fendoir, grattoir",
            u"CROCHET: égrenoir, _gorgeoir, bouillie",
            u"",
            u"DF, 11 BARATTE, 1N ROULEAU",
            u"BALANCE, 0N ROULEAU, 0N TINET: charrue",
            u"BANNETON, 01 CROCHET, 11 FLÉAU, 1N TINET: pulvérisateur",
            u"PORTE, 11 CROCHET, 0N CROCHET",
            u"",
            u"ROULEAU: tribulum",
            u"HERSE, 1N FLÉAU, 1N FLÉAU",
            u"",
            u"FLÉAU: battadère, van, mesure",
        ]
        mcd = Mcd(clauses, params)
        self.assertEqual(mcd.get_layout(), list(range(16)))
        self.assertEqual(mcd.get_layout_data(), {
            'col_count': 4,
            'row_count': 4,
            'links': (
                (0, 1), # from BARATTE to MARTEAU
                (0, 4), # from BARATTE to DF
                (1, 2),
                (2, 5),
                (2, 6),
                (3, 6),
                (3, 7),
                (4, 9),
                (5, 9),
                (6, 13),
                (10, 13)
            ),
            'multiplicity': {
                (0, 1): 1,
                (0, 4): 1,
                (1, 0): 1,
                (1, 2): 1,
                (2, 1): 1,
                (2, 5): 1,
                (2, 6): 1,
                (3, 6): 1,
                (3, 7): 2, # 2 links between CROCHET and PORTE
                (4, 0): 1,
                (4, 9): 1,
                (5, 2): 1,
                (5, 9): 1,
                (6, 2): 1,
                (6, 3): 1,
                (6, 13): 1,
                (7, 3): 2, # 2 links between PORTE and CROCHET
                (9, 4): 1,
                (9, 5): 1,
                (10, 13): 2,
                (13, 6): 1,
                (13, 10): 2
            },
            'successors': [
                {1, 4}, # BARATTE has MARTEAU and DF as successors
                {0, 2},
                {1, 5, 6},
                {6, 7},
                {0, 9},
                {2, 9},
                {2, 3, 13},
                {3}, # reflexive association PORTE: no multiple edges
                set(), # phantom
                {4, 5},
                {13},
                set(),
                set(),
                {6, 10},
                set(),
                set()]
            }
        )
        expected = u"""
            BARATTE: piston, racloir, fusil
            MARTEAU, 0N BARATTE, 11 TINET: ciseaux
            TINET: fendoir, grattoir
            CROCHET: égrenoir, _gorgeoir, bouillie

            DF, 11 BARATTE, 1N ROULEAU
            BALANCE, 0N ROULEAU, 0N TINET: charrue
            BANNETON, 01 CROCHET, 11 FLÉAU, 1N TINET: pulvérisateur
            PORTE, 11 CROCHET, 0N CROCHET

            :
            ROULEAU: tribulum
            HERSE, 1N FLÉAU, 1N FLÉAU
            :

            :
            FLÉAU: battadère, van, mesure
            ::
        """.strip().replace("  ", "")
        mcd.set_layout(list(range(16)))
        self.assertEqual(mcd.get_clauses(), expected)


    def test_input_errors(self):
        clauses = [
            u"PROJET: num. projet, nom projet, budget projet",
            u"ASSUMER, 1N PROJET, 1N INDIVIDU",
        ]
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.1", Mcd, clauses, params)

    def test_duplicate_errors(self):
        clauses = [
            u"DF, 11 BARATTE, 1N ROULEAU",
            u"BARATTE: piston, racloir, fusil",
            u"TINET: fendoir, grattoir",
            u"BALANCE, 0N ROULEAU, 0N TINET: charrue",
            u"BARATTE: tribulum",
        ]
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.6", Mcd, clauses, params)
        clauses = [
            u"DF, 11 BARATTE, 1N ROULEAU",
            u"BARATTE: piston, racloir, fusil",
            u"TINET: fendoir, grattoir",
            u"DF, 0N ROULEAU, 0N TINET: charrue",
            u"ROULEAU: tribulum",
        ]
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.7", Mcd, clauses, params)
        clauses = [
            u"BARATTE, 11 BARATTE, 1N ROULEAU",
            u"BARATTE: piston, racloir, fusil",
            u"TINET: fendoir, grattoir",
            u"BALANCE, 0N ROULEAU, 0N TINET: charrue",
            u"ROULEAU: tribulum",
        ]
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.8", Mcd, clauses, params)
        clauses = [
            u"BARATTE: piston, racloir, fusil",
            u"BARATTE, 11 BARATTE, 1N ROULEAU",
            u"TINET: fendoir, grattoir",
            u"BALANCE, 0N ROULEAU, 0N TINET: charrue",
            u"ROULEAU: tribulum",
        ]
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.8", Mcd, clauses, params)

    def test_flip(self):
        clauses = u"""
            BARATTE: piston, racloir, fusil
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
        mcd = Mcd(clauses, params)
        expected = u"""
            :
            FLÉAU: battadère, van, mesure
            ::

            :
            ROULEAU: tribulum
            HERSE, 1N FLÉAU, 1N FLÉAU
            :

            DF, 11 BARATTE, 1N ROULEAU
            BALANCE, 0N ROULEAU, 0N TINET: charrue
            BANNETON, 01 CROCHET, 11 FLÉAU, 1N TINET: pulvérisateur
            PORTE, 11 CROCHET, 0N CROCHET

            BARATTE: piston, racloir, fusil
            MARTEAU, 0N BARATTE, 11 TINET: ciseaux
            TINET: fendoir, grattoir
            CROCHET: égrenoir, _gorgeoir, bouillie
        """.strip().replace("  ", "")
        self.assertEqual(mcd.get_clauses_horizontal_mirror(), expected)
        expected = u"""
            CROCHET: égrenoir, _gorgeoir, bouillie
            TINET: fendoir, grattoir
            MARTEAU, 0N BARATTE, 11 TINET: ciseaux
            BARATTE: piston, racloir, fusil

            PORTE, 11 CROCHET, 0N CROCHET
            BANNETON, 01 CROCHET, 11 FLÉAU, 1N TINET: pulvérisateur
            BALANCE, 0N ROULEAU, 0N TINET: charrue
            DF, 11 BARATTE, 1N ROULEAU

            :
            HERSE, 1N FLÉAU, 1N FLÉAU
            ROULEAU: tribulum
            :

            ::
            FLÉAU: battadère, van, mesure
            :
        """.strip().replace("  ", "")
        self.assertEqual(mcd.get_clauses_vertical_mirror(), expected)
        expected = u"""
            BARATTE: piston, racloir, fusil
            DF, 11 BARATTE, 1N ROULEAU
            ::

            MARTEAU, 0N BARATTE, 11 TINET: ciseaux
            BALANCE, 0N ROULEAU, 0N TINET: charrue
            ROULEAU: tribulum
            FLÉAU: battadère, van, mesure

            TINET: fendoir, grattoir
            BANNETON, 01 CROCHET, 11 FLÉAU, 1N TINET: pulvérisateur
            HERSE, 1N FLÉAU, 1N FLÉAU
            :

            CROCHET: égrenoir, _gorgeoir, bouillie
            PORTE, 11 CROCHET, 0N CROCHET
            ::
        """.strip().replace("  ", "")
        self.assertEqual(mcd.get_clauses_diagonal_mirror(), expected)

    def test_explicit_fit(self):
        # initially: (5, 4) for 11 nodes
        clauses = u"""
            Item: Norm, Wash, Haul
            Milk, 0N Item, 0N Draw

            Draw: Lady, Face, Soon, Dish, Ever
            Unit, 1N Draw, 11 Folk: Peer, Tour, 

            Folk: Hall, Fold, Baby, Bind, Gene, Aids, Free
            Pack, 1N Folk, 1N Seem 
            Seem: Teen, Amid
            Disk, 0N Flip, 1N Seem
            Flip : Gold, Ride

            Call: Ride, Soon
            Gear , 1N Call, 1N Folk
        """.split("\n")
        mcd = Mcd(clauses, params)
        # minimal fit: (4, 3)
        expected = u"""
            Item: Norm, Wash, Haul
            Milk, 0N Item, 0N Draw
            Draw: Lady, Face, Soon, Dish, Ever
            Unit, 1N Draw, 11 Folk: Peer, Tour,

            Folk: Hall, Fold, Baby, Bind, Gene, Aids, Free
            Pack, 1N Folk, 1N Seem
            Seem: Teen, Amid
            Disk, 0N Flip, 1N Seem

            Flip : Gold, Ride
            Call: Ride, Soon
            Gear , 1N Call, 1N Folk
            :
        """.strip().replace("  ", "")
        self.assertEqual(mcd.get_reformatted_clauses(0), expected)
        # 1st next fit: (5, 3)
        expected = u"""
            Item: Norm, Wash, Haul
            Milk, 0N Item, 0N Draw
            Draw: Lady, Face, Soon, Dish, Ever
            Unit, 1N Draw, 11 Folk: Peer, Tour,
            Folk: Hall, Fold, Baby, Bind, Gene, Aids, Free

            Pack, 1N Folk, 1N Seem
            Seem: Teen, Amid
            Disk, 0N Flip, 1N Seem
            Flip : Gold, Ride
            Call: Ride, Soon

            Gear , 1N Call, 1N Folk
            ::::
        """.strip().replace("  ", "")
        self.assertEqual(mcd.get_reformatted_clauses(1), expected)
        # 2nd next fit: (4, 4)
        expected = u"""
            Item: Norm, Wash, Haul
            Milk, 0N Item, 0N Draw
            Draw: Lady, Face, Soon, Dish, Ever
            Unit, 1N Draw, 11 Folk: Peer, Tour,

            Folk: Hall, Fold, Baby, Bind, Gene, Aids, Free
            Pack, 1N Folk, 1N Seem
            Seem: Teen, Amid
            Disk, 0N Flip, 1N Seem

            Flip : Gold, Ride
            Call: Ride, Soon
            Gear , 1N Call, 1N Folk
            :

            ::::
        """.strip().replace("  ", "")
        self.assertEqual(mcd.get_reformatted_clauses(2), expected)
        
    def test_automatic_fit_produces_next_grid(self):
        # initially: (5, 4) for 11 nodes
        clauses = u"""
            Item: Norm, Wash, Haul
            Milk, 0N Item, 0N Draw

            Draw: Lady, Face, Soon, Dish, Ever
            Unit, 1N Draw, 11 Folk: Peer, Tour, 

            Folk: Hall, Fold, Baby, Bind, Gene, Aids, Free
            Pack, 1N Folk, 1N Seem 
            Seem: Teen, Amid
            Disk, 0N Flip, 1N Seem
            Flip : Gold, Ride

            Call: Ride, Soon
            Gear , 1N Call, 1N Folk
        """.split("\n")
        mcd = Mcd(clauses, params)
        # (5, 4) being a preferred grid, the next one (6, 4) is generated
        expected = u"""
            Item: Norm, Wash, Haul
            Milk, 0N Item, 0N Draw
            Draw: Lady, Face, Soon, Dish, Ever
            Unit, 1N Draw, 11 Folk: Peer, Tour,
            Folk: Hall, Fold, Baby, Bind, Gene, Aids, Free
            Pack, 1N Folk, 1N Seem

            Seem: Teen, Amid
            Disk, 0N Flip, 1N Seem
            Flip : Gold, Ride
            Call: Ride, Soon
            Gear , 1N Call, 1N Folk
            :

            ::::::

            ::::::
        """.strip().replace("  ", "")
        self.assertEqual(mcd.get_reformatted_clauses(-1), expected)

    def test_implicit_fit_produces_min_grid_next(self):
        # initially: (4, 5) for 11 nodes
        clauses = u"""
            Item: Norm, Wash, Haul
            Milk, 0N Item, 0N Draw

            Draw: Lady, Face, Soon, Dish, Ever
            Unit, 1N Draw, 11 Folk: Peer, Tour, 

            Folk: Hall, Fold, Baby, Bind, Gene, Aids, Free

            Pack, 1N Folk, 1N Seem
            Seem: Teen, Amid
            Disk, 0N Flip, 1N Seem
            Flip : Gold, Ride

            Call: Ride, Soon
            Gear , 1N Call, 1N Folk
        """.split("\n")
        mcd = Mcd(clauses, params)
        # (4, 5) not being a preferred grid, it is equivalent to nth_fit == 1
        expected = u"""
            Item: Norm, Wash, Haul
            Milk, 0N Item, 0N Draw
            Draw: Lady, Face, Soon, Dish, Ever
            Unit, 1N Draw, 11 Folk: Peer, Tour,
            Folk: Hall, Fold, Baby, Bind, Gene, Aids, Free

            Pack, 1N Folk, 1N Seem
            Seem: Teen, Amid
            Disk, 0N Flip, 1N Seem
            Flip : Gold, Ride
            Call: Ride, Soon

            Gear , 1N Call, 1N Folk
            ::::
        """.strip().replace("  ", "")
        self.assertEqual(mcd.get_reformatted_clauses(-1), expected)
        self.assertEqual(mcd.get_reformatted_clauses(1), expected)


if __name__ == '__main__':
    unittest.main()
