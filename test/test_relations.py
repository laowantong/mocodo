import json
import unittest
from copy import deepcopy

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.argument_parser import parsed_arguments
from mocodo.file_helpers import read_contents
from mocodo.mcd import Mcd
from mocodo.convert.relations import *
from mocodo.tools.string_tools import markdown_table


minimal_template = json.loads(read_contents("mocodo/resources/relation_templates/text.json"))
debug_template = json.loads(read_contents("mocodo/resources/relation_templates/debug.json"))
params = parsed_arguments()
params["title"] = "Untitled"
params["guess_title"] = False


def debug_table(t):
    tsv = t.get_text(debug_template).strip().replace("this_relation_name", "relation")
    rows = [line.split("\t") for line in tsv.split("\n")]
    return re.sub("(?m)^", "            ", markdown_table(rows))

class relationsTest(unittest.TestCase):
    
    def test_arrows_are_ignored(self):
        source = """
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N< Personne, 22> Personne
        """
        t = Relations(Mcd(source, params), params)
        d1 = t.get_text(debug_template)
        source = """
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N Personne, 22 Personne
        """
        t = Relations(Mcd(source, params), params)
        d2 = t.get_text(debug_template)
        self.assertEqual(d1, d2)
    
    def test_reciprocical_relative_entities(self):
        source = """
            Aids: Norm, Free, Soon, Pack, Face, Seem, Teen
            Yard, 0N Unit, ON Aids
            Ever, 1N Unit, 1N Item
            Item: Norm, Wash, Haul, Milk, Draw, Lady, Face, Soon, Dish
            :

            Amid, 1n Aids, 1n Disk, _11 Flip: Gold
            Same, _11 Unit, 0N Flip
            Unit: Folk, Peer, Tour, Hall
            Fold, _11 Unit, 1N Baby, _11 Item
            Baby: Soon

            Disk: Soon, Ride, Folk, Call, Gear, Tent, Lean
            Flip: Lend
            Pump, _11 Flip, 1N Unit: Both, Raid
            Gene: Soon
            Bind, _11 Baby, 1n Gene
        """
        mcd = Mcd(source, params)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.11", Relations, mcd, params)
        source = """
            Disk: Soon, Ride, Folk, Call, Gear, Tent, Lean
            Flip: Lend
            Pump, _11 Flip, 1N Unit: Both, Raid
            Gene: Soon
            Bind, _11 Baby, 1n Gene

            Amid, 1n Aids, 1n Disk, _11 Flip: Gold
            Same, _11 Unit, 0N Flip
            Unit: Folk, Peer, Tour, Hall
            Fold, _11 Unit, 1N Baby, _11 Item
            Baby: Soon

            Aids: Norm, Free, Soon, Pack, Face, Seem, Teen
            Yard, 0N Unit, ON Aids
            Ever, 1N Unit, 1N Item
            Item: Norm, Wash, Haul, Milk, Draw, Lady, Face, Soon, Dish
            :
        """
        mcd = Mcd(source, params)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.11", Relations, mcd, params)
        mcd = Mcd(source, params)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.11", Relations, mcd, params)
        source = """
            ITEM, 1N NORM, 1N WASH
            NORM: haul
            
            WASH: soon
            BABY, 1N WASH, 1N FACE
            FACE: gene
            
            AAA, _11 FLIP, 1N WASH
            FLIP: soona
            GEAR, _11 FLIP, _11 FACE
        """
        mcd = Mcd(source, params)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.11", Relations, mcd, params)
        source = """
            ITEM, 1N NORM, 1N WASH
            NORM: haul
            
            WASH: soon
            BABY, 1N WASH, 1N FACE
            FACE: gene
            
            CCC, _11 FLIP, 1N WASH
            FLIP: soona
            GEAR, _11 FLIP, _11 FACE
        """
        mcd = Mcd(source, params)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.11", Relations, mcd, params)

    
    def test_weak_entities_strengthened_by_itself(self):
        source = """
            SCELERISQUE: blandit, elit
            DF, _11 SCELERISQUE, 1N SCELERISQUE
        """
        mcd = Mcd(source, params)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.16", Relations, mcd, params)
    
    def test_weak_entities_strengthened_by_several_entities(self):
        source = """
            Baby: Soon, protect_baby
            Yard, _11 Unit, ON Baby: Hall
            
            :
            Unit: Folk, Peer
            
            
            Item: Norm, Wash
            Ever, _11 Unit, 1N Item: Tour
        """
        expected = """
            Baby (_Soon_, protect_baby)
            Item (_Norm_, Wash)
            Unit (_#Norm_, _#Soon_, _Folk_, Peer, Hall, Tour)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertTrue(t.get_text(minimal_template) == expected)
    
    def test_weak_entities_with_cycle(self):
        source = """
            ITEM: norm, wash, haul
            MILK, _11 ITEM, 1N DRAW: lady, face

            SOON, 1N ITEM, _11 DRAW
            DRAW: ever, unit, tour, fold
        """
        mcd = Mcd(source, params)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.17", Relations, mcd, params)
    
    def test_difference_between_attribute_label_before_disambiguation_and_label_with_notes(self):
        template = {
          "extension": ".json",
          "transform_attribute": [
            {
              "search": " ",
              "replace": "_"
            },
            {
              "search": "\\.",
              "replace": ""
            }
          ],
          "compose_label_disambiguated_by_note": "{leg_note}",
        }
        source = """
            A pour mère, 01 Chien, 0N [num_mère] Chien
            Chien: num. chien, nom chien, sexe, date naissance
            A pour père présumé, 0N Chien, 0N [num_père] Chien
        """
        text = """
            A pour père présumé (_#num_chien_, _#num_père_)
            Chien (_num_chien_, nom_chien, sexe, date_naissance, #num_mère)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(template), text)
    
    def test_difference_between_attribute_label_before_disambiguation_and_label_without_notes(self):
        template = {
          "extension": None,
          "transform_attribute": [
            {
              "search": " ",
              "replace": "_"
            },
            {
              "search": "\\.",
              "replace": ""
            }
          ],
          "compose_label_disambiguated_by_number": "{label_before_disambiguation}_{disambiguation_number}",
        }
        source = """
            A pour mère, 01 Chien, 0N Chien
            Chien: num. chien, nom chien, sexe, date naissance
            A pour père présumé, 0N Chien, 0N Chien
        """
        text = """
            A pour père présumé (_#num_chien_, _#num_chien_1_)
            Chien (_num_chien_, nom_chien, sexe, date_naissance, #num_chien_1)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(template), text)
    
    def test_inheritance_leftwards_double_arrow(self):
        source = """
            /\\ ANIMAL <= CARNIVORE, HERBIVORE
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, CARNIVORE, quantité viande, HERBIVORE, plante préférée)
        """.strip().replace("    ", "")
        mcd = Mcd(source, params)
        t = Relations(mcd, params)
        self.assertEqual(t.get_text(minimal_template), text)
        expected = """
            | relation | label           | data_type           | nature                    | adjacent_source |
            |:---------|:----------------|:--------------------|:--------------------------|:----------------|
            | ANIMAL   | animal          |                     | primary_key               |                 |
            | ANIMAL   | poids           |                     | normal_attribute          |                 |
            | ANIMAL   | CARNIVORE       | BOOLEAN_PLACEHOLDER | deleted_child_entity_name | CARNIVORE       |
            | ANIMAL   | quantité viande |                     | deleted_child_attribute   | CARNIVORE       |
            | ANIMAL   | HERBIVORE       | BOOLEAN_PLACEHOLDER | deleted_child_entity_name | HERBIVORE       |
            | ANIMAL   | plante préférée |                     | deleted_child_attribute   | HERBIVORE       |
        """
        actual = debug_table(t)
        self.assertEqual(actual.strip(), expected.strip())

    def test_inheritance_leftwards_simple_arrow(self):
        source = """
            /\\ ANIMAL <- CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, type, quantité viande, plante préférée)
        """.strip().replace("    ", "")
        mcd = Mcd(source, params)
        t = Relations(mcd, params)
        self.assertEqual(t.get_text(minimal_template), text)
        expected = """
            | relation | label           | data_type                | nature                      | adjacent_source |
            |:---------|:----------------|:-------------------------|:----------------------------|:----------------|
            | ANIMAL   | animal          |                          | primary_key                 |                 |
            | ANIMAL   | poids           |                          | normal_attribute            |                 |
            | ANIMAL   | type            | UNSIGNED_INT_PLACEHOLDER | deleted_child_discriminant_ |                 |
            | ANIMAL   | quantité viande |                          | deleted_child_attribute     | CARNIVORE       |
            | ANIMAL   | plante préférée |                          | deleted_child_attribute     | HERBIVORE       |
        """
        actual = debug_table(t)
        self.assertEqual(actual.strip(), expected.strip())

    def test_inheritance_rightwards_simple_arrow(self):
        source = """
            /\\ ANIMAL -> CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, type)
            CARNIVORE (_#animal_, quantité viande)
            HERBIVORE (_#animal_, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        expected = """
            | relation  | label           | data_type                | nature                      |
            |:----------|:----------------|:-------------------------|:----------------------------|
            | ANIMAL    | animal          |                          | primary_key                 |
            | ANIMAL    | poids           |                          | normal_attribute            |
            | ANIMAL    | type            | UNSIGNED_INT_PLACEHOLDER | deleted_child_discriminant_ |
            | CARNIVORE | animal          |                          | parent_primary_key          |
            | CARNIVORE | quantité viande |                          | normal_attribute            |
            | HERBIVORE | animal          |                          | parent_primary_key          |
            | HERBIVORE | plante préférée |                          | normal_attribute            |
        """
        actual = debug_table(t)
        self.assertEqual(actual.strip(), expected.strip())

    def test_inheritance_rightwards_double_arrow_with_totality(self):
        source = """
            /T\\ ANIMAL => CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            CARNIVORE (_animal_, poids, quantité viande)
            HERBIVORE (_animal_, poids, plante préférée)
        """.strip().replace("    ", "")
        mcd = Mcd(source, params)
        t = Relations(mcd, params)
        self.assertEqual(t.get_text(minimal_template), text)
        expected = """
            | relation  | label           | data_type | nature                     |
            |:----------|:----------------|:----------|:---------------------------|
            | CARNIVORE | animal          |           | deleted_parent_primary_key |
            | CARNIVORE | poids           |           | deleted_parent_attribute   |
            | CARNIVORE | quantité viande |           | normal_attribute           |
            | HERBIVORE | animal          |           | deleted_parent_primary_key |
            | HERBIVORE | poids           |           | deleted_parent_attribute   |
            | HERBIVORE | plante préférée |           | normal_attribute           |
        """
        actual = debug_table(t)
        self.assertEqual(actual.strip(), expected.strip())

    def test_inheritance_rightwards_double_arrow_without_totality(self):
        source = """
            /X\\ ANIMAL => CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        mcd = Mcd(source, params)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.25", Relations, mcd, params)

    def test_inheritance_leftwards_simple_arrow_unpretty(self):
        source = """
            /\\ ANIMAL <-- CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, type, quantité viande, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        expected = """
            | relation | label           | data_type                | nature                      | adjacent_source |
            |:---------|:----------------|:-------------------------|:----------------------------|:----------------|
            | ANIMAL   | animal          |                          | primary_key                 |                 |
            | ANIMAL   | poids           |                          | normal_attribute            |                 |
            | ANIMAL   | type            | UNSIGNED_INT_PLACEHOLDER | deleted_child_discriminant_ |                 |
            | ANIMAL   | quantité viande |                          | deleted_child_attribute     | CARNIVORE       |
            | ANIMAL   | plante préférée |                          | deleted_child_attribute     | HERBIVORE       |
        """
        actual = debug_table(t)
        self.assertEqual(actual.strip(), expected.strip())

    def test_inheritance_with_unique_child(self):
        source = """
            CARNIVORE: quantité viande
            /\\ ANIMAL -> CARNIVORE: type
            ANIMAL: animal, poids
        """
        text = """
            ANIMAL (_animal_, poids, type)
            CARNIVORE (_#animal_, quantité viande)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        expected = """
            | relation  | label           | data_type                | nature                      |
            |:----------|:----------------|:-------------------------|:----------------------------|
            | ANIMAL    | animal          |                          | primary_key                 |
            | ANIMAL    | poids           |                          | normal_attribute            |
            | ANIMAL    | type            | UNSIGNED_INT_PLACEHOLDER | deleted_child_discriminant_ |
            | CARNIVORE | animal          |                          | parent_primary_key          |
            | CARNIVORE | quantité viande |                          | normal_attribute            |
        """
        actual = debug_table(t)
        self.assertEqual(actual.strip(), expected.strip())

    def test_inheritance_with_distant_leg_note(self):
        source = """
            HERBIVORE: plante préférée
            :
            :

            /XT\\ ANIMAL => CARNIVORE, HERBIVORE: type alimentation
            ANIMAL: nom, sexe, date naissance, date décès
            A MÈRE, 01 ANIMAL, 0N> [mère] ANIMAL

            CARNIVORE: quantité viande
            :
            :        
        """
        text = """
            CARNIVORE (_nom_, sexe, date naissance, date décès, nom mère, quantité viande)
            HERBIVORE (_nom_, sexe, date naissance, date décès, nom mère, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), text)
    
    def test_two_same_type_inheritances(self):
        # example from user fduchatea on https://github.com/laowantong/mocodo/issues/64
        source = """
            :
            :
            Inscrites :
            :

            :
            UtilisatricesPlus : nom, prénom
            /XT1\\ UtilisatricesPlus --> Inscrites, Abonnées : catégorie
            Abonnées :

            Utilisatrices : idU, email
            /XT2\\ Utilisatrices --> Invitées, UtilisatricesPlus : catégorie
            Invitées : adresseIP
            :
        """
        text = """
            Invitées (_#idU_, adresseIP)
            Utilisatrices (_idU_, email, catégorie)
            UtilisatricesPlus (_#idU_, nom, prénom, catégorie)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), text)
    

if __name__ == '__main__':
    unittest.main()
