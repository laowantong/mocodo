import gettext
import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.association import *
from mocodo.tools.parser_tools import extract_clauses


gettext.NullTranslations().install()

def association_wrapper(s, **kargs):
    Association.reset_df_counter()
    return Association(extract_clauses(s)[0], **kargs)

class ParseTest(unittest.TestCase):
    
    def test_reflexive(self):
        a = association_wrapper("ÊTRE AMI, 0N BANDIT, 0N BANDIT")
        self.assertEqual(a.bid, "ETRE_AMI")
        self.assertEqual(a.name_view, "ÊTRE AMI")
        self.assertEqual(a.attributes, [])
        for (i, leg) in enumerate(a.legs):
            self.assertEqual(leg.card_view, "0,N")
            self.assertEqual(leg.entity_bid, "BANDIT")
            self.assertEqual(leg.arrow, "")
            self.assertEqual(leg.note, None)

    def test_double(self):
        l = [
            association_wrapper("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE"),
            association_wrapper("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE:"),
        ]
        for a in l:
            self.assertEqual(a.bid, "EMPLOYER")
            self.assertEqual(a.name_view, "EMPLOYER")
            self.assertEqual(a.legs[0].card_view, "0,1")
            self.assertEqual(a.legs[0].entity_bid, "PARTICIPANT")
            self.assertEqual(a.legs[0].arrow, "")
            self.assertEqual(a.legs[0].note, None)
            self.assertEqual(a.legs[1].card_view, "0,N")
            self.assertEqual(a.legs[1].entity_bid, "ENTREPRISE")
            self.assertEqual(a.legs[1].arrow, "")
            self.assertEqual(a.legs[1].note, None)
        self.assertEqual(l[0].attributes, [])
        self.assertEqual(l[1].attributes[0].kind, "phantom")

    def test_triple(self):
        a = association_wrapper("SUIVRE, 0N DATE, 11 ÉTUDIANT, 0N ENSEIGNANT")
        self.assertEqual(a.bid, "SUIVRE")
        self.assertEqual(a.name_view, "SUIVRE")
        self.assertEqual(a.attributes, [])
        self.assertEqual(a.legs[0].card_view, "0,N")
        self.assertEqual(a.legs[0].entity_bid, "DATE")
        self.assertEqual(a.legs[0].arrow, "")
        self.assertEqual(a.legs[0].note, None)
        self.assertEqual(a.legs[1].card_view, "1,1")
        self.assertEqual(a.legs[1].entity_bid, "ETUDIANT")
        self.assertEqual(a.legs[1].arrow, "")
        self.assertEqual(a.legs[1].note, None)
        self.assertEqual(a.legs[2].card_view, "0,N")
        self.assertEqual(a.legs[2].entity_bid, "ENSEIGNANT")
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
        a = association_wrapper("ENGENDRER, 0N [Père] PERSONNE, 0N [Mère] PERSONNE, /1N [Enfant] PERSONNE")
        self.assertEqual(a.legs[0].note, "Père")
        self.assertEqual(a.legs[1].note, "Mère")
        self.assertEqual(a.legs[2].note, "Enfant")
        self.assertEqual(a.legs[0].card_view, "0,N")
        self.assertEqual(a.legs[1].card_view, "0,N")
        self.assertEqual(a.legs[2].card_view, "1,N")

    def test_attributes(self):
        l = [
            association_wrapper("SOUTENIR, 01 ÉTUDIANT, 0N DATE: note stage, heure soutenance"),
            association_wrapper("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage , heure soutenance "),
            association_wrapper("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage,heure soutenance "),
        ]
        for a in l:
            self.assertEqual([att.label for att in a.attributes], ["note stage", "heure soutenance"])
            self.assertEqual([att.__class__ for att in a.attributes], [SimpleAssociationAttribute, SimpleAssociationAttribute])

    def test_identifiers(self):
        a = association_wrapper("Réserver, 1N Client, 0N Chambre: _Date, Durée")
        self.assertEqual([att.label for att in a.attributes], ["Date", "Durée"])
        self.assertEqual([att.__class__ for att in a.attributes], [StrongAttribute, SimpleAssociationAttribute])

    def test_other_card(self):
        a = association_wrapper("SOUTENIR, XX ÉTUDIANT, XX DATE: note stage")
        self.assertTrue(not a.legs[0].card_view.strip())
        self.assertTrue(not a.legs[1].card_view.strip())
        a = association_wrapper("SOUTENIR, AB ÉTUDIANT, CD DATE: note stage")
        self.assertEqual(a.legs[0].card_view, "A,B")
        self.assertEqual(a.legs[1].card_view, "C,D")
        a = association_wrapper("SOUTENIR, XY ÉTUDIANT, XY DATE: note stage")
        self.assertEqual(a.legs[0].card_view, "Y")
        self.assertEqual(a.legs[1].card_view, "Y")

    def test_numbered_association_wrapper(self):
        a = association_wrapper("SOUTENIR1, 01 ÉTUDIANT, 0N DATE: note stage")
        self.assertEqual(a.bid, "SOUTENIR1")
        self.assertEqual(a.name_view, "SOUTENIR")
        a = association_wrapper("SOUTENIR123, 01 ÉTUDIANT, 0N DATE: note stage")
        self.assertEqual(a.bid, "SOUTENIR123")
        self.assertEqual(a.name_view, "SOUTENIR12")

    def test_df(self):
        a = association_wrapper("DF, 0N CLIENT, 11 COMMANDE")
        self.assertEqual(a.bid, "DF0")
        self.assertEqual(a.name_view, "DF")
        a = association_wrapper("CIF, 0N CLIENT, 11 COMMANDE", df_label="CIF")
        self.assertEqual(a.bid, "CIF")
        self.assertEqual(a.name_view, "CIF")
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.37", association_wrapper, "DF, 0N CLIENT, 0N COMMANDE")

    def test_cluster_of_one_entity(self):
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.51", association_wrapper, "SUIVRE, 0N DATE, /1N ÉTUDIANT")

    def test_cluster_of_two_entities(self):
        a = association_wrapper("SUIVRE, 0N DATE, /1N ÉTUDIANT, 0N ENSEIGNANT")
        self.assertEqual(a.legs[0].entity_bid, "DATE")
        self.assertEqual(a.legs[0].kind, "cluster_leg")
        self.assertEqual(a.legs[1].entity_bid, "ETUDIANT")
        self.assertEqual(a.legs[1].kind, "cluster_peg")
        self.assertEqual(a.legs[2].entity_bid, "ENSEIGNANT")
        self.assertEqual(a.legs[2].kind, "cluster_leg")


if __name__ == '__main__':
    unittest.main()
