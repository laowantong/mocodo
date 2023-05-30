import gettext
import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.association import *
from mocodo.parser_tools import extract_clauses


gettext.NullTranslations().install()

def association_wrapper(s, **kargs):
    return Association(extract_clauses(s)[0], **kargs)

class ParseTest(unittest.TestCase):
    
    def test_reflexive(self):
        a = association_wrapper("ÊTRE AMI, 0N BANDIT, 0N BANDIT")
        self.assertEqual(a.name, "ÊTRE AMI")
        self.assertEqual(a.name_view, "ÊTRE AMI")
        self.assertEqual(a.attributes, [])
        for (i, leg) in enumerate(a.legs):
            self.assertEqual(leg.card_view, "0,N")
            self.assertEqual(leg.entity_name, "BANDIT")
            self.assertEqual(leg.arrow, "")
            self.assertEqual(leg.note, None)

    def test_double(self):
        l = [
            association_wrapper("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE"),
            association_wrapper("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE:"),
            association_wrapper("EMPLOYER,01 PARTICIPANT,0N ENTREPRISE"),
            association_wrapper(" EMPLOYER , 01 PARTICIPANT, 0N   ENTREPRISE "),
        ]
        for a in l:
            self.assertEqual(a.name, "EMPLOYER")
            self.assertEqual(a.name_view, "EMPLOYER")
            self.assertEqual(a.attributes, [])
            self.assertEqual(a.legs[0].card_view, "0,1")
            self.assertEqual(a.legs[0].entity_name, "PARTICIPANT")
            self.assertEqual(a.legs[0].arrow, "")
            self.assertEqual(a.legs[0].note, None)
            self.assertEqual(a.legs[1].card_view, "0,N")
            self.assertEqual(a.legs[1].entity_name, "ENTREPRISE")
            self.assertEqual(a.legs[1].arrow, "")
            self.assertEqual(a.legs[1].note, None)

    def test_triple(self):
        a = association_wrapper("SUIVRE, 0N DATE, 11 ÉTUDIANT, 0N ENSEIGNANT")
        self.assertEqual(a.name, "SUIVRE")
        self.assertEqual(a.name_view, "SUIVRE")
        self.assertEqual(a.attributes, [])
        self.assertEqual(a.legs[0].card_view, "0,N")
        self.assertEqual(a.legs[0].entity_name, "DATE")
        self.assertEqual(a.legs[0].arrow, "")
        self.assertEqual(a.legs[0].note, None)
        self.assertEqual(a.legs[1].card_view, "1,1")
        self.assertEqual(a.legs[1].entity_name, "ÉTUDIANT")
        self.assertEqual(a.legs[1].arrow, "")
        self.assertEqual(a.legs[1].note, None)
        self.assertEqual(a.legs[2].card_view, "0,N")
        self.assertEqual(a.legs[2].entity_name, "ENSEIGNANT")
        self.assertEqual(a.legs[2].arrow, "")
        self.assertEqual(a.legs[2].note, None)

    def test_arrow(self):
        a = association_wrapper("EMPLOYER, 01> PARTICIPANT, 0N< ENTREPRISE")
        self.assertEqual(a.legs[0].arrow, ">")
        self.assertEqual(a.legs[1].arrow, "<")
        self.assertEqual(a.legs[0].card_view, "0,1")
        self.assertEqual(a.legs[1].card_view, "0,N")

    def test_note(self):
        a = association_wrapper("ENGENDRER, 0N [Parent] PERSONNE, 1N [Enfant] PERSONNE")
        self.assertEqual(a.legs[0].note, "Parent")
        self.assertEqual(a.legs[1].note, "Enfant")
        self.assertEqual(a.legs[0].card_view, "0,N")
        self.assertEqual(a.legs[1].card_view, "1,N")

    def test_note_in_agregation(self):
        a = association_wrapper("ENGENDRER, /0N [Parent] PERSONNE, 1N [Enfant] PERSONNE")
        self.assertEqual(a.legs[0].note, "Parent")
        self.assertEqual(a.legs[1].note, "Enfant")
        self.assertEqual(a.legs[0].card_view, "0,N")
        self.assertEqual(a.legs[1].card_view, "1,N")

    def test_attributes(self):
        l = [
            association_wrapper("SOUTENIR, 01 ÉTUDIANT, 0N DATE: note stage, heure soutenance"),
            association_wrapper("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage , heure soutenance "),
            association_wrapper("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage,heure soutenance "),
        ]
        for a in l:
            self.assertEqual([att.label for att in a.attributes], ["note stage", "heure soutenance"])
            self.assertEqual([att.__class__ for att in a.attributes], [SimpleAssociationAttribute, SimpleAssociationAttribute])

    def test_other_card(self):
        a = association_wrapper("SOUTENIR, XX ÉTUDIANT, XX DATE: note stage")
        self.assertTrue(not a.legs[0].card_view.strip())
        self.assertTrue(not a.legs[1].card_view.strip())
        a = association_wrapper("SOUTENIR, XY ÉTUDIANT, XY DATE: note stage")
        self.assertEqual(a.legs[0].card_view, "X,Y")
        self.assertEqual(a.legs[1].card_view, "X,Y")

    def test_numbered_association_wrapper(self):
        a = association_wrapper("SOUTENIR1, 01 ÉTUDIANT, 0N DATE: note stage")
        self.assertEqual(a.name, "SOUTENIR1")
        self.assertEqual(a.name_view, "SOUTENIR")
        a = association_wrapper("SOUTENIR123, 01 ÉTUDIANT, 0N DATE: note stage")
        self.assertEqual(a.name, "SOUTENIR123")
        self.assertEqual(a.name_view, "SOUTENIR12")

    def test_df(self):
        a = association_wrapper("DF, 0N CLIENT, 11 COMMANDE")
        self.assertEqual(a.name, "DF")
        self.assertEqual(a.name_view, "DF")
        a = association_wrapper("CIF, 0N CLIENT, 11 COMMANDE", df_label="CIF")
        self.assertEqual(a.name, "CIF")
        self.assertEqual(a.name_view, "CIF")

    def test_cluster_of_one_entity(self):
        a = association_wrapper("SUIVRE, 0N DATE, /1N ÉTUDIANT")
        self.assertEqual(a.legs[0].entity_name, "DATE")
        self.assertEqual(a.legs[0].kind, "cluster_leg")
        self.assertEqual(a.legs[1].entity_name, "ÉTUDIANT")
        self.assertEqual(a.legs[1].kind, "cluster_peg")

    def test_cluster_of_two_entities(self):
        a = association_wrapper("SUIVRE, 0N DATE, /1N ÉTUDIANT, 0N ENSEIGNANT")
        self.assertEqual(a.legs[0].entity_name, "DATE")
        self.assertEqual(a.legs[0].kind, "cluster_leg")
        self.assertEqual(a.legs[1].entity_name, "ÉTUDIANT")
        self.assertEqual(a.legs[1].kind, "cluster_peg")
        self.assertEqual(a.legs[2].entity_name, "ENSEIGNANT")
        self.assertEqual(a.legs[2].kind, "cluster_leg")

    def test_cluster_with_forbidden_cardinality(self):
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.26", association_wrapper, "SUIVRE, 0N DATE, /11 ÉTUDIANT, 0N ENSEIGNANT")

    def test_cluster_without_valid_leg(self):
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.27", association_wrapper, "SUIVRE, /0N DATE, /1N ÉTUDIANT, /0N ENSEIGNANT")
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.27", association_wrapper, "SUIVRE, 11 DATE, /1N ÉTUDIANT, /0N ENSEIGNANT")

    def test_cluster_with_df(self):
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.28", association_wrapper, "SUIVRE, 0N DATE, /1N ÉTUDIANT, 11 ENSEIGNANT")


if __name__ == '__main__':
    unittest.main()
