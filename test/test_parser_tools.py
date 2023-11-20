from pathlib import Path
import re
import gettext
import unittest
import pprint

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.parse_mcd import Lark_StandAlone, UnexpectedToken
from mocodo.tools.parser_tools import reconstruct_source, parse_source, extract_clauses
from mocodo.mocodo_error import MocodoError

gettext.NullTranslations().install()

parser = Lark_StandAlone()

valid_lines = r"""
:
:::
:  :  :
   :  :  :
   % commented
% commented %
  % foo\\ , %  foo  /TX\\
AYANT-DROIT: nom ayant-droit, lien
DIRIGER, 0N EMPLOYÉ, 01 PROJET
REQUÉRIR, 1N PROJET, 0N PIÈCE: qté requise
COMPOSER, 0N [composée] PIÈCE, 0N [composante] PIÈCE: quantité
DF, _11 AYANT-DROIT, 0N EMPLOYÉ
FOURNIR, 1N PROJET, 1N PIÈCE, 1N SOCIÉTÉ: qté fournie
CONTRÔLER, 0N< [filiale] SOCIÉTÉ, 01 [mère] SOCIÉTÉ
DF, 0N> CLIENT, 11 COMMANDE
GRATTE-CIEL: latitude, _longitude, nom, hauteur, année de construction
Peut recevoir, 1N> Groupe sanguin, 1N< Groupe sanguin
Engendre, 0N< Personne, 22> Personne
Agent 0070: bar
DF4, 11 Agent 0070, 1N Agent1
Agent1: bar
DF, _11 ŒUVRE, _11 EXEMPLAIRE
Réserver, /1N Client, 1N Chambre, 0N Date: Durée
LIGULA, 0N LACUS, /1N EROS, 0N TELLUS, 0N CONSEQUAT: metus
Réserver: _Durée
+LIGULA, 01 LACUS, 1N EROS: metus
-LIGULA, 01 LACUS, 1N EROS: metus
PASSER, 0N [Un client peut passer un nombre quelconque de commandes.] CLIENT, 11 [Toute commande est passée par un en un seul client.] COMMANDE
INCLURE, 1N [Une commande peut inclure plusieurs produits distincts, et en inclut au moins un.] COMMANDE, 0N [Certains produits ne sont jamais commandés, d'autres le sont plusieurs fois.] PRODUIT: Quantité
CLIENT: 
CLIENT: ,          ,,
COMMANDE: ,               ,
PRODUIT: ,            , 
MEAN: wash, rest, king,
HERE, 0N NICE, 0N MEAN: wood, much, , stop
NICE: _poke, news, , lawn
Unit, 1N Draw, 11 Folk: Peer, Tour, 
PASSER, XX CLIENT, XX COMMANDE
INCLURE, XX COMMANDE, XX PRODUIT: 
ŒUVRE: 612.NAT.34, J'apprends à lire à mes souris blanches, mai 1975
EXEMPLAIRE2: 1, bon état, 12/6/1975
EXEMPLAIRE3: 2, bon état, 1/8/1977
EXEMPLAIRE4: 3, reliure rongée, 3/4/2005
DF, -1N ŒUVRE, -_11 EXEMPLAIRE1
+Prof: Num. prof, Nom prof
-Prof: Num. prof, Nom prof
Enseignant: num. ens. [numéro identifiant un enseignant], nom ens. [nom enseignant], tél. ens. [téléphone enseignant]
COMMANDE: Num commande, Date, Montant, #Réf. client>CLIENT>Réf. client
COMMANDE: Num commande, Date, Montant, #Réf. client > CLIENT > Réf. client
INCLURE: #Num commande>COMMANDE>Num commande, _#Réf. produit>PRODUIT>Réf. produit, Quantité
INCLURE: #Num commande > COMMANDE > Num commande, _#Réf. produit > PRODUIT > Réf. produit, Quantité
CLIENT: Réf. client [varchar(8)], Nom [varchar(20)], Adresse [varchar(40)]
INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
PARTICIPANT: numero [], nom, adresse [type3]
COMMANDE: Num commande, Date, Montant, #Réf. client!>CLIENT>Réf. client
COMMANDE: Num commande, Date, Montant, Réf. client!
L33T, 0N> H4X0R, 0N< H4X0R
L33T123, 0N> H4X0R12, 0N< H4X0R0
   AYANT-DROIT: nom ayant-droit, lien
   DIRIGER, 0N EMPLOYÉ, 01 PROJET
   REQUÉRIR, 1N PROJET, 0N PIÈCE: qté requise
DIRIGER, EMPLOYÉ, PROJET
A, B, C
Foo, Bar
DIRIGER, EMPLOYÉ, PROJET: biz, buz
A, B, C: biz, buz
Foo, Bar: biz, buz
AYANT-DROIT   :   nom ayant-droit   ,   lien   
DIRIGER   ,    0N    EMPLOYÉ   ,    01    PROJET   : fizz,  buzz   
AYANT-DROIT  :  nom ayant-droit  ,  lien  
DIRIGER  ,  0N  EMPLOYÉ  ,  01  PROJET  : fizz, buzz  
AYANT-DROIT	 :	 nom ayant-droit	 ,	 lien	 
DIRIGER	 ,		0N		EMPLOYÉ	 ,		01		PROJET	 : fizz,	buzz	 
() [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
(II) ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
(III) [bla bla.]
(IV) 
(])
(+)
(/)
(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 12.5, 30
(II) ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 12.5, 30
(III) [bla bla.]: 12.5, 30
(IV) : 12.5, 30
(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: FOO, 30
(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 12.5, BAR
(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: FOO, BAR
(IV) : 12.5, 30
(A) --Lorem, .....Ipsum, -Dolor: 30, 10
(B) ->Dolor, <-->Sit, -->Amet: 69, 10
(XX) ->foo, -->foo, -> foo, --> foo
(I) ->Stocker, ..Dépôt, ..Article, --Composer, --Louer
/XT\ Personne ==> Homme, Femme: sexe
/XT1\\ Personne <= Homme, Femme: sexe
/XT\\ Personne => Homme, Femme: sexe
/T\\ Personne <= Homme, Femme: sexe
/T\\ Personne => Homme, Femme: sexe
/X\\ Personne <= Homme, Femme: sexe
/X\\ Personne => Homme, Femme: sexe
/\\ Personne <= Homme, Femme: sexe
/\\ Personne => Homme, Femme: sexe
/1\\ FOO => BAR
/T\\foo==>foo11
Étudiant: num, 1_nom, 1_prénom, adresse, 2_mail
Étudiant: 0_num, 1_nom, 1_prénom, adresse, 2_mail
Position: 0_latitude, 0_longitude, altitude
Foo: bar, 1_baz, 21_qux, 123_quux
Réserver, 1N Client, 0N Chambre: _date, durée
""".splitlines()

line = "-" * 80
path = Path("test/test_parser_tools_snapshot.txt")
with path.open(mode="w") as file:
    for source in valid_lines:
        file.write(f"{line}\n{source}\n")
        tree = parse_source(source).pretty()
        file.write(f"{line}{tree}".strip())
        file.write(f"\n{line}\n")
        clauses = extract_clauses(source)
        output = pprint.pformat(clauses, sort_dicts=False)
        file.write(f"{output}\n\n")

def fuzzer(seed=0):
    import random
    random.seed(seed)
    for _ in range(50):
        (left, right) = random.sample(valid_lines, 2)
        source = f"{left[:random.randint(0, len(left))]}{right[random.randint(0, len(right)):]}"
        try:
            tree = parse_source(source)
            print(source)
        except Exception as error:
            print(source)
            print(error)
        input()

# fuzzer(4)

mocodo_errors = [
    *[(501, c) for c in "0123456789!#$&')*,.;<=>?@[\\]^_`{|}~"],
    *[(501, f" {c}") for c in "0123456789!#$&')*,.;<=>?@[\\]^_`{|}~"],
    (501, ": foobar"),
    (501, " : foobar"),
    (502, "AYANT-: nom ay, lien"),
    (502, "FOO, 0N Bar, 1N Biz [bla]"),
    (502, "FOO, 0N Bar, 1N Biz [bla], 0N Buz"),
    (502, " foo /TX\\#  ]  #/ "),
    (502, "BACK\\SLASH:"),
    (502, " foo_11<11_ ]<-->]foo"),
    (503, "FOOBAR"),
    (503, "  FOOBAR>"),
    (503, "  FOOBAR    >"),
    (503, "  FOOBAR+"),
    (505, "/T\\, foobar"),
    (506, "DIRIGER, 0 EMPLOYÉ, 01 PROJET"),
    (506, "DIRIGER, 0 EMPLOYÉ, 01 PROJET: biz, buz"),
    (506, "DIRIGER, 0NV"),
    (507, "/ANYTHING\\ Personne => Homme, Femme: sexe"),
    (507, "/X12\\ Personne => Homme, Femme: sexe"),
    (507, "/1N\\"),
    (508, "(I) : 1, 2, 3"),
    (508, "(I) : 1, 2,"),
    (509, "DIRIGER,"),
    (509, "DIRIGER,    "),
    (510, "(I) : "),
    (510, "(I) ->Foo ..Bar : "),
    (510, "(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 12.5, "),
    (510, "(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: FOOBAR, "),
    (510, "(A) : Ipsum, --Lorem: 30, 90"),
    (511, " +"),
    (511, "   +#   "),
    (511, "/T\\ \\.. ,\\foo"),
    (511, "+..==>"),
    (511, " /TX\\ foo -> .bar"),
    (512, "PARTICIPANT: numero [, nom, adresse"),
    (514, "(IIII)"),
    (514, "(    )"),
    (514, "(    )"),
    (515, "(A) --Lorem, >Ipsum: 30, 90"),
    (515, "(A) --Lorem, : Ipsum: 30, 90"),
    (515, "(A) --Lorem 30, 90"),
    (516, "(A) >Ipsum, --Lorem: 30, 90"),
    (516, "())"),
    (516, "((I))"),
    (517, "/TX\\ foo bar "),
    (518, "COMMANDE: Num commande, Date, Montant, #Réf. client->CLIENT->Réf. client"),
    (518, "INCLURE: #Num commande->COMMANDE->Num commande, _#Réf. produit->PRODUIT->Réf. produit, Quantité"),
    (519, "(A) ->Ipsum ->Lorem: 30, 90"),
    (500, "FOOBAR: foo, /bar"),
    (500, "FOO, 1N Bar: -->Amet"),
    (521, "FOOBAR: foo>bar, biz"),
    (522, "FOO: #bar, biz"),
    (522, "FOO: #bar!, biz"),
    (522, "FOO: #bar"),
    (522, "FOO: #bar!"),
    (522, "FOO: biz, #bar"),
    (522, "FOO: #bar>buzz, biz"),
    (522, "FOO: #bar>buzz!, biz"),
    (522, "FOO: #bar!>buzz, biz"),
    (522, "FOO: #bar>buzz"),
    (522, "FOO: biz, #bar>buzz"),
    (523, "FOO: #bar>buzz>, biz"),
    (523, "FOO: #bar>buzz>"),
    (523, "FOO: biz, #bar>buzz>  "),
    (524, "DIRIGER, 0N EMPLOYÉ > PRODUIT, Quantité"),
    (525, "(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 12.5"),
    (526, "(A) ->Ipsum, ->Lorem: 30, 9N"),
    (527, "(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 3,14 3,14"),
    (528, "FOO: bar!?, biz"),
]

class MocodoErrorTest(unittest.TestCase):
    def test_mocodo_errors(self):
        for n, source in mocodo_errors:
            try:
                parse_source(source)
            except MocodoError as e:
                actual_error_number = re.search(r"\d+", str(e)).group()
                assert actual_error_number == str(n), f"Expected error {n} for:\n{source}"
            except Exception as e:
                print(source)
                pin = e.get_context(source)
                print(f"{line}\n{source}\n{line}\n{pin}")
                if isinstance(e, UnexpectedToken):
                    print(f'Unexpected token "{repr(e.token)}" at line {e.line}, column {e.column}.')
                    print(f"Expected: {set(e.expected)}.\n")
                assert False
            else:
                assert False, f"\n\nExpected Mocodo Error {n} for:\n{source}"


class TestReconstructSource(unittest.TestCase):
    def test_reconstruct_source(self):
        for source in valid_lines:
            if not source:
                continue
            tree = parse_source(source)
            new_source = reconstruct_source(tree)
            self.assertEqual(source.strip(), new_source.strip())

    def test_alignment(self):
        source = """
            AYANT-DROIT: nom ayant-droit, lien
            DIRIGER, 0N EMPLOYÉ, 01 PROJET
            
            
            REQUÉRIR, 1N PROJET, 0N PIÈCE: qté requise
            ::

            % comment
            
            PIÈCE: réf. pièce, libellé pièce

              (I) [Les pièces fournies par une société pour un projet font partie de celles qu'il requiert.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET        
        """
        clauses = extract_clauses(source)
        for raw_line, clause in zip(source.splitlines(), clauses):
            self.assertEqual(clause["source"].lstrip(), raw_line.lstrip())

if __name__ == "__main__":
    unittest.main()
