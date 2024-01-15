import gettext
import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.argument_parser import parsed_arguments
from mocodo.mcd import *

gettext.NullTranslations().install()

params = parsed_arguments([])

style = {
    "cartouche_text_height_ratio" : 0.85,
    "card_text_height_ratio"      : 0.85,
    "df_text_height_ratio"        : 1.1,
    "attribute_text_height_ratio" : 0.65,
    "line_skip_height"            : 0,
    "card_baseline"               : 3,
    "card_underline_skip_height"  : -2,
    "underline_skip_height"       : -3,
    "underline_depth"             : 1,
    "card_underline_depth"        : 1,
    "dash_width"                  : 4,
    "margin"                 : 9,
    "box_stroke_depth"            : 1.5,
    "inner_stroke_depth"          : 1.5,
    "rect_margin_width"           : 8,
    "rect_margin_height"          : 6,
    "round_rect_margin_width"     : 7,
    "round_rect_margin_height"    : 5,
    "round_corner_radius"         : 14,
    "leg_stroke_depth"            : 1,
    "card_margin"                 : 5,
    "arrow_width"                 : 12,
    "arrow_half_height"           : 6,
    "arrow_axis"                  : 8,
    "note_overlay_height"   : 40,
    "note_baseline"         : 24,
    "entity_cartouche_font"       : None,
    "association_cartouche_font"  : None,
    "entity_attribute_font"       : None,
    "association_attribute_font"  : None,
    "card_font"                   : None,
    "label_font"                  : None,
    "note_font"             : None
}

def stub_for_get_font_metrics(s):
    stub_for_get_font_metrics.get_pixel_width = lambda s: 5 * len(s)
    stub_for_get_font_metrics.get_pixel_height = lambda: 10
    return stub_for_get_font_metrics

def get_dimensions(mcd, verbose=False):
    mcd.calculate_size(style)
    result = []
    log = ["["]
    for box in mcd.boxes:
        log.append("{'bid': %s, " % repr(box.bid))
        d = {"bid": box.bid}
        for key in "xywh":
            d[key] = getattr(box, key)
            log.append("'%s': %s, " % (key, d[key]))
        log[-1] = log[-1][:-2]
        log.append("},\n")
        result.append(d)
    log[-1] = log[-1][:-2]
    log.append("]")
    if verbose:
        print("".join(log))
    return result

class McdGeometryTest(unittest.TestCase):

    def test_simplest_mcd(self):
        clauses = [
            "My entity: first, second",
        ]
        mcd = Mcd("\n".join(clauses), stub_for_get_font_metrics, **params)
        self.assertEqual(get_dimensions(mcd), [{'bid': 'MY_ENTITY', 'x': 9, 'y': 9, 'w': 62, 'h': 54}])
    
    def test_read_me_mcd(self):
        clauses = [
            "DF, 11 Élève, 1N Classe",
            "Classe: Num. classe, Num. salle",
            "Faire Cours, 1N Classe, 1N Prof: Vol. horaire",
            "Catégorie: Code catégorie, Nom catégorie",
            "",
            "Élève: Num. élève, Nom élève",
            "Noter, 1N Élève, 0N Prof, 0N Matière, 1N Date: Note",
            "Prof: Num. prof, Nom prof",
            "Relever, 0N Catégorie, 11 Prof",
            "",
            "Date: Date",
            "Matière: Libellé matière",
            "Enseigner, 11 Prof, 1N Matière",
        ]
        mcd = Mcd("\n".join(clauses), stub_for_get_font_metrics, **params)
        self.assertEqual(get_dimensions(mcd), [
            {'bid': 'DF0', 'x': 30, 'y': 24, 'w': 24, 'h': 24},
            {'bid': 'CLASSE', 'x': 95, 'y': 9, 'w': 72, 'h': 54},
            {'bid': 'FAIRE_COURS', 'x': 195, 'y': 15, 'w': 74, 'h': 42},
            {'bid': 'CATEGORIE', 'x': 294, 'y': 9, 'w': 86, 'h': 54},
            {'bid': 'ELEVE', 'x': 9, 'y': 83, 'w': 66, 'h': 54},
            {'bid': 'NOTER', 'x': 111, 'y': 89, 'w': 40, 'h': 42},
            {'bid': 'PROF', 'x': 201, 'y': 83, 'w': 62, 'h': 54},
            {'bid': 'RELEVER', 'x': 312, 'y': 89, 'w': 50, 'h': 42},
            {'bid': 'DATE', 'x': 24, 'y': 157, 'w': 36, 'h': 44},
            {'bid': 'MATIERE', 'x': 85, 'y': 157, 'w': 92, 'h': 44},
            {'bid': 'ENSEIGNER', 'x': 202, 'y': 158, 'w': 60, 'h': 42},
            {'bid': 'PHANTOM_#1', 'x': 337, 'y': 179, 'w': 0, 'h': 0}
        ])
    
    def test_mocodo_online_mcd(self):
        clauses = [
            "PEUT VIVRE DANS, 1N ESPÈCE, 1N ENCLOS: nb. max. congénères",
            "ENCLOS: num. enclos",
            "OCCUPE, 1N ANIMAL, 1N PÉRIODE, 1N ENCLOS",
            "PÉRIODE: date début, _date fin",
            "",
            "ESPÈCE: code espèce, libellé",
            "DF, 0N ESPÈCE, _11 ANIMAL",
            "ANIMAL: nom, sexe, date naissance, date décès",
            "A MÈRE, 01 ANIMAL, 0N> [mère] ANIMAL",
            "",
            "PEUT COHABITER AVEC, 0N ESPÈCE, 0N [commensale] ESPÈCE: nb. max. commensaux",
            ":",
            "A PÈRE, 0N ANIMAL, 0N> [père présumé] ANIMAL",
            "-INVISIBLE:"
        ]
        mcd = Mcd("\n".join(clauses), stub_for_get_font_metrics, **params)
        self.assertEqual(get_dimensions(mcd), [
            {'bid': 'PEUT_VIVRE_DANS', 'x': 9, 'y': 15, 'w': 110, 'h': 42},
            {'bid': 'ENCLOS', 'x': 144, 'y': 14, 'w': 72, 'h': 44},
            {'bid': 'OCCUPE', 'x': 241, 'y': 15, 'w': 44, 'h': 42},
            {'bid': 'PERIODE', 'x': 320, 'y': 9, 'w': 66, 'h': 54},
            {'bid': 'ESPECE', 'x': 28, 'y': 93, 'w': 72, 'h': 54},
            {'bid': 'DF0', 'x': 168, 'y': 108, 'w': 24, 'h': 24},
            {'bid': 'ANIMAL', 'x': 220, 'y': 83, 'w': 86, 'h': 74},
            {'bid': 'A_MERE', 'x': 331, 'y': 99, 'w': 44, 'h': 42},
            {'bid': 'PEUT_COHABITER_AVEC', 'x': 9, 'y': 177, 'w': 110, 'h': 42},
            {'bid': 'PHANTOM_#1', 'x': 180, 'y': 198, 'w': 0, 'h': 0},
            {'bid': 'A_PERE', 'x': 241, 'y': 177, 'w': 44, 'h': 42},
            {'bid': 'INVISIBLE', 'x': 353, 'y': 198, 'w': 0, 'h': 0}
        ])
    
if __name__ == '__main__':
    unittest.main()
