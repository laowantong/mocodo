import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.modify import (
    pre_type,
    drain,
    explode,
    obfuscate,
    op_tk,
    randomize_cards,
    fix_cards,
    split,
)

from mocodo.argument_parser import parsed_arguments


class TestTransformers(unittest.TestCase):
    def test_obfuscate(self):
        source = """
            AYANT-DROIT: nom ayant-droit, lien
            DIRIGER, 0N EMPLOYÉ, 01 PROJET
            REQUÉRIR, 1N PROJET, 0N PIÈCE: qté requise
            PIÈCE: réf. pièce, libellé pièce
            COMPOSER, 0N [composée] PIÈCE, 0N [composante] PIÈCE: quantité

            DF1, _11 AYANT-DROIT, 0N EMPLOYÉ
            EMPLOYÉ: matricule, nom employé
            PROJET: num. projet, nom projet
            FOURNIR, 1N PROJET, 1N PIÈCE, 1N SOCIÉTÉ: qté fournie

            DÉPARTEMENT: num. département, nom département
            EMPLOYER, 11 EMPLOYÉ, 1N DÉPARTEMENT
            TRAVAILLER, 0N EMPLOYÉ, 1N PROJET
            SOCIÉTÉ: num. société, raison sociale
            CONTRÔLER, 0N< [filiale] SOCIÉTÉ, 01 [mère] SOCIÉTÉ

            (I) [Les pièces fournies par une société pour un projet font partie de celles qu'il requiert.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
        """
        params = parsed_arguments()
        params["obfuscation_source"] = "four_letter_words.txt"
        params["seed"] = 42
        actual = obfuscate.run(source, params)
        expected = """
            FEEL: turn, grin
            LAND, 0N NEAR, 01 SILK
            DEBT, 1N SILK, 0N SHOE: loss
            SHOE: poet, stir
            AUTO, 0N [slew] SHOE, 0N [tape] SHOE: knee

            CODE1, _11 FEEL, 0N NEAR
            NEAR: they, bath
            SILK: unit, haul
            DRAW, 1N SILK, 1N SHOE, 1N FOUR: duck

            ICON: golf, snap
            CLIP, 11 NEAR, 1N ICON
            AREA, 0N NEAR, 1N SILK
            FOUR: calm, away
            VARY, 0N< [urge] FOUR, 01 [pull] FOUR

            (I) [Les pièces fournies par une société pour un projet font partie de celles qu'il requiert.] ..SHOE, ->DEBT, --DRAW, SILK
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_randomize_cards(self):
        source = """
            BAKE, 0N TEND, 01 TALL
            FISH, -1N TALL, -0N TOUR: slot
            DOWN, 0N [cold] TOUR, 0N [echo] TOUR: hang
            DF1, _11 PORK, 0N TEND
            DF2, 11 DRAW, 0N BULK
            HERE, 1N TALL, 1N TOUR, 1N HOST: mask
            GOAL, 11 TEND, 1N AIDS
            ZONE, 0N TEND, /1N TALL
            LUCK, 0N< [find] HOST, 01 [hill] HOST
            AIDS, XX VARY, ?? WRAP
        """
        params = parsed_arguments()
        params["seed"] = 42
        actual = randomize_cards.run(source, params)
        expected = """
            BAKE, 01 TEND, 01 TALL
            FISH, -0N TALL, -_11 TOUR: slot
            DOWN, 01 [cold] TOUR, /1N [echo] TOUR: hang
            DF1, 01 PORK, _11 TEND
            DF2, 01 DRAW, 11 BULK
            HERE, 1N TALL, 11 TOUR, /1N HOST: mask
            GOAL, 11 TEND, 1N AIDS
            ZONE, 0N TEND, 01 TALL
            LUCK, 01< [find] HOST, 0N [hill] HOST
            AIDS, 0N VARY, 01 WRAP
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_fix_cards(self):
        source = "A, ON B, No No"
        actual = fix_cards.run(source).strip()
        expected = "A, 0N B, 0N No"
        self.assertEqual(actual, expected)

    def test_pre_type(self):
        source = """
            MEAN: wash, rest [], king [int],
            HERE, 0N NICE, 0N MEAN: wood, much [], stop [int]
            NICE: _poke, news [], , lawn [int]
        """
        actual = pre_type.run(source)
        expected = """
            MEAN: wash [], rest [], king [int],
            HERE, 0N NICE, 0N MEAN: wood [], much [], stop [int]
            NICE: _poke [], news [], , lawn [int]
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_split(self):
        source = """
            Easy, 0N Team, 0N Tire, 11 Bath
            Plea, 0N Toll, 01 Calm, 0N Path
            Busy, 0N Vast, 0N Goal, 0N Chop
            Pole, 0N Snap, 11 Vary, 0N Tide, 1N Peak
            Loop, 0N Soil, 11 Cute
            +Aunt, 01 Dirt, 1N Path, 0N Meat
            Come, -01 Suit, 1N Plea, 0N Each
            Body, 11> File, 1N< Dust, 0N Peak
            Odds, 1N Tone, 01 Peak, 0N Bold, 0N Slip: item, snap
            Chef, 1N Skip, 01 City, 0N Cell: bold [VARCHAR(42)], dead [DATE]
        """
        actual = split.run(source)
        expected = """
            Easy0, 11 Bath, 0N Team
            Easy1, 11 Bath, 0N Tire
            Plea0, 01 Calm, 0N Toll
            Plea1, 01 Calm, 0N Path
            Busy, 0N Vast, 0N Goal, 0N Chop
            Pole0, 11 Vary, 0N Snap
            Pole1, 11 Vary, 0N Tide
            Pole2, 11 Vary, 1N Peak
            Loop, 0N Soil, 11 Cute
            +Aunt0, 01 Dirt, 1N Path
            +Aunt1, 01 Dirt, 0N Meat
            Come0, -01 Suit, 1N Plea
            Come1, -01 Suit, 0N Each
            Body0, 11> File, 1N< Dust
            Body1, 11> File, 0N Peak
            Odds0, 01 Peak, 1N Tone: item, snap
            Odds1, 01 Peak, 0N Bold
            Odds2, 01 Peak, 0N Slip
            Chef0, 01 City, 1N Skip: bold [VARCHAR(42)], dead [DATE]
            Chef1, 01 City, 0N Cell
         """
        self.assertEqual(actual.strip(), expected.strip())

    def test_explosion_weakness(self):
        source = """
            Wake: tend, bath
            Bowl, 0N Wake, 1N Move, 0N Poet: turn, from
            Poet: edge, skip
            Move: aids
        """
        params = parsed_arguments()
        params["weak_explosion"] = True
        actual = explode.run(source, params)
        expected = """
            Wake: tend, bath
            Bowl: _turn, from
            Bo1, _11 Bowl, 0N Wake
            Bo2, _11 Bowl, 1N Move
            Bo3, _11 Bowl, 0N Poet
            Poet: edge, skip
            Move: aids
        """
        self.assertEqual(actual.strip(), expected.strip())   
        params["weak_explosion"] = False
        actual = explode.run(source, params)
        expected = """
            Wake: tend, bath
            Bowl: id. bowl, turn, from
            Bo1, 11 Bowl, 0N Wake
            Bo2, 11 Bowl, 1N Move
            Bo3, 11 Bowl, 0N Poet
            Poet: edge, skip
            Move: aids
        """
        self.assertEqual(actual.strip(), expected.strip())   

    def test_explosion_arity(self):
        source = """
            Edge: what, call
            Love, 0N Edge, 1N Ruin: toss, noon
            Ruin: area, slip
            Gene: five, away
            Hate, 0N Gene, 1N Rain
            Rain: iron, pose
        """
        params = parsed_arguments()
        params["explosion_arity"] = 3
        actual = explode.run(source, params)
        expected = source # no change
        self.assertEqual(actual.strip(), expected.strip())   
        params["explosion_arity"] = 2
        actual = explode.run(source, params)
        expected = """
            Edge: what, call
            Love: id. love, toss, noon
            Lo1, 11 Love, 0N Edge
            Lo2, 11 Love, 1N Ruin
            Ruin: area, slip
            Gene: five, away
            Hate: id. hate
            Ha1, 11 Hate, 0N Gene
            Ha2, 11 Hate, 1N Rain
            Rain: iron, pose
        """
        self.assertEqual(actual.strip(), expected.strip())   

    def test_drain(self):
        source = """
            Wake: tend, bath
            Bowl, 0N Wake, 11 Move: turn [type 1], from [type 2]
            Move: aids
            Hour, 01 Poet, 11 Move: chew
            Poet: edge, skip
            Draw, 01 Poet, 0N Rice: road
            Rice: easy, link
        """
        actual = drain.run(source)
        expected = """
            Wake: tend, bath
            Bowl, 0N Wake, 11 Move
            Move: aids, turn [type 1], from [type 2], chew
            Hour, 01 Poet, 11 Move
            Poet: edge, skip
            Draw, 01 Poet, 0N Rice: road
            Rice: easy, link
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_ascii(self):
        source = """
            AYANT-DROIT: nom ayant-droit, lien
            DIRIGER, 0N EMPLOYÉ, 01 PROJET
            REQUÉRIR, 1N PROJET, 0N PIÈCE: qté requise
            PIÈCE: réf. pièce, libellé pièce
            COMPOSER, 0N [composée] PIÈCE, 0N [composante] PIÈCE: quantité

            DF1, _11 AYANT-DROIT, 0N EMPLOYÉ
            EMPLOYÉ: matricule, nom employé
            PROJET: num. projet, nom projet
            FOURNIR, 1N PROJET, 1N PIÈCE, 1N SOCIÉTÉ: qté fournie

            DÉPARTEMENT: num. département, nom département
            EMPLOYER, 11 EMPLOYÉ, 1N DÉPARTEMENT
            TRAVAILLER, 0N EMPLOYÉ, 1N PROJET
            SOCIÉTÉ: num. société, raison sociale
            CONTRÔLER, 0N< [filiale] SOCIÉTÉ, 01 [mère] SOCIÉTÉ

            (I) [Les pièces fournies par une société pour un projet font partie de celles qu'il requiert.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
        """
        actual = op_tk.run(source, "ascii", "labels")
        expected = """
            AYANT-DROIT: nom ayant-droit, lien
            DIRIGER, 0N EMPLOYE, 01 PROJET
            REQUERIR, 1N PROJET, 0N PIECE: qte requise
            PIECE: ref. piece, libelle piece
            COMPOSER, 0N [composee] PIECE, 0N [composante] PIECE: quantite

            DF1, _11 AYANT-DROIT, 0N EMPLOYE
            EMPLOYE: matricule, nom employe
            PROJET: num. projet, nom projet
            FOURNIR, 1N PROJET, 1N PIECE, 1N SOCIETE: qte fournie

            DEPARTEMENT: num. departement, nom departement
            EMPLOYER, 11 EMPLOYE, 1N DEPARTEMENT
            TRAVAILLER, 0N EMPLOYE, 1N PROJET
            SOCIETE: num. societe, raison sociale
            CONTROLER, 0N< [filiale] SOCIETE, 01 [mere] SOCIETE

            (I) [Les pièces fournies par une société pour un projet font partie de celles qu'il requiert.] ..PIECE, ->REQUERIR, --FOURNIR, PROJET
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_snake(self):
        source = """
            space separated words: chien chat, élan éléphant
            underline_separated_words: chien_chat, élan_éléphant
            camelCaseWords: chienChat, élanÉléphant
            CamelCaseWords: ChienChat, ÉlanÉléphant
            dash-separated-words: chien-chat, élan-éléphant
            digitTerminated1: chien chat1, élan éléphant1
            too  many _ separators: chien__chat_, élan__Éléphant, réf. client
            +prefixedEntity: _prefixed_Attribute
            ALL UPPER CASE: CHIEN CHAT, ÉLAN ÉLÉPHANT
        """
        actual = op_tk.run(source, "snake", "labels")
        expected = """
            space_separated_words: chien_chat, élan_éléphant
            underline_separated_words: chien_chat, élan_éléphant
            camel_case_words: chien_chat, élan_éléphant
            camel_case_words: chien_chat, élan_éléphant
            dash_separated_words: chien_chat, élan_éléphant
            digit_terminated1: chien_chat1, élan_éléphant1
            too_many_separators: chien_chat, élan_éléphant, réf_client
            +prefixed_entity: _prefixed_attribute
            ALL_UPPER_CASE: CHIEN_CHAT, ÉLAN_ÉLÉPHANT
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_camel(self):
        source = """
            space separated words: chien chat, élan éléphant
            underline_separated_words: chien_chat, élan_éléphant
            camelCaseWords: chienChat, élanÉléphant
            CamelCaseWords: ChienChat, ÉlanÉléphant
            dash-separated-words: chien-chat, élan-éléphant
            digitTerminated1: chien chat1, élan éléphant1
            too  many _ separators: chien__chat_, élan__Éléphant, réf. client
            +prefixedEntity: _prefixed_Attribute
            ALL UPPER CASE: CHIEN CHAT, ÉLAN ÉLÉPHANT
        """
        actual = op_tk.run(source, "camel", "labels")
        expected = """
            spaceSeparatedWords: chienChat, élanÉléphant
            underlineSeparatedWords: chienChat, élanÉléphant
            camelCaseWords: chienChat, élanÉléphant
            CamelCaseWords: ChienChat, ÉlanÉléphant
            dashSeparatedWords: chienChat, élanÉléphant
            digitTerminated1: chienChat1, élanÉléphant1
            tooManySeparators: chienChat, élanÉléphant, réfClient
            +prefixedEntity: _prefixedAttribute
            allUpperCase: chienChat, élanÉléphant
        """
        self.assertEqual(actual.strip(), expected.strip())

if __name__ == "__main__":
    unittest.main()
