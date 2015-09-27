#!/usr/bin/python
# encoding: utf-8

import unittest
from mocodo.relations import *
from mocodo.mcd import Mcd
import json
import codecs
from mocodo.argument_parser import parsed_arguments

clauses = """
PASS, 11 PEAK, 01 GAME: rain
GAME: glad, oven
SHED, 0N SLOW, 0N GAME, 0N DIET: free
SLOW: else, line
CORD, 1N /SLOW, 01 LOCK: left
LOCK: bury

PEAK: amid, salt
BOOT, 01 GAME, 0N GAME: snap
DIET: iron, cell
SOUL, 0N DIET, 0N SLOW: joke
ALLY, 1N ODDS, 11 SLOW: whom
FUND, 1N LOCK, 1N /ODDS: dump

DENY, 0N QUIT, 0N QUIT: hers
QUIT: rich, milk
MYTH, 11 DIET, 0N QUIT: clip
POEM: cute, farm
HANG, 1N POEM, _11 ODDS: golf
ODDS: echo
""".split("\n")

params = parsed_arguments()
params["title"] = "Untitled"
params["guess_title"] = False
t = Relations(Mcd(clauses, params), params)

class relationTemplatesTest(unittest.TestCase):
    


    def test_diagram(self):
        template = json.loads(codecs.open("mocodo/relation_templates/diagram.json").read())
        expected = u"""
            %%mocodo
            :
            :
            :
            GAME: glad, oven, #glad.1->GAME->glad, snap
            :
            SHED: #else->SLOW->else, _#glad->GAME->glad, _#iron->DIET->iron, free
            :
            SLOW: else, line, #cute->ODDS->cute, #echo->ODDS->echo, whom
            :
            CORD: #else->SLOW->else, _#bury->LOCK->bury, left
            :
            LOCK: bury
            :
            
            
            :
            PEAK: amid, salt, #glad->GAME->glad, rain
            :
            :
            :
            DIET: iron, cell, #rich->QUIT->rich, clip
            :
            SOUL: #iron->DIET->iron, _#else->SLOW->else, joke
            :
            :
            :
            FUND: #bury->LOCK->bury, #cute->ODDS->cute, #echo->ODDS->echo, dump
            :
            
            
            :
            DENY: #rich->QUIT->rich, _#rich.1->QUIT->rich, hers
            :
            QUIT: rich, milk
            :
            :
            :
            POEM: cute, farm
            :
            :
            :
            ODDS: #cute->POEM->cute, _echo, golf
            :
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_html(self):
        template = json.loads(codecs.open("mocodo/relation_templates/html.json").read())
        expected = u"""
            <html>
            <head>
            <meta charset='utf-8'>
            <style>
              #mld .relation { font-variant: small-caps; font-weight: bold }
              #mld .primary { text-decoration: underline }
              #mld .foreign { font-style: oblique }
              #mld .normal { }
            </style>
            </head>
            <body>
            <div id='mld'>
            <div>
              <span class='relation'>GAME</span> (
                <span class='primary'>glad</span>,
                <span class='normal'>oven</span>,
                <span class='foreign'>glad.1</span>,
                <span class='normal'>snap</span>
              )
            </div>
            <div>
              <span class='relation'>SHED</span> (
                <span class='foreign primary'>else</span>,
                <span class='foreign primary'>glad</span>,
                <span class='foreign primary'>iron</span>,
                <span class='normal'>free</span>
              )
            </div>
            <div>
              <span class='relation'>SLOW</span> (
                <span class='primary'>else</span>,
                <span class='normal'>line</span>,
                <span class='foreign'>cute</span>,
                <span class='foreign'>echo</span>,
                <span class='normal'>whom</span>
              )
            </div>
            <div>
              <span class='relation'>CORD</span> (
                <span class='foreign'>else</span>,
                <span class='foreign primary'>bury</span>,
                <span class='normal'>left</span>
              )
            </div>
            <!--
            <div>
              <span class='relation'>LOCK</span> (
                <span class='primary'>bury</span>
              )
            </div>
            -->
            <div>
              <span class='relation'>PEAK</span> (
                <span class='primary'>amid</span>,
                <span class='normal'>salt</span>,
                <span class='foreign'>glad</span>,
                <span class='normal'>rain</span>
              )
            </div>
            <div>
              <span class='relation'>DIET</span> (
                <span class='primary'>iron</span>,
                <span class='normal'>cell</span>,
                <span class='foreign'>rich</span>,
                <span class='normal'>clip</span>
              )
            </div>
            <div>
              <span class='relation'>SOUL</span> (
                <span class='foreign primary'>iron</span>,
                <span class='foreign primary'>else</span>,
                <span class='normal'>joke</span>
              )
            </div>
            <div>
              <span class='relation'>FUND</span> (
                <span class='foreign primary'>bury</span>,
                <span class='foreign'>cute</span>,
                <span class='foreign'>echo</span>,
                <span class='normal'>dump</span>
              )
            </div>
            <div>
              <span class='relation'>DENY</span> (
                <span class='foreign primary'>rich</span>,
                <span class='foreign primary'>rich.1</span>,
                <span class='normal'>hers</span>
              )
            </div>
            <div>
              <span class='relation'>QUIT</span> (
                <span class='primary'>rich</span>,
                <span class='normal'>milk</span>
              )
            </div>
            <div>
              <span class='relation'>POEM</span> (
                <span class='primary'>cute</span>,
                <span class='normal'>farm</span>
              )
            </div>
            <div>
              <span class='relation'>ODDS</span> (
                <span class='foreign primary'>cute</span>,
                <span class='primary'>echo</span>,
                <span class='normal'>golf</span>
              )
            </div>
            </div>
            </body>
            </html>
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_html_verbose(self):
        template = json.loads(codecs.open("mocodo/relation_templates/html_verbose.json").read())
        expected = u"""
            <html>
            <head>
            <meta charset='utf-8'>
            <style>
              #mld .relation { font-variant: small-caps; font-weight: bold }
              #mld .primary { text-decoration: underline }
              #mld .foreign { font-style: oblique }
              #mld .normal { }
              #mld strong { font-weight: bold }
              #mld i { font-style: italic }
              #mld ul { list-style-type:square; margin: 0 0 1em 2em }
            </style>
            </head>
            <body>
            <div id='mld'>
            <div>
              <span class='relation'>GAME</span> (
                <span class='primary'>glad</span>,
                <span class='normal'>oven</span>,
                <span class='foreign'>glad.1</span>,
                <span class='normal'>snap</span>
              )
              <ul>
                <li>Le champ <i>glad</i> constitue la clef primaire de la table. C'était déjà un identifiant de l'entité <i>GAME</i>.</li>
                <li>Le champ <i>oven</i> était déjà un simple attribut de l'entité <i>GAME</i>.</li>
                <li>Le champ <i>glad.1</i> est une clef étrangère. Il a migré à partir de l'entité <i>GAME</i> par l'association de dépendance fonctionnelle <i>BOOT</i> en perdant son caractère identifiant.</li>
                <li>Le champ <i>snap</i> a migré à partir de l'association de dépendance fonctionnelle <i>BOOT</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>SHED</span> (
                <span class='foreign primary'>else</span>,
                <span class='foreign primary'>glad</span>,
                <span class='foreign primary'>iron</span>,
                <span class='normal'>free</span>
              )
              <ul>
                <li>Le champ <i>else</i> fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité <i>SLOW</i>.</li>
                <li>Le champ <i>glad</i> fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité <i>GAME</i>.</li>
                <li>Le champ <i>iron</i> fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité <i>DIET</i>.</li>
                <li>Le champ <i>free</i> était déjà un simple attribut de l'association <i>SHED</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>SLOW</span> (
                <span class='primary'>else</span>,
                <span class='normal'>line</span>,
                <span class='foreign'>cute</span>,
                <span class='foreign'>echo</span>,
                <span class='normal'>whom</span>
              )
              <ul>
                <li>Le champ <i>else</i> constitue la clef primaire de la table. C'était déjà un identifiant de l'entité <i>SLOW</i>.</li>
                <li>Le champ <i>line</i> était déjà un simple attribut de l'entité <i>SLOW</i>.</li>
                <li>Le champ <i>cute</i> est une clef étrangère. Il a migré à partir de l'entité <i>ODDS</i> par l'association de dépendance fonctionnelle <i>ALLY</i> en perdant son caractère identifiant.</li>
                <li>Le champ <i>echo</i> est une clef étrangère. Il a migré à partir de l'entité <i>ODDS</i> par l'association de dépendance fonctionnelle <i>ALLY</i> en perdant son caractère identifiant.</li>
                <li>Le champ <i>whom</i> a migré à partir de l'association de dépendance fonctionnelle <i>ALLY</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>CORD</span> (
                <span class='foreign'>else</span>,
                <span class='foreign primary'>bury</span>,
                <span class='normal'>left</span>
              )
              <ul>
                <li>Le champ <i>else</i> est une clef étrangère issue de l'entité <i>SLOW</i>. Il devrait normalement migrer à travers l'association <i>CORD</i>, mais celle-ci a été explicitement promue au rang de table.</li>
                <li>Le champ <i>bury</i> constitue la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité <i>LOCK</i>.</li>
                <li>Le champ <i>left</i> était déjà un simple attribut de l'association <i>CORD</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>LOCK</span> (
                <span class='primary'>bury</span>
              )
              <ul>
                <li><strong>Avertissement.</strong> Cette table ne comportant qu'un seul champ, on peut envisager de la supprimer.</li>
                <li>Le champ <i>bury</i> constitue la clef primaire de la table. C'était déjà un identifiant de l'entité <i>LOCK</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>PEAK</span> (
                <span class='primary'>amid</span>,
                <span class='normal'>salt</span>,
                <span class='foreign'>glad</span>,
                <span class='normal'>rain</span>
              )
              <ul>
                <li>Le champ <i>amid</i> constitue la clef primaire de la table. C'était déjà un identifiant de l'entité <i>PEAK</i>.</li>
                <li>Le champ <i>salt</i> était déjà un simple attribut de l'entité <i>PEAK</i>.</li>
                <li>Le champ <i>glad</i> est une clef étrangère. Il a migré à partir de l'entité <i>GAME</i> par l'association de dépendance fonctionnelle <i>PASS</i> en perdant son caractère identifiant.</li>
                <li>Le champ <i>rain</i> a migré à partir de l'association de dépendance fonctionnelle <i>PASS</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>DIET</span> (
                <span class='primary'>iron</span>,
                <span class='normal'>cell</span>,
                <span class='foreign'>rich</span>,
                <span class='normal'>clip</span>
              )
              <ul>
                <li>Le champ <i>iron</i> constitue la clef primaire de la table. C'était déjà un identifiant de l'entité <i>DIET</i>.</li>
                <li>Le champ <i>cell</i> était déjà un simple attribut de l'entité <i>DIET</i>.</li>
                <li>Le champ <i>rich</i> est une clef étrangère. Il a migré à partir de l'entité <i>QUIT</i> par l'association de dépendance fonctionnelle <i>MYTH</i> en perdant son caractère identifiant.</li>
                <li>Le champ <i>clip</i> a migré à partir de l'association de dépendance fonctionnelle <i>MYTH</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>SOUL</span> (
                <span class='foreign primary'>iron</span>,
                <span class='foreign primary'>else</span>,
                <span class='normal'>joke</span>
              )
              <ul>
                <li>Le champ <i>iron</i> fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité <i>DIET</i>.</li>
                <li>Le champ <i>else</i> fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité <i>SLOW</i>.</li>
                <li>Le champ <i>joke</i> était déjà un simple attribut de l'association <i>SOUL</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>FUND</span> (
                <span class='foreign primary'>bury</span>,
                <span class='foreign'>cute</span>,
                <span class='foreign'>echo</span>,
                <span class='normal'>dump</span>
              )
              <ul>
                <li>Le champ <i>bury</i> constitue la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité <i>LOCK</i>.</li>
                <li>Le champ <i>cute</i> est une clef étrangère issue de l'entité <i>ODDS</i>. Il devrait normalement faire partie de l'identifiant de <i>FUND</i>, mais a été rétrogradé explicitement au rang de simple attribut.</li>
                <li>Le champ <i>echo</i> est une clef étrangère issue de l'entité <i>ODDS</i>. Il devrait normalement faire partie de l'identifiant de <i>FUND</i>, mais a été rétrogradé explicitement au rang de simple attribut.</li>
                <li>Le champ <i>dump</i> était déjà un simple attribut de l'association <i>FUND</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>DENY</span> (
                <span class='foreign primary'>rich</span>,
                <span class='foreign primary'>rich.1</span>,
                <span class='normal'>hers</span>
              )
              <ul>
                <li>Les champs <i>rich</i> et <i>rich.1</i> constituent la clef primaire de la table. Ce sont des clefs étrangères qui ont migré directement à partir de l'entité <i>QUIT</i>.</li>
                <li>Le champ <i>hers</i> était déjà un simple attribut de l'association <i>DENY</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>QUIT</span> (
                <span class='primary'>rich</span>,
                <span class='normal'>milk</span>
              )
              <ul>
                <li>Le champ <i>rich</i> constitue la clef primaire de la table. C'était déjà un identifiant de l'entité <i>QUIT</i>.</li>
                <li>Le champ <i>milk</i> était déjà un simple attribut de l'entité <i>QUIT</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>POEM</span> (
                <span class='primary'>cute</span>,
                <span class='normal'>farm</span>
              )
              <ul>
                <li>Le champ <i>cute</i> constitue la clef primaire de la table. C'était déjà un identifiant de l'entité <i>POEM</i>.</li>
                <li>Le champ <i>farm</i> était déjà un simple attribut de l'entité <i>POEM</i>.</li>
              </ul>
            </div>
            
            <div>
              <span class='relation'>ODDS</span> (
                <span class='foreign primary'>cute</span>,
                <span class='primary'>echo</span>,
                <span class='normal'>golf</span>
              )
              <ul>
                <li>Le champ <i>cute</i> fait partie de la clef primaire de la table. Il a migré à partir de l'entité <i>POEM</i> pour renforcer l'identifiant.</li>
                <li>Le champ <i>echo</i> fait partie de la clef primaire de la table. C'était déjà un identifiant de l'entité <i>ODDS</i>.</li>
                <li>Le champ <i>golf</i> a migré à partir de l'association de dépendance fonctionnelle <i>HANG</i>.</li>
              </ul>
            </div>
            
            </div>
            </body>
            </html>
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_latex(self):
        template = json.loads(codecs.open("mocodo/relation_templates/latex.json").read())
        expected = u"""
            % Copy this before \\begin{document}
            
            \\usepackage[normalem]{ulem}
            \\newenvironment{mld}
              {\\par\\begin{minipage}{\\linewidth}\\begin{tabular}{rp{0.7\\linewidth}}}
              {\\end{tabular}\\end{minipage}\\par}
            \\newcommand{\\relat}[1]{\\textsc{#1}}
            \\newcommand{\\attr}[1]{\\emph{#1}}
            \\newcommand{\\prim}[1]{\\uline{#1}}
            \\newcommand{\\foreign}[1]{\\#\\textsl{#1}}
            
            % Copy that after \\begin{document}
            
            \\begin{mld}
              Game & (\\prim{glad}, \\attr{oven}, \\foreign{glad.1}, \\attr{snap})\\\\
              Shed & (\\foreign{\\prim{else}}, \\foreign{\\prim{glad}}, \\foreign{\\prim{iron}}, \\attr{free})\\\\
              Slow & (\\prim{else}, \\attr{line}, \\foreign{cute}, \\foreign{echo}, \\attr{whom})\\\\
              Cord & (\\foreign{else}, \\foreign{\\prim{bury}}, \\attr{left})\\\\
            % Lock & (\\prim{bury})\\\\
              Peak & (\\prim{amid}, \\attr{salt}, \\foreign{glad}, \\attr{rain})\\\\
              Diet & (\\prim{iron}, \\attr{cell}, \\foreign{rich}, \\attr{clip})\\\\
              Soul & (\\foreign{\\prim{iron}}, \\foreign{\\prim{else}}, \\attr{joke})\\\\
              Fund & (\\foreign{\\prim{bury}}, \\foreign{cute}, \\foreign{echo}, \\attr{dump})\\\\
              Deny & (\\foreign{\\prim{rich}}, \\foreign{\\prim{rich.1}}, \\attr{hers})\\\\
              Quit & (\\prim{rich}, \\attr{milk})\\\\
              Poem & (\\prim{cute}, \\attr{farm})\\\\
              Odds & (\\foreign{\\prim{cute}}, \\prim{echo}, \\attr{golf})\\\\
            \\end{mld}
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_markdown(self):
        template = json.loads(codecs.open("mocodo/relation_templates/markdown.json").read())
        expected = u"""
            **GAME** (<ins>glad</ins>, oven, _glad.1_, snap)  
            **SHED** (<ins>_else_</ins>, <ins>_glad_</ins>, <ins>_iron_</ins>, free)  
            **SLOW** (<ins>else</ins>, line, _cute_, _echo_, whom)  
            **CORD** (_else_, <ins>_bury_</ins>, left)  
            <!---
            **LOCK** (<ins>bury</ins>)
            --->  
            **PEAK** (<ins>amid</ins>, salt, _glad_, rain)  
            **DIET** (<ins>iron</ins>, cell, _rich_, clip)  
            **SOUL** (<ins>_iron_</ins>, <ins>_else_</ins>, joke)  
            **FUND** (<ins>_bury_</ins>, _cute_, _echo_, dump)  
            **DENY** (<ins>_rich_</ins>, <ins>_rich.1_</ins>, hers)  
            **QUIT** (<ins>rich</ins>, milk)  
            **POEM** (<ins>cute</ins>, farm)  
            **ODDS** (<ins>_cute_</ins>, <ins>echo</ins>, golf)
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_markdown_verbose(self):
        template = json.loads(codecs.open("mocodo/relation_templates/markdown_verbose.json").read())
        expected = u"""
            **GAME** (<ins>glad</ins>, oven, _glad.1_, snap)  
            - Le champ _glad_ constitue la clef primaire de la table. C'était déjà un identifiant de l'entité _GAME_.  
            - Le champ _oven_ était déjà un simple attribut de l'entité _GAME_.  
            - Le champ _glad.1_ est une clef étrangère. Il a migré à partir de l'entité _GAME_ par l'association de dépendance fonctionnelle _BOOT_ en perdant son caractère identifiant.  
            - Le champ _snap_ a migré à partir de l'association de dépendance fonctionnelle _BOOT_.  
            
            **SHED** (<ins>_else_</ins>, <ins>_glad_</ins>, <ins>_iron_</ins>, free)  
            - Le champ _else_ fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité _SLOW_.  
            - Le champ _glad_ fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité _GAME_.  
            - Le champ _iron_ fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité _DIET_.  
            - Le champ _free_ était déjà un simple attribut de l'association _SHED_.  
            
            **SLOW** (<ins>else</ins>, line, _cute_, _echo_, whom)  
            - Le champ _else_ constitue la clef primaire de la table. C'était déjà un identifiant de l'entité _SLOW_.  
            - Le champ _line_ était déjà un simple attribut de l'entité _SLOW_.  
            - Le champ _cute_ est une clef étrangère. Il a migré à partir de l'entité _ODDS_ par l'association de dépendance fonctionnelle _ALLY_ en perdant son caractère identifiant.  
            - Le champ _echo_ est une clef étrangère. Il a migré à partir de l'entité _ODDS_ par l'association de dépendance fonctionnelle _ALLY_ en perdant son caractère identifiant.  
            - Le champ _whom_ a migré à partir de l'association de dépendance fonctionnelle _ALLY_.  
            
            **CORD** (_else_, <ins>_bury_</ins>, left)  
            - Le champ _else_ est une clef étrangère issue de l'entité _SLOW_. Il devrait normalement migrer à travers l'association _CORD_, mais celle-ci a été explicitement promue au rang de table.  
            - Le champ _bury_ constitue la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité _LOCK_.  
            - Le champ _left_ était déjà un simple attribut de l'association _CORD_.  
            
            **LOCK** (<ins>bury</ins>)  
            - **Avertissement.** Cette table ne comportant qu'un seul champ, on peut envisager de la supprimer.
            - Le champ _bury_ constitue la clef primaire de la table. C'était déjà un identifiant de l'entité _LOCK_.  
            
            **PEAK** (<ins>amid</ins>, salt, _glad_, rain)  
            - Le champ _amid_ constitue la clef primaire de la table. C'était déjà un identifiant de l'entité _PEAK_.  
            - Le champ _salt_ était déjà un simple attribut de l'entité _PEAK_.  
            - Le champ _glad_ est une clef étrangère. Il a migré à partir de l'entité _GAME_ par l'association de dépendance fonctionnelle _PASS_ en perdant son caractère identifiant.  
            - Le champ _rain_ a migré à partir de l'association de dépendance fonctionnelle _PASS_.  
            
            **DIET** (<ins>iron</ins>, cell, _rich_, clip)  
            - Le champ _iron_ constitue la clef primaire de la table. C'était déjà un identifiant de l'entité _DIET_.  
            - Le champ _cell_ était déjà un simple attribut de l'entité _DIET_.  
            - Le champ _rich_ est une clef étrangère. Il a migré à partir de l'entité _QUIT_ par l'association de dépendance fonctionnelle _MYTH_ en perdant son caractère identifiant.  
            - Le champ _clip_ a migré à partir de l'association de dépendance fonctionnelle _MYTH_.  
            
            **SOUL** (<ins>_iron_</ins>, <ins>_else_</ins>, joke)  
            - Le champ _iron_ fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité _DIET_.  
            - Le champ _else_ fait partie de la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité _SLOW_.  
            - Le champ _joke_ était déjà un simple attribut de l'association _SOUL_.  
            
            **FUND** (<ins>_bury_</ins>, _cute_, _echo_, dump)  
            - Le champ _bury_ constitue la clef primaire de la table. C'est une clef étrangère qui a migré directement à partir de l'entité _LOCK_.  
            - Le champ _cute_ est une clef étrangère issue de l'entité _ODDS_. Il devrait normalement faire partie de l'identifiant de _FUND_, mais a été rétrogradé explicitement au rang de simple attribut.  
            - Le champ _echo_ est une clef étrangère issue de l'entité _ODDS_. Il devrait normalement faire partie de l'identifiant de _FUND_, mais a été rétrogradé explicitement au rang de simple attribut.  
            - Le champ _dump_ était déjà un simple attribut de l'association _FUND_.  
            
            **DENY** (<ins>_rich_</ins>, <ins>_rich.1_</ins>, hers)  
            - Les champs _rich_ et _rich.1_ constituent la clef primaire de la table. Ce sont des clefs étrangères qui ont migré directement à partir de l'entité _QUIT_.  
            - Le champ _hers_ était déjà un simple attribut de l'association _DENY_.  
            
            **QUIT** (<ins>rich</ins>, milk)  
            - Le champ _rich_ constitue la clef primaire de la table. C'était déjà un identifiant de l'entité _QUIT_.  
            - Le champ _milk_ était déjà un simple attribut de l'entité _QUIT_.  
            
            **POEM** (<ins>cute</ins>, farm)  
            - Le champ _cute_ constitue la clef primaire de la table. C'était déjà un identifiant de l'entité _POEM_.  
            - Le champ _farm_ était déjà un simple attribut de l'entité _POEM_.  
            
            **ODDS** (<ins>_cute_</ins>, <ins>echo</ins>, golf)  
            - Le champ _cute_ fait partie de la clef primaire de la table. Il a migré à partir de l'entité _POEM_ pour renforcer l'identifiant.  
            - Le champ _echo_ fait partie de la clef primaire de la table. C'était déjà un identifiant de l'entité _ODDS_.  
            - Le champ _golf_ a migré à partir de l'association de dépendance fonctionnelle _HANG_.
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_mysql(self):
        template = json.loads(codecs.open("mocodo/relation_templates/mysql.json").read())
        expected = u"""
            CREATE DATABASE IF NOT EXISTS `UNTITLED` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
            USE `UNTITLED`;
            
            CREATE TABLE `GAME` (
              `glad` None,
              `oven` None,
              `glad_1` None,
              `snap` None,
              PRIMARY KEY(`glad`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `SHED` (
              `else` None,
              `glad` None,
              `iron` None,
              `free` None,
              PRIMARY KEY(`else`, `glad`, `iron`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `SLOW` (
              `else` None,
              `line` None,
              `cute` None,
              `echo` None,
              `whom` None,
              PRIMARY KEY(`else`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `CORD` (
              `else` None,
              `bury` None,
              `left` None,
              PRIMARY KEY(`bury`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            /*
            CREATE TABLE `LOCK` (
              `bury` None,
              PRIMARY KEY(`bury`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            */
            
            CREATE TABLE `PEAK` (
              `amid` None,
              `salt` None,
              `glad` None,
              `rain` None,
              PRIMARY KEY(`amid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `DIET` (
              `iron` None,
              `cell` None,
              `rich` None,
              `clip` None,
              PRIMARY KEY(`iron`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `SOUL` (
              `iron` None,
              `else` None,
              `joke` None,
              PRIMARY KEY(`iron`, `else`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `FUND` (
              `bury` None,
              `cute` None,
              `echo` None,
              `dump` None,
              PRIMARY KEY(`bury`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `DENY` (
              `rich` None,
              `rich_1` None,
              `hers` None,
              PRIMARY KEY(`rich`, `rich_1`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `QUIT` (
              `rich` None,
              `milk` None,
              PRIMARY KEY(`rich`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `POEM` (
              `cute` None,
              `farm` None,
              PRIMARY KEY(`cute`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            CREATE TABLE `ODDS` (
              `cute` None,
              `echo` None,
              `golf` None,
              PRIMARY KEY(`cute`, `echo`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
            ALTER TABLE `GAME` ADD FOREIGN KEY (`glad_1`) REFERENCES `GAME` (`glad_1`);
            ALTER TABLE `SHED` ADD FOREIGN KEY (`else`) REFERENCES `SLOW` (`else`);
            ALTER TABLE `SHED` ADD FOREIGN KEY (`glad`) REFERENCES `GAME` (`glad`);
            ALTER TABLE `SHED` ADD FOREIGN KEY (`iron`) REFERENCES `DIET` (`iron`);
            ALTER TABLE `SLOW` ADD FOREIGN KEY (`cute`) REFERENCES `ODDS` (`cute`);
            ALTER TABLE `SLOW` ADD FOREIGN KEY (`echo`) REFERENCES `ODDS` (`echo`);
            ALTER TABLE `CORD` ADD FOREIGN KEY (`else`) REFERENCES `SLOW` (`else`);
            ALTER TABLE `CORD` ADD FOREIGN KEY (`bury`) REFERENCES `LOCK` (`bury`);
            ALTER TABLE `PEAK` ADD FOREIGN KEY (`glad`) REFERENCES `GAME` (`glad`);
            ALTER TABLE `DIET` ADD FOREIGN KEY (`rich`) REFERENCES `QUIT` (`rich`);
            ALTER TABLE `SOUL` ADD FOREIGN KEY (`iron`) REFERENCES `DIET` (`iron`);
            ALTER TABLE `SOUL` ADD FOREIGN KEY (`else`) REFERENCES `SLOW` (`else`);
            ALTER TABLE `FUND` ADD FOREIGN KEY (`bury`) REFERENCES `LOCK` (`bury`);
            ALTER TABLE `FUND` ADD FOREIGN KEY (`cute`) REFERENCES `ODDS` (`cute`);
            ALTER TABLE `FUND` ADD FOREIGN KEY (`echo`) REFERENCES `ODDS` (`echo`);
            ALTER TABLE `DENY` ADD FOREIGN KEY (`rich`) REFERENCES `QUIT` (`rich`);
            ALTER TABLE `DENY` ADD FOREIGN KEY (`rich_1`) REFERENCES `QUIT` (`rich_1`);
            ALTER TABLE `ODDS` ADD FOREIGN KEY (`cute`) REFERENCES `POEM` (`cute`);
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_oracle(self):
        template = json.loads(codecs.open("mocodo/relation_templates/oracle.json").read())
        expected = u"""
            CREATE TABLE "GAME" (
              "glad" None,
              "oven" None,
              "glad_1" None,
              "snap" None,
              PRIMARY KEY("glad")
            );
            
            CREATE TABLE "SHED" (
              "else" None,
              "glad" None,
              "iron" None,
              "free" None,
              PRIMARY KEY("else", "glad", "iron")
            );
            
            CREATE TABLE "SLOW" (
              "else" None,
              "line" None,
              "cute" None,
              "echo" None,
              "whom" None,
              PRIMARY KEY("else")
            );
            
            CREATE TABLE "CORD" (
              "else" None,
              "bury" None,
              "left" None,
              PRIMARY KEY("bury")
            );
            
            /*
            CREATE TABLE "LOCK" (
              "bury" None,
              PRIMARY KEY("bury")
            );
            */
            
            CREATE TABLE "PEAK" (
              "amid" None,
              "salt" None,
              "glad" None,
              "rain" None,
              PRIMARY KEY("amid")
            );
            
            CREATE TABLE "DIET" (
              "iron" None,
              "cell" None,
              "rich" None,
              "clip" None,
              PRIMARY KEY("iron")
            );
            
            CREATE TABLE "SOUL" (
              "iron" None,
              "else" None,
              "joke" None,
              PRIMARY KEY("iron", "else")
            );
            
            CREATE TABLE "FUND" (
              "bury" None,
              "cute" None,
              "echo" None,
              "dump" None,
              PRIMARY KEY("bury")
            );
            
            CREATE TABLE "DENY" (
              "rich" None,
              "rich_1" None,
              "hers" None,
              PRIMARY KEY("rich", "rich_1")
            );
            
            CREATE TABLE "QUIT" (
              "rich" None,
              "milk" None,
              PRIMARY KEY("rich")
            );
            
            CREATE TABLE "POEM" (
              "cute" None,
              "farm" None,
              PRIMARY KEY("cute")
            );
            
            CREATE TABLE "ODDS" (
              "cute" None,
              "echo" None,
              "golf" None,
              PRIMARY KEY("cute", "echo")
            );
            
            ALTER TABLE "GAME" ADD FOREIGN KEY ("glad_1") REFERENCES "GAME" ("glad_1");
            ALTER TABLE "SHED" ADD FOREIGN KEY ("else") REFERENCES "SLOW" ("else");
            ALTER TABLE "SHED" ADD FOREIGN KEY ("glad") REFERENCES "GAME" ("glad");
            ALTER TABLE "SHED" ADD FOREIGN KEY ("iron") REFERENCES "DIET" ("iron");
            ALTER TABLE "SLOW" ADD FOREIGN KEY ("cute") REFERENCES "ODDS" ("cute");
            ALTER TABLE "SLOW" ADD FOREIGN KEY ("echo") REFERENCES "ODDS" ("echo");
            ALTER TABLE "CORD" ADD FOREIGN KEY ("else") REFERENCES "SLOW" ("else");
            ALTER TABLE "CORD" ADD FOREIGN KEY ("bury") REFERENCES "LOCK" ("bury");
            ALTER TABLE "PEAK" ADD FOREIGN KEY ("glad") REFERENCES "GAME" ("glad");
            ALTER TABLE "DIET" ADD FOREIGN KEY ("rich") REFERENCES "QUIT" ("rich");
            ALTER TABLE "SOUL" ADD FOREIGN KEY ("iron") REFERENCES "DIET" ("iron");
            ALTER TABLE "SOUL" ADD FOREIGN KEY ("else") REFERENCES "SLOW" ("else");
            ALTER TABLE "FUND" ADD FOREIGN KEY ("bury") REFERENCES "LOCK" ("bury");
            ALTER TABLE "FUND" ADD FOREIGN KEY ("cute") REFERENCES "ODDS" ("cute");
            ALTER TABLE "FUND" ADD FOREIGN KEY ("echo") REFERENCES "ODDS" ("echo");
            ALTER TABLE "DENY" ADD FOREIGN KEY ("rich") REFERENCES "QUIT" ("rich");
            ALTER TABLE "DENY" ADD FOREIGN KEY ("rich_1") REFERENCES "QUIT" ("rich_1");
            ALTER TABLE "ODDS" ADD FOREIGN KEY ("cute") REFERENCES "POEM" ("cute");
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_postgresql(self):
        template = json.loads(codecs.open("mocodo/relation_templates/postgresql.json").read())
        expected = u"""
            CREATE DATABASE "UNTITLED";
            \\c "UNTITLED;
            
            CREATE TABLE "GAME" (
              "glad" None,
              "oven" None,
              "glad_1" None,
              "snap" None,
              PRIMARY KEY("glad")
            );
            
            CREATE TABLE "SHED" (
              "else" None,
              "glad" None,
              "iron" None,
              "free" None,
              PRIMARY KEY("else", "glad", "iron")
            );
            
            CREATE TABLE "SLOW" (
              "else" None,
              "line" None,
              "cute" None,
              "echo" None,
              "whom" None,
              PRIMARY KEY("else")
            );
            
            CREATE TABLE "CORD" (
              "else" None,
              "bury" None,
              "left" None,
              PRIMARY KEY("bury")
            );
            
            /*
            CREATE TABLE "LOCK" (
              "bury" None,
              PRIMARY KEY("bury")
            );
            */
            
            CREATE TABLE "PEAK" (
              "amid" None,
              "salt" None,
              "glad" None,
              "rain" None,
              PRIMARY KEY("amid")
            );
            
            CREATE TABLE "DIET" (
              "iron" None,
              "cell" None,
              "rich" None,
              "clip" None,
              PRIMARY KEY("iron")
            );
            
            CREATE TABLE "SOUL" (
              "iron" None,
              "else" None,
              "joke" None,
              PRIMARY KEY("iron", "else")
            );
            
            CREATE TABLE "FUND" (
              "bury" None,
              "cute" None,
              "echo" None,
              "dump" None,
              PRIMARY KEY("bury")
            );
            
            CREATE TABLE "DENY" (
              "rich" None,
              "rich_1" None,
              "hers" None,
              PRIMARY KEY("rich", "rich_1")
            );
            
            CREATE TABLE "QUIT" (
              "rich" None,
              "milk" None,
              PRIMARY KEY("rich")
            );
            
            CREATE TABLE "POEM" (
              "cute" None,
              "farm" None,
              PRIMARY KEY("cute")
            );
            
            CREATE TABLE "ODDS" (
              "cute" None,
              "echo" None,
              "golf" None,
              PRIMARY KEY("cute", "echo")
            );
            
            ALTER TABLE "GAME" ADD FOREIGN KEY ("glad_1") REFERENCES "GAME" ("glad_1");
            ALTER TABLE "SHED" ADD FOREIGN KEY ("else") REFERENCES "SLOW" ("else");
            ALTER TABLE "SHED" ADD FOREIGN KEY ("glad") REFERENCES "GAME" ("glad");
            ALTER TABLE "SHED" ADD FOREIGN KEY ("iron") REFERENCES "DIET" ("iron");
            ALTER TABLE "SLOW" ADD FOREIGN KEY ("cute") REFERENCES "ODDS" ("cute");
            ALTER TABLE "SLOW" ADD FOREIGN KEY ("echo") REFERENCES "ODDS" ("echo");
            ALTER TABLE "CORD" ADD FOREIGN KEY ("else") REFERENCES "SLOW" ("else");
            ALTER TABLE "CORD" ADD FOREIGN KEY ("bury") REFERENCES "LOCK" ("bury");
            ALTER TABLE "PEAK" ADD FOREIGN KEY ("glad") REFERENCES "GAME" ("glad");
            ALTER TABLE "DIET" ADD FOREIGN KEY ("rich") REFERENCES "QUIT" ("rich");
            ALTER TABLE "SOUL" ADD FOREIGN KEY ("iron") REFERENCES "DIET" ("iron");
            ALTER TABLE "SOUL" ADD FOREIGN KEY ("else") REFERENCES "SLOW" ("else");
            ALTER TABLE "FUND" ADD FOREIGN KEY ("bury") REFERENCES "LOCK" ("bury");
            ALTER TABLE "FUND" ADD FOREIGN KEY ("cute") REFERENCES "ODDS" ("cute");
            ALTER TABLE "FUND" ADD FOREIGN KEY ("echo") REFERENCES "ODDS" ("echo");
            ALTER TABLE "DENY" ADD FOREIGN KEY ("rich") REFERENCES "QUIT" ("rich");
            ALTER TABLE "DENY" ADD FOREIGN KEY ("rich_1") REFERENCES "QUIT" ("rich_1");
            ALTER TABLE "ODDS" ADD FOREIGN KEY ("cute") REFERENCES "POEM" ("cute");
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_sqlite(self):
        template = json.loads(codecs.open("mocodo/relation_templates/sqlite.json").read())
        expected = u"""
            .open "UNTITLED";
            
            CREATE TABLE "GAME" (
              "glad" None PRIMARY KEY,
              "oven" None,
              "glad_1" None,
              "snap" None,
              FOREIGN KEY ("glad_1") REFERENCES "GAME" ("glad_1")
            );
            
            CREATE TABLE "SHED" (
              "else" None,
              "glad" None,
              "iron" None,
              "free" None,
              FOREIGN KEY ("else") REFERENCES "SLOW" ("else"),
              FOREIGN KEY ("glad") REFERENCES "GAME" ("glad"),
              FOREIGN KEY ("iron") REFERENCES "DIET" ("iron")
            );
            
            CREATE TABLE "SLOW" (
              "else" None PRIMARY KEY,
              "line" None,
              "cute" None,
              "echo" None,
              "whom" None,
              FOREIGN KEY ("cute") REFERENCES "ODDS" ("cute"),
              FOREIGN KEY ("echo") REFERENCES "ODDS" ("echo")
            );
            
            CREATE TABLE "CORD" (
              "else" None,
              "bury" None,
              "left" None,
              FOREIGN KEY ("else") REFERENCES "SLOW" ("else"),
              FOREIGN KEY ("bury") REFERENCES "LOCK" ("bury")
            );
            
            /*
            CREATE TABLE "LOCK" (
              "bury" None PRIMARY KEY
            );
            */
            
            CREATE TABLE "PEAK" (
              "amid" None PRIMARY KEY,
              "salt" None,
              "glad" None,
              "rain" None,
              FOREIGN KEY ("glad") REFERENCES "GAME" ("glad")
            );
            
            CREATE TABLE "DIET" (
              "iron" None PRIMARY KEY,
              "cell" None,
              "rich" None,
              "clip" None,
              FOREIGN KEY ("rich") REFERENCES "QUIT" ("rich")
            );
            
            CREATE TABLE "SOUL" (
              "iron" None,
              "else" None,
              "joke" None,
              FOREIGN KEY ("iron") REFERENCES "DIET" ("iron"),
              FOREIGN KEY ("else") REFERENCES "SLOW" ("else")
            );
            
            CREATE TABLE "FUND" (
              "bury" None,
              "cute" None,
              "echo" None,
              "dump" None,
              FOREIGN KEY ("bury") REFERENCES "LOCK" ("bury"),
              FOREIGN KEY ("cute") REFERENCES "ODDS" ("cute"),
              FOREIGN KEY ("echo") REFERENCES "ODDS" ("echo")
            );
            
            CREATE TABLE "DENY" (
              "rich" None,
              "rich_1" None,
              "hers" None,
              FOREIGN KEY ("rich") REFERENCES "QUIT" ("rich"),
              FOREIGN KEY ("rich_1") REFERENCES "QUIT" ("rich_1")
            );
            
            CREATE TABLE "QUIT" (
              "rich" None PRIMARY KEY,
              "milk" None
            );
            
            CREATE TABLE "POEM" (
              "cute" None PRIMARY KEY,
              "farm" None
            );
            
            CREATE TABLE "ODDS" (
              "cute" None,
              "echo" None PRIMARY KEY,
              "golf" None,
              FOREIGN KEY ("cute") REFERENCES "POEM" ("cute")
            );
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_text(self):
        template = json.loads(codecs.open("mocodo/relation_templates/text.json").read())
        expected = u"""
            GAME (_glad_, oven, #glad.1, snap)
            SHED (_#else_, _#glad_, _#iron_, free)
            SLOW (_else_, line, #cute, #echo, whom)
            CORD (#else, _#bury_, left)
            LOCK (_bury_)
            PEAK (_amid_, salt, #glad, rain)
            DIET (_iron_, cell, #rich, clip)
            SOUL (_#iron_, _#else_, joke)
            FUND (_#bury_, #cute, #echo, dump)
            DENY (_#rich_, _#rich.1_, hers)
            QUIT (_rich_, milk)
            POEM (_cute_, farm)
            ODDS (_#cute_, _echo_, golf)
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

    def test_txt2tags(self):
        template = json.loads(codecs.open("mocodo/relation_templates/txt2tags.json").read())
        expected = u"""
            Untitled
            Généré par Mocodo
            %%mtime(%c)
            %!encoding: utf8
            - **GAME** (__glad__, oven, #glad.1, snap)
            - **SHED** (__#else__, __#glad__, __#iron__, free)
            - **SLOW** (__else__, line, #cute, #echo, whom)
            - **CORD** (#else, __#bury__, left)
            %% - **LOCK** (__bury__)
            - **PEAK** (__amid__, salt, #glad, rain)
            - **DIET** (__iron__, cell, #rich, clip)
            - **SOUL** (__#iron__, __#else__, joke)
            - **FUND** (__#bury__, #cute, #echo, dump)
            - **DENY** (__#rich__, __#rich.1__, hers)
            - **QUIT** (__rich__, milk)
            - **POEM** (__cute__, farm)
            - **ODDS** (__#cute__, __echo__, golf)
        """.strip().replace("    ", "").split()
        result = t.get_text(template).split()
        for (result_line, expected_line) in zip(result, expected):
            self.assertEquals(result_line, expected_line)

if __name__ == '__main__':
    unittest.main()
