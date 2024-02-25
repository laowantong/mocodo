from pathlib import Path
import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.argument_parser import parsed_arguments
from mocodo.mcd import Mcd
from mocodo.convert.relations import *
from mocodo.tools.string_tools import markdown_table
from mocodo.tools.load_mini_yaml import run as load_mini_yaml


minimal_template = load_mini_yaml(Path("mocodo/resources/relation_templates/text.yaml"))
debug_template = load_mini_yaml(Path("mocodo/resources/relation_templates/debug.yaml"))
params = parsed_arguments([])
params["title"] = "Untitled"
params["guess_title"] = False

def debug_table(t):
    tsv = t.get_text(debug_template).rstrip("\n")
    tsv = tsv.replace("this relation name", "relation")
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

    def test_association_attributes(self):
        source = """
            Client: Id. client
            Réserver, 1N Client, 0N Chambre: _Date, Durée
            Chambre: Num. chambre, Prix
        """
        expected = """
            Chambre (_Num. chambre_, Prix)
            Réserver (_Id. client_, _#Num. chambre_, _Date_, Durée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), expected)
    
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
        self.assertEqual(t.get_text(minimal_template), expected)
    
    def test_weak_entities_with_cycle(self):
        source = """
            ITEM: norm, wash, haul
            MILK, _11 ITEM, 1N DRAW: lady, face

            SOON, 1N ITEM, _11 DRAW
            DRAW: ever, unit, tour, fold
        """
        mcd = Mcd(source, params)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.17", Relations, mcd, params)

    def test_disambiguation_by_role(self):
        source = """
            Entité A: id. entité A 
            DF, 11 Entité centrale, 1N Entité A
            DF, 11 Entité centrale, 1N [-nouveau nom B] Entité B
            Entité B: id. entité B

            Entité E: id. entité E 
            DF, 11 Entité centrale, 1N [suffixe] Entité E
            Entité centrale: id. entité centrale
            DF, 11 Entité centrale, 1N [+hérissons] Entité C

            :
            Entité D: id. entité D
            DF, 11 Entité centrale, 1N [Description affichée au survol.] Entité D
            Entité C: id. entité C
        """
        expected = """
            Entité centrale (_id. entité centrale_, id. entité A, nouveau nom B, id. entité E suffixe, id. entité Chérissons, id. entité D)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), expected)

    def test_disambiguation_by_number(self):
        source = """
            Entité A: id
            DF, 11 Entité centrale, 1N Entité A
            DF, 11 Entité centrale, 1N Entité B
            Entité B: id

            Entité E: id
            DF, 11 Entité centrale, 1N [Description affichée au survol.] Entité E
            Entité centrale: id
            DF, 11 Entité centrale, 1N [suffixe] Entité C

            :
            Entité D: id
            DF, 11 Entité centrale, 1N [suffixe] Entité D
            Entité C: id
        """
        expected = """
            Entité centrale (_id_, id 2, id 3, id 4, id suffixe 1, id suffixe 2)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), expected)

    def test_disambiguation_by_role_then_number(self):
        source = """
            FOO: id
            BAR: id
            DF, 11 FOO, 1N BAR
            DF, 11 FOO, 1N BAR
            DF, 11 FOO, 1N [role] BAR
            DF, 11 FOO, 1N [+role] BAR
            DF, 11 FOO, 1N [+_role] BAR
            DF, 11 FOO, 1N [-role] BAR
            DF, 11 FOO, 1N [string containing spaces] BAR
        """
        expected = """
            FOO (_id_, id 2, id 3, id role, idrole, id_role, role, id 4)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), expected)

    def test_inheritance_leftwards_double_arrow(self):
        source = """
            /\\ ANIMAL <= CARNIVORE, HERBIVORE
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, est carnivore, quantité viande, est herbivore, plante préférée)
        """.strip().replace("    ", "")
        mcd = Mcd(source, params)
        t = Relations(mcd, params)
        self.assertEqual(t.get_text(minimal_template), text)
        expected = """
            | relation | attribute       | optionality | unicities | nature                    | is primary | adjacent source | outer source | association name | datatype            | leg note |
            |:---------|:----------------|:------------|:----------|:--------------------------|:-----------|:----------------|:-------------|:-----------------|:--------------------|:---------|
            | ANIMAL   | animal          | !           |           | primary_key               | True       |                 |              |                  |                     |          |
            | ANIMAL   | poids           |             |           | normal_attribute          | False      |                 |              |                  |                     |          |
            | ANIMAL   | est carnivore   | !           |           | deleted_child_entity_name | False      | CARNIVORE       | CARNIVORE    |                  | BOOLEAN_PLACEHOLDER |          |
            | ANIMAL   | quantité viande | ?           |           | deleted_child_attribute   | False      | CARNIVORE       |              |                  |                     |          |
            | ANIMAL   | est herbivore   | !           |           | deleted_child_entity_name | False      | HERBIVORE       | HERBIVORE    |                  | BOOLEAN_PLACEHOLDER |          |
            | ANIMAL   | plante préférée | ?           |           | deleted_child_attribute   | False      | HERBIVORE       |              |                  |                     |          |
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
            | relation | attribute       | optionality | unicities | nature                       | is primary | adjacent source | outer source | association name | datatype                 | leg note |
            |:---------|:----------------|:------------|:----------|:-----------------------------|:-----------|:----------------|:-------------|:-----------------|:-------------------------|:---------|
            | ANIMAL   | animal          | !           |           | primary_key                  | True       |                 |              |                  |                          |          |
            | ANIMAL   | poids           |             |           | normal_attribute             | False      |                 |              |                  |                          |          |
            | ANIMAL   | type            | ?           |           | deleted_child_discriminator_ | False      |                 |              |                  | UNSIGNED_INT_PLACEHOLDER |          |
            | ANIMAL   | quantité viande | ?           |           | deleted_child_attribute      | False      | CARNIVORE       |              |                  |                          |          |
            | ANIMAL   | plante préférée | ?           |           | deleted_child_attribute      | False      | HERBIVORE       |              |                  |                          |          |
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
            | relation  | attribute       | optionality | unicities | nature                       | is primary | adjacent source | outer source | association name | datatype                 | leg note |
            |:----------|:----------------|:------------|:----------|:-----------------------------|:-----------|:----------------|:-------------|:-----------------|:-------------------------|:---------|
            | ANIMAL    | animal          | !           |           | primary_key                  | True       |                 |              |                  |                          |          |
            | ANIMAL    | poids           |             |           | normal_attribute             | False      |                 |              |                  |                          |          |
            | ANIMAL    | type            | ?           |           | deleted_child_discriminator_ | False      |                 |              |                  | UNSIGNED_INT_PLACEHOLDER |          |
            | CARNIVORE | animal          | !           |           | parent_primary_key           | True       | ANIMAL          | ANIMAL       |                  |                          |          |
            | CARNIVORE | quantité viande |             |           | normal_attribute             | False      |                 |              |                  |                          |          |
            | HERBIVORE | animal          | !           |           | parent_primary_key           | True       | ANIMAL          | ANIMAL       |                  |                          |          |
            | HERBIVORE | plante préférée |             |           | normal_attribute             | False      |                 |              |                  |                          |          |
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
            | relation  | attribute       | optionality | unicities | nature                     | is primary | adjacent source | outer source | association name | datatype | leg note |
            |:----------|:----------------|:------------|:----------|:---------------------------|:-----------|:----------------|:-------------|:-----------------|:---------|:---------|
            | CARNIVORE | animal          | !           |           | deleted_parent_primary_key | True       | ANIMAL          | ANIMAL       | T                |          |          |
            | CARNIVORE | poids           |             |           | deleted_parent_attribute   | False      | ANIMAL          |              | T                |          |          |
            | CARNIVORE | quantité viande |             |           | normal_attribute           | False      |                 |              |                  |          |          |
            | HERBIVORE | animal          | !           |           | deleted_parent_primary_key | True       | ANIMAL          | ANIMAL       | T                |          |          |
            | HERBIVORE | poids           |             |           | deleted_parent_attribute   | False      | ANIMAL          |              | T                |          |          |
            | HERBIVORE | plante préférée |             |           | normal_attribute           | False      |                 |              |                  |          |          |
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
            | relation | attribute       | optionality | unicities | nature                       | is primary | adjacent source | outer source | association name | datatype                 | leg note |
            |:---------|:----------------|:------------|:----------|:-----------------------------|:-----------|:----------------|:-------------|:-----------------|:-------------------------|:---------|
            | ANIMAL   | animal          | !           |           | primary_key                  | True       |                 |              |                  |                          |          |
            | ANIMAL   | poids           |             |           | normal_attribute             | False      |                 |              |                  |                          |          |
            | ANIMAL   | type            | ?           |           | deleted_child_discriminator_ | False      |                 |              |                  | UNSIGNED_INT_PLACEHOLDER |          |
            | ANIMAL   | quantité viande | ?           |           | deleted_child_attribute      | False      | CARNIVORE       |              |                  |                          |          |
            | ANIMAL   | plante préférée | ?           |           | deleted_child_attribute      | False      | HERBIVORE       |              |                  |                          |          |
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
            | relation  | attribute       | optionality | unicities | nature                       | is primary | adjacent source | outer source | association name | datatype                 | leg note |
            |:----------|:----------------|:------------|:----------|:-----------------------------|:-----------|:----------------|:-------------|:-----------------|:-------------------------|:---------|
            | ANIMAL    | animal          | !           |           | primary_key                  | True       |                 |              |                  |                          |          |
            | ANIMAL    | poids           |             |           | normal_attribute             | False      |                 |              |                  |                          |          |
            | ANIMAL    | type            | ?           |           | deleted_child_discriminator_ | False      |                 |              |                  | UNSIGNED_INT_PLACEHOLDER |          |
            | CARNIVORE | animal          | !           |           | parent_primary_key           | True       | ANIMAL          | ANIMAL       |                  |                          |          |
            | CARNIVORE | quantité viande |             |           | normal_attribute             | False      |                 |              |                  |                          |          |
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
            /XT\\ UtilisatricesPlus --> Inscrites, Abonnées : catégorie
            Abonnées :

            Utilisatrices : idU, email
            /XT\\ Utilisatrices --> Invitées, UtilisatricesPlus : catégorie
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
    
    def test_roles_with_inheritance(self):
        # https://github.com/laowantong/mocodo/issues/110
        source = """
            Équipe: id équipe,nom équipe
            Accueille, 11 Match, 0N [-hôte] Équipe

            Reçoit, 11 Match, 0N [-visiteur] Équipe
            Match: id match

            Rencontre: id rencontre
            /XT\\ Rencontre <- Match: type rencontre
        """
        text = """
            Équipe (_id équipe_, nom équipe)
            Rencontre (_id rencontre_, type rencontre, id match, #hôte, #visiteur)
        """.strip().replace("    ", "")
        t = Relations(Mcd(source, params), params)
        self.assertEqual(t.get_text(minimal_template), text)

if __name__ == '__main__':
    unittest.main()
