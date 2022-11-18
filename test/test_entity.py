import unittest

__import__("sys").path[0:0] = ["mocodo"]
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
            e.add_attributes([])
            self.assertEqual(e.name, "PARTICIPANT")
            self.assertEqual(e.name_view, "PARTICIPANT")
            self.assertEqual([a.label for a in e.attributes], ["numero", "nom", "adresse"])
            self.assertEqual([a.get_category() for a in e.attributes], ["strong", "simple", "simple"])

    def test_data_types(self):
        e = Entity("PARTICIPANT: numero [type1], nom [type2] , adresse[type3]")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["numero", "nom", "adresse"])
        self.assertEqual([a.data_type for a in e.attributes], ["type1", "type2", "type3"])
        e = Entity("PARTICIPANT: numero [type a,b,c], nom [type2], adresse [type3]")
        e.add_attributes([])
        self.assertEqual([a.data_type for a in e.attributes], ["type a,b,c", "type2", "type3"])
        e = Entity("PARTICIPANT: numero [], nom, adresse [type3]")
        e.add_attributes([])
        self.assertEqual([a.data_type for a in e.attributes], ["", None, "type3"])
        e = Entity("PARTICIPANT: numero [, nom, adresse")
        e.add_attributes([])
        self.assertEqual([a.data_type for a in e.attributes], [None, None, None])

    def test_numbered_entity(self):
        e = Entity("PARTICIPANT5: numero, nom, adresse")
        e.add_attributes([])
        self.assertEqual(e.name, "PARTICIPANT5")
        self.assertEqual(e.name_view, "PARTICIPANT")
        e = Entity("PARTICIPANT123: numero, nom, adresse")
        e.add_attributes([])
        self.assertEqual(e.name, "PARTICIPANT123")
        self.assertEqual(e.name_view, "PARTICIPANT12")

    def test_blank(self):
        e = Entity("MOT-CLEF: mot-clé, ,")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["mot-clé", "", ""])
        self.assertEqual([a.get_category() for a in e.attributes], ["strong", "phantom", "phantom"])

    def test_all_blank(self):
        e = Entity("BLANK: , ,")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["", "", ""])
        self.assertEqual([a.get_category() for a in e.attributes], ["phantom", "phantom", "phantom"])

    def test_no_identifier_at_first_position(self):
        e = Entity("POSITION: _abscisse, ordonnee")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.get_category() for a in e.attributes], ["simple", "simple"])

    def test_no_identifier_for_children(self):
        e = Entity("POSITION: abscisse, _ordonnee")
        e.add_attributes([], is_child=True)
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.get_category() for a in e.attributes], ["simple", "simple"])

    def test_multiple_strong_identifier(self):
        e = Entity("POSITION: abscisse, _ordonnee")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.get_category() for a in e.attributes], ["strong", "strong"])

    def test_weak_identifier(self):
        e = Entity("LIVRE: Num. exemplaire, Etat du livre, Date d'achat")
        e.add_attributes(["placeholder"])
        self.assertEqual([a.label for a in e.attributes], ["Num. exemplaire", "Etat du livre", "Date d'achat"])
        self.assertEqual([a.get_category() for a in e.attributes], ["weak", "simple", "simple"])

    def test_weak_composite_identifier(self):
        e = Entity("POSITION: abscisse, _ordonnee, foobar")
        e.add_attributes(["placeholder"])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee", "foobar"])
        self.assertEqual([a.get_category() for a in e.attributes], ["weak", "weak", "simple"])

    def test_backslash_suppression(self):
        e = Entity("PARTICIPANT\: numero\, \tnom\t, ad\\resse")
        e.add_attributes([])
        self.assertEqual(e.name, "PARTICIPANT")
        self.assertEqual(e.name_view, "PARTICIPANT")
        self.assertEqual([a.label for a in e.attributes], ["numero", "nom", "adresse"])

if __name__ == '__main__':
    unittest.main()
