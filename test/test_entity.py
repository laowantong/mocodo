import unittest
from collections import defaultdict

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.entity import *
from mocodo.tools.parser_tools import extract_clauses

def entity_wrapper(s, legs_to_strengthen=None, is_child=False):
    if legs_to_strengthen is None:
        legs_to_strengthen = []
    e = Entity(extract_clauses(s)[0])
    e.add_attributes(legs_to_strengthen, is_child, fk_format=None)
    return e

class EntityTest(unittest.TestCase):

    def test_default(self):
        entities = [
            entity_wrapper("PARTICIPANT: numero, nom, adresse"),
            entity_wrapper("PARTICIPANT:numero,nom,adresse"),
            entity_wrapper(" PARTICIPANT: numero, nom, adresse "),
            entity_wrapper("PARTICIPANT :numero ,nom ,adresse"),
        ]
        for e in entities:
            self.assertEqual(e.bid, "PARTICIPANT")
            self.assertEqual(e.name_view, "PARTICIPANT")
            self.assertEqual([a.label for a in e.attributes], ["numero", "nom", "adresse"])
            self.assertEqual([a.kind for a in e.attributes], ["strong", "simple", "simple"])

    def test_datatypes(self):
        e = entity_wrapper("PARTICIPANT: numero [type1], nom [type2] , adresse[type3]")
        self.assertEqual([a.label for a in e.attributes], ["numero", "nom", "adresse"])
        self.assertEqual([a.datatype for a in e.attributes], ["type1", "type2", "type3"])
        e = entity_wrapper("PARTICIPANT: numero [type a,b,c], nom [type2], adresse [type3]")
        self.assertEqual([a.datatype for a in e.attributes], ["type a,b,c", "type2", "type3"])
        e = entity_wrapper("PARTICIPANT: numero [], nom, adresse [type3]")
        self.assertEqual([a.datatype for a in e.attributes], ["", "", "type3"])

    def test_numbered_entity(self):
        e = entity_wrapper("PARTICIPANT5: numero, nom, adresse")
        self.assertEqual(e.bid, "PARTICIPANT5")
        self.assertEqual(e.name_view, "PARTICIPANT")
        e = entity_wrapper("PARTICIPANT123: numero, nom, adresse")
        self.assertEqual(e.bid, "PARTICIPANT123")
        self.assertEqual(e.name_view, "PARTICIPANT12")

    def test_blank(self):
        e = entity_wrapper("MOT-CLEF: mot-clé, ,")
        self.assertEqual([a.label for a in e.attributes], ["mot-clé", "", ""])
        self.assertEqual([a.kind for a in e.attributes], ["strong", "phantom", "phantom"])

    def test_all_blank(self):
        e = entity_wrapper("BLANK: , ,")
        self.assertEqual([a.label for a in e.attributes], ["", "", ""])
        self.assertEqual([a.kind for a in e.attributes], ["phantom", "phantom", "phantom"])

    def test_no_identifier_at_first_position(self):
        e = entity_wrapper("POSITION: _abscisse, ordonnee")
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.kind for a in e.attributes], ["simple", "simple"])

    def test_no_identifier_for_children(self):
        e = entity_wrapper("POSITION: abscisse, _ordonnee", [], is_child=True)
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.kind for a in e.attributes], ["simple", "simple"])

    def test_multiple_strong_identifier(self):
        e = entity_wrapper("POSITION: abscisse, _ordonnee")
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee"])
        self.assertEqual([a.kind for a in e.attributes], ["strong", "strong"])

    def test_weak_identifier(self):
        e = entity_wrapper("LIVRE: Num. exemplaire, Etat du livre, Date d'achat", ["placeholder"])
        self.assertEqual([a.label for a in e.attributes], ["Num. exemplaire", "Etat du livre", "Date d'achat"])
        self.assertEqual([a.kind for a in e.attributes], ["weak", "simple", "simple"])

    def test_weak_composite_identifier(self):
        e = entity_wrapper("POSITION: abscisse, _ordonnee, foobar", ["placeholder"])
        self.assertEqual([a.label for a in e.attributes], ["abscisse", "ordonnee", "foobar"])
        self.assertEqual([a.kind for a in e.attributes], ["weak", "weak", "simple"])


class CandidateIdentifiersTest(unittest.TestCase):

    def check(self, expected_candidates, expected_id_texts, legs_to_strengthen=None):
        for source in self.sources:
            entity = entity_wrapper(source, legs_to_strengthen)
            self.assertEqual(entity.candidates, expected_candidates)
            actual_id_texts = [a.id_text for a in entity.attributes]
            self.assertEqual(actual_id_texts, expected_id_texts)

    # Strong entities without alternate identifiers

    def test_simple_id(self):
        self.sources = [
            "FOOBAR: foo, bar, biz, qux",
        ]
        self.check(
            {"0": {"foo"}},
            ["ID", "", "", ""]
        )
    
    def test_no_id(self):
        self.sources = [
            "FOOBAR: _foo, bar, biz, qux",
            "FOOBAR: 0_foo, bar, biz, qux",            
        ]
        self.check(
            {},
            ["", "", "", ""]
        )

    def test_composite_id(self):
        self.sources = [
            "FOOBAR: foo, _bar, biz, qux",
            "FOOBAR: foo, 0_bar, biz, qux",
        ]
        self.check(
            {"0": {"foo", "bar"}},
            ["ID", "ID", "", ""]
        )
    
    def test_pushed_simple_id(self):
        self.sources = [
            "FOOBAR: _foo, _bar, biz, qux",
            "FOOBAR: _foo, 0_bar, biz, qux",
            "FOOBAR: 0_foo, _bar, biz, qux",
            "FOOBAR: 0_foo, 0_bar, biz, qux",
        ]
        self.check(
            {"0": {"bar"}},
            ["", "ID", "", ""]
        )

    def test_pushed_composite_id(self):
        self.sources = [
            "FOOBAR: _foo, _bar, _biz, qux",
            "FOOBAR: _foo, _bar, 0_biz, qux",
            "FOOBAR: _foo, 0_bar, _biz, qux",
            "FOOBAR: _foo, 0_bar, 0_biz, qux",
            "FOOBAR: 0_foo, _bar, _biz, qux",
            "FOOBAR: 0_foo, _bar, 0_biz, qux",
            "FOOBAR: 0_foo, 0_bar, _biz, qux",
            "FOOBAR: 0_foo, 0_bar, 0_biz, qux",
        ]
        self.check(
            {"0": {"bar", "biz"}},
            ["", "ID", "ID", ""]
        )

    # Weak entities without alternate identifiers

    def test_simple_weak_id(self):
        self.sources = [
            "FOOBAR: foo, bar, biz, qux",
        ]
        self.check(
            {"0": {"foo"}},
            ["id", "", "", ""],
            legs_to_strengthen = ["placeholder"]
        )
    
    def test_no_weak_id(self):
        self.sources = [
            "FOOBAR: _foo, bar, biz, qux",
            "FOOBAR: 0_foo, bar, biz, qux",            
        ]
        self.check(
            {},
            ["", "", "", ""],
            legs_to_strengthen = ["placeholder"]
        )

    def test_composite_weak_id(self):
        self.sources = [
            "FOOBAR: foo, _bar, biz, qux",
            "FOOBAR: foo, 0_bar, biz, qux",
        ]
        self.check(
            {"0": {"foo", "bar"}},
            ["id", "id", "", ""],
            legs_to_strengthen = ["placeholder"]
        )
    
    def test_pushed_simple_weak_id(self):
        self.sources = [
            "FOOBAR: _foo, _bar, biz, qux",
            "FOOBAR: _foo, 0_bar, biz, qux",
            "FOOBAR: 0_foo, _bar, biz, qux",
            "FOOBAR: 0_foo, 0_bar, biz, qux",
        ]
        self.check(
            {"0": {"bar"}},
            ["", "id", "", ""],
            legs_to_strengthen = ["placeholder"]
        )

    def test_pushed_composite_weak_id(self):
        self.sources = [
            "FOOBAR: _foo, _bar, _biz, qux",
            "FOOBAR: _foo, _bar, 0_biz, qux",
            "FOOBAR: _foo, 0_bar, _biz, qux",
            "FOOBAR: _foo, 0_bar, 0_biz, qux",
            "FOOBAR: 0_foo, _bar, _biz, qux",
            "FOOBAR: 0_foo, _bar, 0_biz, qux",
            "FOOBAR: 0_foo, 0_bar, _biz, qux",
            "FOOBAR: 0_foo, 0_bar, 0_biz, qux",
        ]
        self.check(
            {"0": {"bar", "biz"}},
            ["", "id", "id", ""],
            legs_to_strengthen = ["placeholder"]
        )

    # Strong entities with alternate identifiers

    def test_alt_ids_and_simple_id(self):
        self.sources = [
            "FOOBAR: foo, 1_bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"foo"}, "1": {"bar", "biz"}, "2": {"biz", "qux"}},
            ["ID", "1", "1 2", "2"]
        )
        self.sources = [
            "FOOBAR: 1_foo, bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"foo"}, "1": {"foo", "biz"}, "2": {"biz", "qux"}},
            ["1 ID", "", "1 2", "2"]
        )
    
    def test_alt_ids_and_no_id(self):
        self.sources = [
            "FOOBAR: _foo, 1_bar, 12_biz, 2_qux",
            "FOOBAR: 0_foo, 1_bar, 12_biz, 2_qux",
        ]
        self.check(
            {"1": {"bar", "biz"}, "2": {"biz", "qux"}},
            ["", "1", "1 2", "2"]
        )

    def test_alt_ids_and_composite_id(self):
        # NB: the "0" prefix is mandatory since "bar" belongs to an alt id.
        # Otherwise, cf. test_alt_ids_and_simple_id().
        self.sources = [
            "FOOBAR: foo, 01_bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"foo", "bar"}, "1": {"bar", "biz"}, "2": {"biz", "qux"}},
            ["ID", "1 ID", "1 2", "2"]
        )
        # When "bar" is not part of an alt id, the "0" prefix is optional.
        self.sources = [
            "FOOBAR: foo, _bar, 12_biz, 2_qux",
            "FOOBAR: foo, 0_bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"foo", "bar"}, "1": {"biz"}, "2": {"biz", "qux"}},
            ["ID", "ID", "1 2", "2"]
        )
        # When "bar" is not part of an alt id, the "0" prefix is optional.
        self.sources = [
            "FOOBAR: 1_foo, 0_bar, 12_biz, 2_qux",
            "FOOBAR: 1_foo, _bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"foo", "bar"}, "1": {"foo", "biz"}, "2": {"biz", "qux"}},
            ["1 ID", "ID", "1 2", "2"]
        )
    
    def test_alt_ids_and_pushed_simple_id(self):
        # NB: the "0" prefix on "bar" is mandatory since "bar" belongs to an alt id.
        # Otherwise, cf. test_alt_ids_and_no_id().
        self.sources = [
            "FOOBAR: _foo, 01_bar, 12_biz, 2_qux",
            "FOOBAR: 0_foo, 01_bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"bar"}, "1": {"bar", "biz"}, "2": {"biz", "qux"}},
            ["", "1 ID", "1 2", "2"]
        )
        # When "bar" is not part of an alt id, the "0" prefix is optional.
        self.sources = [
            "FOOBAR: _foo, _bar, 12_biz, 2_qux",
            "FOOBAR: 0_foo, _bar, 12_biz, 2_qux",
            "FOOBAR: _foo, 0_bar, 12_biz, 2_qux",
            "FOOBAR: 0_foo, 0_bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"bar"}, "1": {"biz"}, "2": {"biz", "qux"}},
            ["", "ID", "1 2", "2"]
        )
        # NB: the "0" prefix on "foo" is mandatory since "foo" belongs to an alt id.
        # Otherwise, cf. test_alt_ids_and_composite_id().
        self.sources = [
            "FOOBAR: 01_foo, 0_bar, 12_biz, 2_qux",
            "FOOBAR: 01_foo, _bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"bar"}, "1": {"foo", "biz"}, "2": {"biz", "qux"}},
            ["1", "ID", "1 2", "2"]
        )

    def test_alt_ids_and_pushed_composite_id(self):
        self.sources = [
            "FOOBAR: _foo, 01_bar, 02_biz, 12_qux",
            "FOOBAR: 0_foo, 01_bar, 02_biz, 12_qux",
        ]
        self.check(
            {"0": {"bar", "biz"}, "1": {"bar", "qux"}, "2": {"biz", "qux"}},
            ["", "1 ID", "2 ID", "1 2"]
        )
        self.sources = [
            "FOOBAR: _foo, _bar, 02_biz, 12_qux",
            "FOOBAR: 0_foo, _bar, 02_biz, 12_qux",
            "FOOBAR: _foo, 0_bar, 02_biz, 12_qux",
            "FOOBAR: 0_foo, 0_bar, 02_biz, 12_qux",
        ]
        self.check(
            {"0": {"bar", "biz"}, "1": {"qux"}, "2": {"biz", "qux"}},
            ["", "ID", "2 ID", "1 2"]
        )
        self.sources = [
            "FOOBAR: 02_foo, _bar, _biz, 12_qux",
            "FOOBAR: 02_foo, _bar, 0_biz, 12_qux",
            "FOOBAR: 02_foo, 0_bar, _biz, 12_qux",
            "FOOBAR: 02_foo, 0_bar, 0_biz, 12_qux",
        ]
        self.check(
            {"0": {"bar", "biz"}, "1": {"qux"}, "2": {"foo", "qux"}},
            ["2", "ID", "ID", "1 2"]
        )

    # Weak entities with alternate identifiers
    # Just one test, since the logic is the same as for strong entities.

    def test_alt_ids_and_simple_id(self):
        self.sources = [
            "FOOBAR: foo, 1_bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"foo"}, "1": {"bar", "biz"}, "2": {"biz", "qux"}},
            ["id", "1", "1 2", "2"],
            legs_to_strengthen =["placeholder"]
        )
        self.sources = [
            "FOOBAR: 1_foo, bar, 12_biz, 2_qux",
        ]
        self.check(
            {"0": {"foo"}, "1": {"foo", "biz"}, "2": {"biz", "qux"}},
            ["1 id", "", "1 2", "2"],
            legs_to_strengthen = ["placeholder"]
        )
    

if __name__ == '__main__':
    unittest.main()
