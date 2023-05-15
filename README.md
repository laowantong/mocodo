**15 mai 2023.** Mocodo 3.2.0 prend en charge la [visualisation des contraintes sur associations](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Visualisation-des-contraintes-sur-associations).

**11 mai 2023.** Ajout d'un tutoriel / galerie d'exemples dans la [version en ligne](https://www.mocodo.net) de Mocodo 3.1.2.

**24 décembre 2022.** Mocodo 3.1.1 corrige la [gestion des collisions des SVG interactifs](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Éviter-qu'une-interaction-sur-un-SVG-ne-s'applique-à-un-autre).

**14 décembre 2022.** Mocodo 3.1 améliore le passage au relationnel : prise en charge de [gabarits personnels dérivés des gabarits existants](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Dérivation-de-gabarits), traitement des [tables indépendantes réduites à leur clé primaire](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Suppression-des-tables-indépendantes-réduites-à-leur-clé-primaire), génération d'un [graphe des dépendances](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Graphe-des-dépendances) pour le tri topologique des tables, [etc](https://github.com/laowantong/mocodo/releases/tag/3.1.0).

**11 septembre 2022.** Mocodo 3.0 introduit l'[héritage](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Héritage-(ou-spécialisation)), l'[agrégation](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Agrégation-(ou-pseudo-entité)), les [calques](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Héritage-(ou-spécialisation)), les [sorties PDF et PNG](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Héritage-(ou-spécialisation)), [etc](https://github.com/laowantong/mocodo/releases/tag/3.0).

------

Documentation [au format HTML](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html) ou sous forme de [notebook](doc/fr_refman.ipynb) Jupyter.

----

![](https://cdn.rawgit.com/laowantong/mocodo/master/logos/banner.svg)

Mocodo est un logiciel d'aide à l'enseignement et à la conception des [bases de données relationnelles](https://fr.wikipedia.org/wiki/Base_de_données_relationnelle).

- En entrée, il prend une description textuelle des entités et associations du modèle conceptuel de données ([MCD](https://fr.wikipedia.org/wiki/Modèle_entité-association)).
- En sortie, il produit son diagramme entité-association en [SVG](https://fr.wikipedia.org/wiki/Scalable_Vector_Graphics) et son schéma relationnel ([MLD](
https://fr.wikipedia.org/wiki/Merise_%28informatique%29#MLD_:_mod.C3.A8le_logique_des_donn.C3.A9es)) en [SQL](https://fr.wikipedia.org/wiki/Structured_Query_Language), [LaTeX](https://fr.wikipedia.org/wiki/LaTeX), [Markdown](https://fr.wikipedia.org/wiki/Markdown), etc.

Ci-dessous, un exemple d'utilisation sous [Jupyter Notebook](https://jupyter.org). L'appel du programme est en première ligne, sur un texte d'entrée donné lignes suivantes. Le cas est adapté de l'article fondateur de Peter Chen, [_The entity-relationship model—toward a unified view of data_](https://doi.org/10.1145/320434.320440) (ACM Trans. Database Syst. 1, 1, March 1976, pp. 9–36), avec en bonus une association de type hiérarchique et une contrainte d'inclusion.

```
%%mocodo --mld --colors brewer+1 --shapes copperplate --relations diagram markdown_data_dict

Ayant-droit: nom ayant-droit, lien
Diriger, 0N Employé, 01 Projet
Requérir, 1N Projet, 0N Pièce: qté requise
Pièce: réf. pièce, libellé pièce
Composer, 0N [composée] Pièce, 0N [composante] Pièce: quantité

DF1, _11 Ayant-droit, 0N Employé
Employé: matricule, nom employé
Projet: num. projet, nom projet
Fournir, 1N Projet, 1N Pièce, 1N Société: qté fournie

Département: num. département, nom département
Employer, 11 Employé, 1N Département
Travailler, 0N Employé, 1N Projet
Société: num. société, raison sociale
Contrôler, 0N< [filiale] Société, 01 [mère] Société

(I) --Fournir, ->Requérir, ..Pièce, Projet
```

En sortie, le MCD (diagramme conceptuel) et le MLD (schéma relationnel) correspondants:

![](https://cdn.rawgit.com/laowantong/mocodo/master/doc/readme_1.png)

**Ayant-droit** (<ins>_#matricule_</ins>, <ins>nom ayant-droit</ins>, lien)<br>
**Composer** (<ins>_#réf. pièce composée_</ins>, <ins>_#réf. pièce composante_</ins>, quantité)<br>
**Département** (<ins>num. département</ins>, nom département)<br>
**Employé** (<ins>matricule</ins>, nom employé, _#num. département_)<br>
**Fournir** (<ins>_#num. projet_</ins>, <ins>_#réf. pièce_</ins>, <ins>_#num. société_</ins>, qté fournie)<br>
**Pièce** (<ins>réf. pièce</ins>, libellé pièce)<br>
**Projet** (<ins>num. projet</ins>, nom projet, _#matricule_)<br>
**Requérir** (<ins>_#num. projet_</ins>, <ins>_#réf. pièce_</ins>, qté requise)<br>
**Société** (<ins>num. société</ins>, raison sociale, _#num. société mère_)<br>
**Travailler** (<ins>_#matricule_</ins>, <ins>_#num. projet_</ins>)

L'appel précédent a également créé un fichier `mocodo_notebook/sandbox_data_dict.md` contenant le dictionnaire des données :

- nom ayant-droit
- lien
- quantité
- num. département
- nom département
- matricule
- nom employé
- qté fournie
- réf. pièce
- libellé pièce
- num. projet
- nom projet
- qté requise
- num. société
- raison sociale

Ainsi que le diagramme relationnel, qui peut être visualisé par un nouvel appel:

```
%mocodo --input mocodo_notebook/sandbox.mld --colors brewer+1
```

![](https://cdn.rawgit.com/laowantong/mocodo/master/doc/readme_2.png)

La devise de Mocodo, « nickel, ni souris », en résume les principaux points forts:

- description textuelle des données. L'utilisateur n'a pas à renseigner, placer et déplacer des éléments comme avec une lessive ordinaire. Il ne fournit rien de plus que les informations définissant son MCD. L'outil s'occupe tout seul du plongement ;
- propreté du rendu. La sortie se fait en vectoriel, prête à être affichée, imprimée, agrandie, exportée dans une multitude de formats sans perte de qualité ;
- rapidité des retouches. L'utilisateur rectifie les alignements en insérant des éléments invisibles, en dupliquant des coordonnées ou en ajustant des facteurs mutiplicatifs : là encore, il travaille sur une description textuelle, et non directement sur le dessin.

Mocodo est libre, gratuit et multiplateforme. Si vous l'aimez, répandez la bonne nouvelle en incluant l'un de ses logos dans votre support : cela augmentera ses chances d'attirer des contributeurs qui le feront évoluer.

Pour vous familiariser avec Mocodo, le mieux est d'utiliser [sa version en ligne](https://www.mocodo.net).
