**11 septembre 2022.** Mocodo 3.0 introduit l'[héritage](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Héritage-(ou-spécialisation)), l'[agrégation](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Agrégation-(ou-pseudo-entité)), les [calques](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Héritage-(ou-spécialisation)), les [sorties PDF et PNG](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html#Héritage-(ou-spécialisation)), [etc](https://github.com/laowantong/mocodo/releases/tag/3.0).

------

![](https://cdn.rawgit.com/laowantong/mocodo/master/logos/banner.svg)

Mocodo est un logiciel d'aide à l'enseignement et à la conception des [bases de données relationnelles](https://fr.wikipedia.org/wiki/Base_de_données_relationnelle).

- En entrée, il prend une description textuelle des entités et associations du modèle conceptuel de données ([MCD](https://fr.wikipedia.org/wiki/Modèle_entité-association)).
- En sortie, il produit son diagramme entité-association en [SVG](https://fr.wikipedia.org/wiki/Scalable_Vector_Graphics) et son schéma relationnel ([MLD](
https://fr.wikipedia.org/wiki/Merise_%28informatique%29#MLD_:_mod.C3.A8le_logique_des_donn.C3.A9es)) en [SQL](https://fr.wikipedia.org/wiki/Structured_Query_Language), [LaTeX](https://fr.wikipedia.org/wiki/LaTeX), [Markdown](https://fr.wikipedia.org/wiki/Markdown), etc.

Ci-dessous, un exemple sous [Jupyter Notebook](https://jupyter.org). L'appel du programme se fait en première ligne, sur un texte d'entrée donné lignes suivantes.

```
%%mocodo --mld --colors brewer+1 --shapes copperplate --relations diagram markdown_data_dict
DF, 11 Élève, 1N Classe
Classe: Num. classe, Num. salle
Faire Cours, 1N Classe, 1N Prof: Vol. horaire
Catégorie: Code catégorie, Nom catégorie

Élève: Num. élève, Nom élève
Noter, 1N Élève, 0N Prof, 0N Matière, 1N Date: Note
Prof: Num. prof, Nom prof
Relever, 0N Catégorie, 11 Prof

Date: Date
Matière: Libellé matière
Enseigner, 11 Prof, 1N Matière
```

En sortie, le MCD (diagramme conceptuel) et le MLD (schéma relationnel) correspondants:

![](https://cdn.rawgit.com/laowantong/mocodo/master/doc/readme_1.svg)

**Catégorie** (<ins>Code catégorie</ins>, Nom catégorie)  
**Classe** (<ins>Num. classe</ins>, Num. salle)  
**Élève** (<ins>Num. élève</ins>, Nom élève, _Num. classe_)  
**Faire Cours** (<ins>_Num. classe_</ins>, <ins>_Num. prof_</ins>, Vol. horaire)  
**Noter** (<ins>_Num. élève_</ins>, <ins>_Num. prof_</ins>, <ins>_Libellé matière_</ins>, <ins>_Date_</ins>, Note)  
**Prof** (<ins>Num. prof</ins>, Nom prof, _Libellé matière_, _Code catégorie_)  

L'appel ci-dessus a également construit le dictionnaire des données:

- Num. classe
- Num. salle
- Vol. horaire
- Code catégorie
- Nom catégorie
- Num. élève
- Nom élève
- Note
- Num. prof
- Nom prof
- Date
- Libellé matière

Ainsi que le diagramme relationnel, qui peut être visualisé par un nouvel appel:

```
%mocodo --input mocodo_notebook/sandbox.mld --colors brewer+1
```

![](https://cdn.rawgit.com/laowantong/mocodo/f06f70a/doc/readme_2.svg)

La devise de Mocodo, « nickel, ni souris », en résume les principaux points forts:

- description textuelle des données. L'utilisateur n'a pas à renseigner, placer et déplacer des éléments comme avec une lessive ordinaire. Il ne fournit rien de plus que les informations définissant son MCD. L'outil s'occupe tout seul du plongement;
- propreté du rendu. La sortie se fait en vectoriel, prête à être affichée, imprimée, agrandie, exportée dans une multitude de formats sans perte de qualité;
- rapidité des retouches. L'utilisateur rectifie les alignements en insérant des éléments invisibles, en dupliquant des coordonnées ou en ajustant des facteurs mutiplicatifs: là encore, il travaille sur une description textuelle, et non directement sur le dessin.

Mocodo est libre, gratuit et multiplateforme. Si vous l'aimez, répandez la bonne nouvelle en incluant l'un de ses logos dans votre support: cela multipliera ses chances d'attirer des contributeurs qui le feront évoluer.

Pour vous familiariser avec Mocodo, le mieux est d'utiliser [sa version en ligne](https://www.mocodo.net).

Pour en savoir plus, lisez la documentation [au format HTML](https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html) ou téléchargez-la [au format Jupyter Notebook](doc/fr_refman.ipynb).
