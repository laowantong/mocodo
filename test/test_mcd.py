import gettext
import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.argument_parser import parsed_arguments
from mocodo.mcd import *


gettext.NullTranslations().install()

params = parsed_arguments([])

class McdTest(unittest.TestCase):

    def test_entity_recognition(self):
        clauses = [
            "PROJET: num. projet, nom projet, budget projet",
            "PROJET ABC: num. projet, nom projet, budget projet",
            "PROJET CDE:",
        ]
        mcd = Mcd("\n".join(clauses), **params)
        self.assertEqual(mcd.box_count, len(clauses))
        for box in mcd.boxes:
            self.assertEqual(box.kind, "entity")

    def test_association_recognition(self):
        entities = ["FONCTION:", "DEPARTEMENT:", "EMPLOYE:", "PERSONNE:",
                    "ETUDIANT:", "DATE:", "CLIENT:", "COMMANDE:", "BANDIT:", "EMPLOYE_ABC:"]
        associations = [
            "ASSUMER, 1N EMPLOYÉ, 1N FONCTION: date début, date fin",
            "DIRIGER, 11 DÉPARTEMENT, 01 EMPLOYÉ",
            "ENGENDRER, 0N [Parent] PERSONNE, 1N [Enfant] PERSONNE",
            "SOUTENIR, XX ÉTUDIANT, XX DATE: note stage",
            "DF, 0N CLIENT, 11 COMMANDE",
            "ÊTRE AMI, 0N BANDIT, 0N BANDIT",
            "ASSURER2, 1N EMPLOYÉ ABC, 1N FONCTION: date début, date fin",
        ]
        clauses = entities + associations
        mcd = Mcd("\n".join(clauses), **params)
        self.assertEqual(mcd.box_count, len(clauses))
        for box in mcd.boxes:
            if box.bid + ":" in entities:
                self.assertEqual(box.kind, "entity")
            else:
                self.assertIn(box.kind, ["association", "df"])

    def test_constraint_recognition(self):
        clauses = [
            "Lorem: lorem, ipsum",
            "Ipsum, XX Lorem, XX Dolor",
            "Dolor: dolor, sit",
            "Sit, XX Dolor, XX Amet",
            "Amet: consectetur, adipiscing",
            "(A) --Lorem, ..Ipsum, Dolor: 30, 90",
            "(B) ->Dolor, <-->Sit, -->Amet: 69, 90",
        ]
        mcd = Mcd("\n".join(clauses), **params)
        self.assertEqual(mcd.box_count, len(clauses) - 2)
        self.assertEqual(len(mcd.constraints), 2)
        for constraint in mcd.constraints:
            self.assertEqual(constraint.kind, "constraint")


    def test_rows(self):
        source = """
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
        """
        mcd = Mcd(source, **params)
        self.assertEqual([element.bid for element in mcd.rows[0]], ["BARATTE", "MARTEAU", "TINET", "CROCHET"])
        self.assertEqual([element.bid for element in mcd.rows[1]], ["DF0", "BALANCE", "BANNETON", "PORTE"])
        self.assertEqual([element.bid for element in mcd.rows[2]], ['PHANTOM_#1', 'ROULEAU', 'HERSE', 'PHANTOM_#2'])
        self.assertEqual([element.bid for element in mcd.rows[3]], ['PHANTOM_#3', 'FLEAU', 'PHANTOM_#4', 'PHANTOM_#5'])

    def test_layout(self):
        clauses = [
            "BARATTE: piston, racloir, fusil",
            "MARTEAU, 0N BARATTE, 11 TINET: ciseaux",
            "TINET: fendoir, grattoir",
            "CROCHET: égrenoir, _gorgeoir, bouillie",
            "",
            "DF, 11 BARATTE, 1N ROULEAU",
            "BALANCE, 0N ROULEAU, 0N TINET: charrue",
            "BANNETON, 01 CROCHET, 11 FLÉAU, 1N TINET: pulvérisateur",
            "PORTE, 11 CROCHET, 0N CROCHET",
            "",
            "ROULEAU: tribulum",
            "HERSE, 1N FLÉAU, 1N FLÉAU",
            "",
            "FLÉAU: battadère, van, mesure",
        ]
        mcd = Mcd("\n".join(clauses), **params)
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
        expected = """
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
            :
            :
        """.strip().replace("  ", "")
        mcd.set_layout(list(range(16)))
        self.assertEqual(mcd.get_clauses(), expected)


    def test_input_errors(self):
        clauses = [
            "PROJET: num. projet, nom projet, budget projet",
            "ASSUMER, 1N PROJET, 1N INDIVIDU",
        ]
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.1", Mcd, "\n".join(clauses), params)

    def test_duplicate_errors(self):
        clauses = [
            "DF, 11 BARATTE, 1N ROULEAU",
            "BARATTE: piston, racloir, fusil",
            "TINET: fendoir, grattoir",
            "BALANCE, 0N ROULEAU, 0N TINET: charrue",
            "BARATTE: tribulum",
        ]
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.6", Mcd, "\n".join(clauses), params)
        clauses = [
            "BARATTE, 11 BARATTE, 1N ROULEAU",
            "BARATTE: piston, racloir, fusil",
            "TINET: fendoir, grattoir",
            "BALANCE, 0N ROULEAU, 0N TINET: charrue",
            "ROULEAU: tribulum",
        ]
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.8", Mcd, "\n".join(clauses), params)
        clauses = [
            "BARATTE: piston, racloir, fusil",
            "BARATTE, 11 BARATTE, 1N ROULEAU",
            "TINET: fendoir, grattoir",
            "BALANCE, 0N ROULEAU, 0N TINET: charrue",
            "ROULEAU: tribulum",
        ]
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.8", Mcd, "\n".join(clauses), params)

    def test_constraint_errors(self):
        clauses = [
            "Lorem: lorem, ipsum",
            "Ipsum, XX Lorem, XX Lorem",
            "(A) --Lorem, ..Ipsum, Dolor: 30, 90",
        ]
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.40", Mcd, "\n".join(clauses), params)

    def test_flip(self):
        source = """
            % The comments are placed before
            BARATTE: piston, racloir, fusil
            MARTEAU, 0N BARATTE, 11 TINET: ciseaux
            TINET: fendoir, grattoir
            CROCHET: égrenoir, _gorgeoir, bouillie

            % ... the first line of the file
            DF, 11 BARATTE, 1N ROULEAU
            BALANCE, 0N ROULEAU, 0N TINET: charrue
            BANNETON, 01 CROCHET, 11 FLÉAU, 1N TINET: pulvérisateur
            PORTE, 11 CROCHET, 0N CROCHET

            ROULEAU: tribulum
            HERSE, 1N FLÉAU, 1N FLÉAU

            FLÉAU: battadère, van, mesure
        """
        mcd = Mcd(source, **params)
        expected = """
            % The comments are placed before
            % ... the first line of the file
            
            :
            FLÉAU: battadère, van, mesure
            :
            :

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
        """.replace("    ", "").strip()
        actual = mcd.get_vertically_flipped_clauses().replace("    ", "").strip()
        self.assertEqual(actual, expected)
        expected = """
            % The comments are placed before
            % ... the first line of the file
            
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

            :
            :
            FLÉAU: battadère, van, mesure
            :
        """.strip().replace("  ", "")
        actual = mcd.get_horizontally_flipped_clauses().replace("    ", "").strip()
        self.assertEqual(actual, expected)
        expected = """
            % The comments are placed before
            % ... the first line of the file
            
            BARATTE: piston, racloir, fusil
            DF, 11 BARATTE, 1N ROULEAU
            :
            :

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
            :
            :
        """.strip().replace("  ", "")
        actual = mcd.get_diagonally_flipped_clauses().replace("    ", "").strip()
        self.assertEqual(actual, expected)

    def test_explicit_fit(self):
        # initially: (5, 4) for 11 nodes
        source = """
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
        """
        mcd = Mcd(source, **params)
        # minimal fit: (4, 3)
        expected = """
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
        """.strip().replace("    ", "")
        actual = mcd.get_refitted_clauses(0).strip().replace("    ", "")
        self.assertEqual(actual, expected)
        # 1st next fit: (5, 3)
        expected = """
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
            :
            :
            :
        """.strip().replace("    ", "")
        actual = mcd.get_refitted_clauses(1).strip().replace("    ", "")
        self.assertEqual(actual, expected)
        # 2nd next fit: (4, 4)
        expected = """
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

            :
            :
            :
            :
        """.strip().replace("    ", "")
        actual = mcd.get_refitted_clauses(2).strip().replace("    ", "")
        self.assertEqual(actual, expected)
        
    def test_implicit_fit_produces_min_grid_next(self):
        # initially: (4, 5) for 11 nodes
        source = """
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
        """
        mcd = Mcd(source, **params)
        # (4, 5) not being a preferred grid, it is equivalent to nth_fit == 1
        expected = """
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
            :
            :
            :
        """.strip().replace("  ", "")
        actual = mcd.get_refitted_clauses(1).strip().replace("    ", "")
        self.assertEqual(actual, expected)
    
    def test_no_overlapping(self):
        source = """
            CLIENT: Réf. client, Nom, Prénom, Adresse
            PASSER, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num commande, Date, Montant
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """.replace("    ", "")
        mcd = Mcd(source, **params)
        self.assertEqual(mcd.get_overlaps(), [])
    
    def test_no_overlapping_with_reflexive_associations(self):
        source = """
            :
            :
                A MÈRE, 01 ANIMAL, 0N> [mère] ANIMAL
            :

            :
            DF, 0N ESPÈCE, _11 ANIMAL
            ANIMAL: nom, sexe, date naissance, date décès
                A PÈRE, 0N ANIMAL, 0N> [père présumé] ANIMAL

                PEUT COHABITER AVEC, 0N ESPÈCE, 0N [commensale] ESPÈCE: nb. max. commensaux
            ESPÈCE: code espèce, libellé
                OCCUPE, 1N ANIMAL, /1N PÉRIODE, 1N ENCLOS
                PÉRIODE: date début, _date fin

            :
            PEUT VIVRE DANS, 1N ESPÈCE, 1N ENCLOS: nb. max. congénères
            ENCLOS: num. enclos
            :       
        """.replace("    ", "")
        mcd = Mcd(source, **params)
        self.assertEqual(mcd.get_overlaps(), [])
    
    def test_horizontal_legs_overlap(self):
        source = """
            CLIENT: Réf. client, Nom, Prénom, Adresse
            COMMANDE: Num commande, Date, Montant
            PRODUIT: Réf. produit, Libellé, Prix unitaire
            PASSER, 0N CLIENT, 11 COMMANDE
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
        """.replace(
            "  ", ""
        )
        mcd = Mcd(source, **params)
        self.assertEqual(
            mcd.get_overlaps(),
            [
                ("PASSER", "CLIENT", "COMMANDE", "COMMANDE"),
                ("PASSER", "COMMANDE", "INCLURE", "COMMANDE"),
                ("INCLURE", "COMMANDE", "PRODUIT", "PRODUIT"),
                ("INCLURE", "PRODUIT", "PASSER", "PASSER"),
            ],
        )

    def test_vertical_legs_overlap(self):
        source = """
            CLIENT: Réf. client, Nom, Prénom, Adresse\n
            COMMANDE: Num commande, Date, Montant\n
            PRODUIT: Réf. produit, Libellé, Prix unitaire\n
            PASSER, 0N CLIENT, 11 COMMANDE\n
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
        """
        mcd = Mcd(source, **params)
        self.assertEqual(
            mcd.get_overlaps(),
            [
                ("PASSER", "CLIENT", "COMMANDE", "COMMANDE"),
                ("PASSER", "COMMANDE", "INCLURE", "COMMANDE"),
                ("INCLURE", "COMMANDE", "PRODUIT", "PRODUIT"),
                ("INCLURE", "PRODUIT", "PASSER", "PASSER"),
            ],
        )

    def test_leg_overlaps_entity(self):
        source = """
            COMMANDE: Num commande, Date, Montant
            PRODUIT: Réf. produit, Libellé, Prix unitaire
            PASSER, 0N CLIENT, 11 COMMANDE
            CLIENT: Réf. client, Nom, Prénom, Adresse

            :
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
            :::
        """
        mcd = Mcd(source, **params)
        self.assertEqual(
            mcd.get_overlaps(),
            [('PASSER', 'COMMANDE', 'PRODUIT', 'PRODUIT')],
        )

    def test_leg_overlaps_association(self):
        source = """
            PRODUIT: Réf. produit, Libellé, Prix unitaire

            COMMANDE: Num commande, Date, Montant
            PASSER, 0N CLIENT, 11 COMMANDE
            CLIENT: Réf. client, Nom, Prénom, Adresse

            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
        """
        mcd = Mcd(source, **params)
        self.assertEqual(
            mcd.get_overlaps(),
            [('INCLURE', 'PRODUIT', 'PASSER', 'PASSER')],
        )


if __name__ == '__main__':
    unittest.main()
