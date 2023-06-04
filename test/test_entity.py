import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.entity import *
from mocodo.parser_tools import extract_clauses

def entity_wrapper(s, **kargs):
    return Entity(extract_clauses(s)[0], **kargs)

class EntityTest(unittest.TestCase):

    def test_default(self):
        entities = [
            entity_wrapper("PARTICIPANT: numero, nom, adresse"),
            entity_wrapper("PARTICIPANT:numero,nom,adresse"),
            entity_wrapper(" PARTICIPANT: numero, nom, adresse "),
            entity_wrapper("PARTICIPANT :numero ,nom ,adresse"),
        ]
        for e in entities:
            e.add_attributes([])
            self.assertEqual(e.name, "PARTICIPANT")
            self.assertEqual(e.name_view, "PARTICIPANT")
            self.assertEqual([a.label for a in e.attributes], ["numero", "nom", "adresse"])
            self.assertEqual([a.kind for a in e.attributes], ["strong", "simple", "simple"])

    def test_data_types(self):
        e = entity_wrapper("PARTICIPANT: numero [type1], nom [type2] , adresse[type3]")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["numero", "nom", "adresse"])
        self.assertEqual([a.data_type for a in e.attributes], ["type1", "type2", "type3"])
        e = entity_wrapper("PARTICIPANT: numero [type a,b,c], nom [type2], adresse [type3]")
        e.add_attributes([])
        self.assertEqual([a.data_type for a in e.attributes], ["type a,b,c", "type2", "type3"])
        e = entity_wrapper("PARTICIPANT: numero [], nom, adresse [type3]")
        e.add_attributes([])
        self.assertEqual([a.data_type for a in e.attributes], ["", None, "type3"])

    def test_numbered_entity(self):
        e = entity_wrapper("PARTICIPANT5: numero, nom, adresse")
        e.add_attributes([])
        self.assertEqual(e.name, "PARTICIPANT5")
        self.assertEqual(e.name_view, "PARTICIPANT")
        e = entity_wrapper("PARTICIPANT123: numero, nom, adresse")
        e.add_attributes([])
        self.assertEqual(e.name, "PARTICIPANT123")
        self.assertEqual(e.name_view, "PARTICIPANT12")

    def test_blank(self):
        e = entity_wrapper("MOT-CLEF: mot-clé, ,")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["mot-clé", "", ""])
        self.assertEqual([a.kind for a in e.attributes], ["strong", "phantom", "phantom"])

    def test_all_blank(self):
        e = entity_wrapper("BLANK: , ,")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["", "", ""])
        self.assertEqual([a.kind for a in e.attributes], ["phantom", "phantom", "phantom"])

    def test_no_identifier_at_first_position(self):
        e = entity_wrapper("POSITION: _abscisse, ordonnee")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.kind for a in e.attributes], ["simple", "simple"])

    def test_no_identifier_for_children(self):
        e = entity_wrapper("POSITION: abscisse, _ordonnee")
        e.add_attributes([], is_child=True)
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.kind for a in e.attributes], ["simple", "simple"])

    def test_multiple_strong_identifier(self):
        e = entity_wrapper("POSITION: abscisse, _ordonnee")
        e.add_attributes([])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.kind for a in e.attributes], ["strong", "strong"])

    def test_weak_identifier(self):
        e = entity_wrapper("LIVRE: Num. exemplaire, Etat du livre, Date d'achat")
        e.add_attributes(["placeholder"])
        self.assertEqual([a.label for a in e.attributes], ["Num. exemplaire", "Etat du livre", "Date d'achat"])
        self.assertEqual([a.kind for a in e.attributes], ["weak", "simple", "simple"])

    def test_weak_composite_identifier(self):
        e = entity_wrapper("POSITION: abscisse, _ordonnee, foobar")
        e.add_attributes(["placeholder"])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee", "foobar"])
        self.assertEqual([a.kind for a in e.attributes], ["weak", "weak", "simple"])

if __name__ == '__main__':
    unittest.main()
