import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.rewrite import (
    _explode as explode,
    _drain as drain,
    _split as split,
)


class TestUpdater(unittest.TestCase):
    def test_split(self):
        source = """
            Easy, 0N Team, 0N Tire, 11 Bath: foo, bar
            Plea, 0N Toll, 01 Calm, 0N Path
            Busy, 0N Vast, 0N Goal, 0N Chop
            Pole, 0N Snap, 11 Vary, 0N Tide, 1N Peak
            Loop, 0N Soil, 11 Cute
            +Aunt, 01 Dirt, 1N Path, 0N Meat
            Come, -01 Suit, 1N Plea, 0N Each
            Body, 11> File, 1N< Dust, 0N Peak
            Odds, 1N Tone, 01 Peak, 0N Bold, 0N Slip: item, snap
            Chef, 1N Skip, 01 City, 0N Cell: bold [VARCHAR(42)], dead [DATE]
            Victima, 11 Tradidit, 01 Periculosum, 0N Superbiam
            Clamorem, 01 Priorum, 0N Iret, 11 Loquatur
            Tuam, 11 Initiis, 01 Genua, 01 Haesit
            Commemorat, 01 Furius, 01 Sermonis, 01 Panem
            Anus, 11 Dianam, 11 Emplastrum, 1N Piscium
        """
        actual = split.run(source)
        expected = """
            Easy0, 11 Bath, 0N Team: foo, bar
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
            Victima0, 11 Tradidit, 01 Periculosum
            Victima1, 11 Tradidit, 0N Superbiam
            Clamorem0, 11 Loquatur, 01 Priorum
            Clamorem1, 11 Loquatur, 0N Iret
            Tuam0, 11 Initiis, 01 Genua
            Tuam1, 11 Initiis, 01 Haesit
            Commemorat0, 01 Furius, 01 Sermonis
            Commemorat1, 01 Furius, 01 Panem
            Anus0, 11 Dianam, 11 Emplastrum
            Anus1, 11 Dianam, 1N Piscium
         """
        self.assertEqual(actual.strip(), expected.strip())

    def test_explode_weak(self):
        source = """
            Wake: tend, bath
            Bowl, 0N Wake, 1N Move, 0N Poet: turn, from
            Poet: edge, skip
            Move: aids
        """
        actual = explode.run(source, {"weak": True})
        expected = """
            Wake: tend, bath
            Bowl: _turn, from
            DF, _11 Bowl, 0N Wake
            DF, _11 Bowl, 1N Move
            DF, _11 Bowl, 0N Poet
            Poet: edge, skip
            Move: aids
        """
        self.assertEqual(actual.strip(), expected.strip())   
        actual = explode.run(source)
        expected = """
            Wake: tend, bath
            Bowl: id. bowl, turn, from
            DF, 11 Bowl, 0N Wake
            DF, 11 Bowl, 1N Move
            DF, 11 Bowl, 0N Poet
            Poet: edge, skip
            Move: aids
        """
        self.assertEqual(actual.strip(), expected.strip())   

    def test_explode_arity(self): # TODO: more cases
        source = """
            Edge: what, call
            Love, 0N Edge, 1N Ruin: toss, noon
            Ruin: area, slip
            Gene: five, away
            Hate, 0N Gene, 1N Rain
            Rain: iron, pose
        """
        actual = explode.run(source, {"arity": "3"})
        expected = source # no change
        self.assertEqual(actual.strip(), expected.strip())   
        actual = explode.run(source, {"arity": "2"})
        expected = """
            Edge: what, call
            Love: id. love, toss, noon
            DF, 11 Love, 0N Edge
            DF, 11 Love, 1N Ruin
            Ruin: area, slip
            Gene: five, away
            Hate: id. hate
            DF, 11 Hate, 0N Gene
            DF, 11 Hate, 1N Rain
            Rain: iron, pose
        """
        self.assertEqual(actual.strip(), expected.strip())   

    def test_explode_cluster(self):
        source = """
            Date: Date
            Réserver, /1N Client, 1N Chambre, 0N Date: Durée
            Chambre: Numéro, Prix
            Client: Id. client, Nom client
        """
        actual = explode.run(source, {"weak": True})
        expected = """
            Date: Date
            Réserver: _Durée
            DF, 11 Réserver, 1N Client
            DF, _11 Réserver, 1N Chambre
            DF, _11 Réserver, 0N Date
            Chambre: Numéro, Prix
            Client: Id. client, Nom client
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


if __name__ == "__main__":
    unittest.main()
