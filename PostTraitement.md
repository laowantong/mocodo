# Post-traitement de la sortie graphique #

Le plongement automatique réalisé par Mocodo pour des MCD de plusieurs lignes peut généralement être amélioré.

#### Fichier d'entrée ####

```
Lacus, 01 Blandit, 1N Elit
Elit: ligula, tellus
Metus, 1N Elit, 0N Congue: nibh

Bibendum, 01 Blandit, 0N Blandit
Blandit: consequat, ligula, nibh, consequat
Ipsum, 1N Blandit, 0N Congue
Congue: ligula, tellus
Augue, 0N Congue, 0N Congue

Velit, 0N Blandit, 0N Nonummy: sollicitudin
DF, 11 Nonummy, 0N Congue

Posuere: pede
Vivamus, 0N Posuere, 0N Nonummy, 0N Blandit: eleifend, iaculis
Nonummy: consequat, ligula
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/visual0.png](http://dl.dropbox.com/u/3108405/mocodo-data/visual0.png)

Depuis la version 1.3, Mocodo est à parité sur toutes les plateformes. Cela signifie qu'au lieu de générer un dessin statique, il génère systématiquement un script, qui lui-même générera le dessin. Quel est l'avantage de cette couche supplémentaire? Eh bien, le script intermédiaire exprime la plupart des positions non en absolu, mais en relation à d'autres positions, peu nombreuses et qui constituent de fait les véritables paramètres. Sa capacité à évaluer des formules le rend beaucoup plus souple et plus puissant que si les valeurs résultantes étaient stockées en dur.

## Retouches manuelles du script intermédiaire ##

Par défaut, Mocodo génère un fichier appelé `sandbox-nodebox.py` (sur Mac OS X avec NodeBox installé) ou `sandbox-svg.py` (dans tous les autres cas). Ce fichier est un script qui devra être exécuté respectivement dans l'environnement NodeBox, ou en tapant:

```
python sandbox-svg.py
```

pour générer effectivement le dessin. Le début de ce script intermédiaire ressemble à ceci:

```
cx = {
  u"Lacus": 182,
  u"Elit": 299,
  u"Metus": 421,
  u"Bibendum": 60,
  u"Blandit": 182,
  u"Ipsum": 299,
  u"Congue": 421,
  u"Augue": 527,
  u"Velit": 299,
  u"DF": 421,
  u"Posuere": 182,
  u"Vivamus": 299,
  u"Nonummy": 421,
}
cy = {
  u"Lacus": 47,
  u"Elit": 47,
  u"Metus": 47,
  u"Bibendum": 162,
  u"Blandit": 162,
  u"Ipsum": 162,
  u"Congue": 162,
  u"Augue": 162,
  u"Velit": 268,
  u"DF": 268,
  u"Posuere": 357,
  u"Vivamus": 357,
  u"Nonummy": 357,
}
```

Ces lignes exposent les principaux paramètres de position:  le dictionnaire `cx` (resp. `cy`) correspond aux abscisses (resp. ordonnées) des centres des entités et associations. Supposons que l'on souhaite aligner verticalement les centres de POSUERE et VIVAMUS avec ceux, respectivement, de BIBENDUM et BLANDIT. Dans `cx`, il suffit de copier la valeur de celles-ci dans celles-là:

```
cx = {
  ...
  u"Bibendum": 60,       # abscisse de référence
  u"Blandit": 182,       # abscisse de référence
  ...
  u"Posuere": 60,        # abscisse modifiée
  u"Vivamus": 182,       # abscisse modifiée
  ...
}
```

#### Sortie après retouche ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/visual1.png](http://dl.dropbox.com/u/3108405/mocodo-data/visual1.png)

Si l'on juge que la partie inférieure de la figure occupe trop de place, on remontera les boîtes concernées en intervenant sur les ordonnées.

```
cy = {
  ...
  u"Velit": 248,         # ordonnée diminuée de 20 pixels
  u"DF": 248,            # ordonnée diminuée de 20 pixels
  u"Posuere": 327,       # ordonnée diminuée de 30 pixels
  u"Vivamus": 327,       # ordonnée diminuée de 30 pixels
  u"Nonummy": 327,       # ordonnée diminuée de 30 pixels
  ...
}
```

Les dimensions calculées à l'origine pour l'image ne tiennent compte ni des cardinalités, ni bien sûr des retouches ultérieures. Il peut donc arriver que son cadre soit trop petit ou trop grand pour le MCD. C'est le cas maintenant. Il faut ajuster sa taille, qui se trouve au tout début du fichier:

```
(width,height) = (572,374)            # ordonnée diminuée de 30 pixels
```

#### Sortie après retouche ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/visual2.png](http://dl.dropbox.com/u/3108405/mocodo-data/visual2.png)

On souhaite maintenant corriger la position de certaines cardinalités.
Ces positions se trouvent dans le dictionnaire `k`:

```
k = {
  u"Lacus,Blandit": 1,
  u"Lacus,Elit": 1,
  u"Metus,Elit": 1,
  u"Metus,Congue": 1,
  u"Bibendum,Blandit,-1.0": -4.0,
  u"Bibendum,Blandit,1.0": 4.0,
  u"Ipsum,Blandit": 1,
  u"Ipsum,Congue": 1,
  u"Augue,Congue,-1.0": -4.0,
  u"Augue,Congue,1.0": 4.0,
  u"Velit,Blandit": 1,
  u"Velit,Nonummy": 1,
  u"DF,Nonummy": 1,
  u"DF,Congue": 1,
  u"Vivamus,Posuere": 1,
  u"Vivamus,Nonummy": 1,
  u"Vivamus,Blandit": 1,
}
```

La valeur `1` est un facteur multiplicatif qui signifie: placer la cardinalité au-dessous de la patte et aussi haut que possible pour laisser une marge suffisante entre les deux. Le facteur `-1` signifierait la même chose, en inversant le haut et le bas.
Logiquement, un facteur de `0` placerait la cardinalité sur la patte elle-même. Toutes les valeurs sont possibles, mais en pratique, quelques changements de signe sont en général suffisants pour éviter les collisions.
Ici, aucune collision ne se produit, mais on peut souhaiter détacher légèrement les cardinalités de l'association réflexive BLANDIT:

```
k = {
  ...
  u"Bibendum,Blandit,-1.0": -4.5,
  u"Bibendum,Blandit,1.0": 4.5,
  ...
}
```

#### Sortie après retouche ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/visual3.png](http://dl.dropbox.com/u/3108405/mocodo-data/visual3.png)

La même technique s'applique pour faire glisser les flèches le long des arcs: le dictionnaire à modifier s'appelle `t`.

Un plus ou moins grand nombre de retouches peuvent être nécessaires, mais vous avez l'idée.
D'aucuns y verront peut-être une dangereuse confusion entre données, programme et résultats; d'autres, une application naturelle du dynamisme des langages du même nom; au total, chacun décidera s'il est plus efficace et plus précis en faisant glisser des objets dans son cliquodrome favori, ou en ajustant des valeurs numériques.

### Astuce ###

Si vous voulez tester différentes palettes de couleurs, tout en conservant les retouches effectuées, copiez les lignes correspondantes, lancez Mocodo avec une nouvelle palette, puis recollez les lignes au même endroit.

## Retouches manuelles d'une sortie au format SVG ##

Un fichier en SVG peut être visualisé dans tout navigateur respectueux des standards du web: Firefox, Chrome, Safari, Opera, [Internet Explorer 9 ou 10](http://blogs.msdn.com/ie/archive/2010/01/05/microsoft-joins-w3c-svg-working-group.aspx), etc.

Pour aller au-delà de la simple visualisation, il faudra faire appel à un logiciel de dessin vectoriel dédié, comme [Inkscape](http://www.inkscape.org/?lang=fr) (libre) ou Illustrator, Freehand, CorelDRAW®, etc.
Les éléments du fichier SVG produit pourront alors être repositionnés à la souris. Certains sont associés, pour permettre leur déplacement en bloc. Dans la version actuelle, les liens ne suivent pas ces déplacements, ce qui oblige à des manipulations supplémentaires. De façon générale, les retouches courantes sont plus faciles à réaliser dans le script intermédiaire généré par Mocodo.

## Exportation ##

L'exportation est déléguée à votre éditeur SVG ou à Nodebox. Le format PDF assure la meilleure qualité, aussi bien pour la visualisation sur écran, que pour la projection ou l'impression. Si vous devez absolument utiliser un format bitmap, préférez PNG ou GIF.