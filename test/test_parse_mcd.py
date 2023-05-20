import os
from pathlib import Path
import unittest
import pprint

os.system("python -m lark.tools.standalone --compress mocodo/resources/grammar.lark > mocodo/parse_mcd.py")
__import__("sys").path[0:0] = ["mocodo"]

from mocodo.parse_mcd import Lark_StandAlone
from mocodo.parse_mcd import UnexpectedInput, UnexpectedToken
from mocodo.parser_tools import reconstruct_source, parse_source, extract_clauses

parser = Lark_StandAlone()

valid_lines = r"""
:
:::
:  :  :
   :  :  :
   % commented
% commented %
AYANT-DROIT: nom ayant-droit, lien
DIRIGER, 0N EMPLOYÉ, 01 PROJET
REQUÉRIR, 1N PROJET, 0N PIÈCE: qté requise
COMPOSER, 0N [composée] PIÈCE, 0N [composante] PIÈCE: quantité
DF1, _11 AYANT-DROIT, 0N EMPLOYÉ
FOURNIR, 1N PROJET, 1N PIÈCE, 1N SOCIÉTÉ: qté fournie
CONTRÔLER, 0N< [filiale] SOCIÉTÉ, 01 [mère] SOCIÉTÉ
DF, 0N> CLIENT, 11 COMMANDE
GRATTE-CIEL: latitude, _longitude, nom, hauteur, année de construction
Peut recevoir, 1N> Groupe sanguin, 1N< Groupe sanguin
Engendre, 0N< Personne, 22> Personne
Agent 0070: bar
DF42, 11 Agent 0070, 1N Agent1
Agent1: bar
DF, _11 ŒUVRE, _11 EXEMPLAIRE
Réserver, /1N Client, 1N Chambre, 0N Date: Durée
LIGULA, 0N LACUS, /1N EROS, 0N TELLUS, 0N CONSEQUAT: metus
Réserver: _Durée
+LIGULA, 01 LACUS, 1N EROS: metus
PASSER, 0N [Un client peut passer un nombre quelconque de commandes.] CLIENT, 11 [Toute commande est passée par un en un seul client.] COMMANDE
INCLURE, 1N [Une commande peut inclure plusieurs produits distincts, et en inclut au moins un.] COMMANDE, 0N [Certains produits ne sont jamais commandés, d'autres le sont plusieurs fois.] PRODUIT: Quantité
CLIENT: 
CLIENT: ,          ,,
COMMANDE: ,               ,
PRODUIT: ,            , 
Unit, 1N Draw, 11 Folk: Peer, Tour, 
PASSER, XX CLIENT, XX COMMANDE
INCLURE, XX COMMANDE, XX PRODUIT: 
ŒUVRE: 612.NAT.34, J'apprends à lire à mes souris blanches, mai 1975
EXEMPLAIRE2: 1, bon état, 12/6/1975
EXEMPLAIRE3: 2, bon état, 1/8/1977
EXEMPLAIRE4: 3, reliure rongée, 3/4/2005
DF1, -1N ŒUVRE, -_11 EXEMPLAIRE1
+Prof: Num. prof, Nom prof
COMMANDE: Num commande, Date, Montant, #Réf. client>CLIENT>Réf. client
INCLURE: #Num commande>COMMANDE>Num commande, _#Réf. produit>PRODUIT>Réf. produit, Quantité
CLIENT: Réf. client [varchar(8)], Nom [varchar(20)], Adresse [varchar(40)]
INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
PARTICIPANT: numero [], nom, adresse [type3]
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
DIRIGER   ,    0N    EMPLOYÉ   ,    01    PROJET   
() [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
(II) ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
(III) [bla bla.]
(IV) 
(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 12.5, 30
(II) ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 12.5, 30
(III) [bla bla.]: 12.5, 30
(IV) : 12.5, 30
(I) [bla bla.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 12.5
(II) ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET: 12.5
(III) [bla bla.]: 12.5
(IV) : 12.5
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
"""

invalid_lines = """
(A) --Lorem, >Ipsum: 30, 90
: foobar
DIRIGER,
, 01 PROJET
(I) : 1, 2, 3
(I) : 
-ABC: 
_FOOBAR: 
FOOBAR
BACK\\SLASH:
DIRIGER, 0 EMPLOYÉ, 01 PROJET
DIRIGER, 0 EMPLOYÉ, 01 PROJET: biz, buz
/ANYTHING\\ Personne => Homme, Femme: sexe
PARTICIPANT: numero [, nom, adresse
"""

line = "-" * 80
path = Path("test/snapshots/parsed.txt")
with path.open(mode="w") as file:
    for source in valid_lines.splitlines():
        file.write(f'{line}\n{source}\n')
        tree = parse_source(source).pretty()
        file.write(f'{line}{tree}'.strip())
        file.write(f'\n{line}\n')
        clauses = extract_clauses(source)
        output = pprint.pformat(clauses, sort_dicts=False)
        file.write(f'{output}\n\n')
    for source in invalid_lines.splitlines():
        if not source:
            continue
        try:
            tree = parse_source(source).pretty()
        except UnexpectedInput as e:
            pinpointed_text = e.get_context(source)
            file.write(f'{line}\n{pinpointed_text}')
            if isinstance(e, UnexpectedToken):
                file.write(f'Unexpected token "{repr(e.token)}" at line {e.line}, column {e.column}.\n')
                file.write(f'Expected: {sorted(e.expected)}.\n')
        else:
            raise Exception(f"Expected error for:\n{source}")


class TestReconstructSource(unittest.TestCase):

    def test_reconstruct_source(self):
        for source in valid_lines.splitlines():
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
        for (raw_line, clause) in zip(source.splitlines(), clauses):
            self.assertEqual(clause["source"].lstrip(), raw_line.lstrip())


if __name__ == '__main__':
    unittest.main()
