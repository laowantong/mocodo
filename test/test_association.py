import gettext
import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.association import *


gettext.NullTranslations().install()

class parse_test(unittest.TestCase):
    
    def test_reflexive(self):
        a = Association(u"ÊTRE AMI, 0N BANDIT, 0N BANDIT")
        self.assertEqual(a.name, u"ÊTRE AMI")
        self.assertEqual(a.name_view, u"ÊTRE AMI")
        self.assertEqual(a.attributes, [])
        for (i, leg) in enumerate(a.legs):
            self.assertEqual(leg.card_view, "0,N")
            self.assertEqual(leg.entity_name, "BANDIT")
            self.assertEqual(leg.arrow, "")
            self.assertEqual(leg.note, None)

    def test_double(self):
        l = [
            Association("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE"),
            Association("EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE:"),
            Association("EMPLOYER,01 PARTICIPANT,0N ENTREPRISE"),
            Association(" EMPLOYER , 01 PARTICIPANT, 0N   ENTREPRISE "),
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
        a = Association("SUIVRE, 0N DATE, 11 ÉTUDIANT, 0N ENSEIGNANT")
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
        a = Association("EMPLOYER, 01> PARTICIPANT, 0N< ENTREPRISE")
        self.assertEqual(a.legs[0].arrow, ">")
        self.assertEqual(a.legs[1].arrow, "<")
        self.assertEqual(a.legs[0].card_view, "0,1")
        self.assertEqual(a.legs[1].card_view, "0,N")

    def test_label(self):
        a = Association("ENGENDRER, 0N [Parent] PERSONNE, 1N [Enfant] PERSONNE")
        self.assertEqual(a.legs[0].note, "Parent")
        self.assertEqual(a.legs[1].note, "Enfant")
        self.assertEqual(a.legs[0].card_view, "0,N")
        self.assertEqual(a.legs[1].card_view, "1,N")

    def test_attributes(self):
        l = [
            Association("SOUTENIR, 01 ÉTUDIANT, 0N DATE: note stage, heure soutenance"),
            Association("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage , heure soutenance "),
            Association("SOUTENIR, 01 ÉTUDIANT, 0N DATE:  note stage,heure soutenance "),
        ]
        for a in l:
            self.assertEqual([att.label for att in a.attributes], ["note stage", "heure soutenance"])
            self.assertEqual([att.__class__ for att in a.attributes], [SimpleAssociationAttribute, SimpleAssociationAttribute])

    def test_other_card(self):
        a = Association("SOUTENIR, XX ÉTUDIANT, XX DATE: note stage")
        self.assertTrue(not a.legs[0].card_view.strip())
        self.assertTrue(not a.legs[1].card_view.strip())
        a = Association("SOUTENIR, XY ÉTUDIANT, XY DATE: note stage")
        self.assertEqual(a.legs[0].card_view, "X,Y")
        self.assertEqual(a.legs[1].card_view, "X,Y")

    def test_numbered_association(self):
        a = Association("SOUTENIR1, 01 ÉTUDIANT, 0N DATE: note stage")
        self.assertEqual(a.name, "SOUTENIR1")
        self.assertEqual(a.name_view, "SOUTENIR")

    def test_df(self):
        a = Association("DF, 0N CLIENT, 11 COMMANDE")
        self.assertEqual(a.name, "DF")
        self.assertEqual(a.name_view, "DF")
        a = Association("CIF, 0N CLIENT, 11 COMMANDE", df_label="CIF")
        self.assertEqual(a.name, "CIF")
        self.assertEqual(a.name_view, "CIF")

    def test_included_in_foreign_key(self):
        a = Association("SUIVRE, 0N DATE, 11 /ÉTUDIANT, 0N ENSEIGNANT")
        self.assertEqual(a.legs[0].entity_name, "DATE")
        self.assertEqual(a.legs[0].may_identify, True)
        self.assertEqual(a.legs[2].entity_name, "ENSEIGNANT")
        self.assertEqual(a.legs[2].may_identify, True)
        self.assertEqual(a.legs[1].entity_name, "ÉTUDIANT")
        self.assertEqual(a.legs[1].may_identify, False)

    def test_input_errors(self):
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.2", Association, "EMPLOYER, PARTICIPANT, 0N ENTREPRISE",)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.2", Association, "EMPLOYER, 1 PARTICIPANT, 0N ENTREPRISE",)

    def test_backslash_suppression(self):
        a = Association(r"BUZZ\, 01 FO\tO, 0N \tBAR\t")
        self.assertEqual(a.name, "BUZZ")
        self.assertEqual(a.name_view, "BUZZ")
        self.assertEqual(a.legs[0].entity_name, "FOtO")
        self.assertEqual(a.legs[1].entity_name, "tBARt")
        a = Association("BUZZ\, 01 FO\tO, 0N \tBAR\t")
        self.assertEqual(a.name, "BUZZ")
        self.assertEqual(a.name_view, "BUZZ")
        self.assertEqual(a.legs[0].entity_name, "FO\tO")
        self.assertEqual(a.legs[1].entity_name, "BAR")

    def test_backslash_conservation(self):
        a = Association(r"/XT\ FOO => BAR")
        self.assertEqual(a.name, "XT")
        self.assertEqual(a.name_view, "XT")
        self.assertEqual(a.legs[0].entity_name, "FOO")
        self.assertEqual(a.legs[1].entity_name, "BAR")
        self.assertEqual(a.kind, "inheritance: =>")

if __name__ == '__main__':
    unittest.main()
