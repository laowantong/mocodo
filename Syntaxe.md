# Syntaxe de description du MCD #

## Besoins élémentaires ##

### Entités, associations, attributs, identifiants, cardinalités ###

#### Fichier d'entrée ####

```
CLIENT: Réf. client, Nom, Prénom, Adresse
PASSER, 0N CLIENT, 11 COMMANDE
COMMANDE: Num commande, Date, Montant
INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
PRODUIT: Réf. produit, Libellé, Prix unitaire
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/basics.png](http://dl.dropbox.com/u/3108405/mocodo-data/basics.png)

La syntaxe ne devrait pas poser problème. À noter:

  * la liste des cardinalités / entités mises en jeu par une association s'intercale entre le nom et l'éventuelle liste d'attributs de celle-ci;
  * le premier attribut d'une entité est considéré par défaut comme son identifiant, et donc souligné;
  * pour les associations sans attributs, le deux-points est facultatif.

#### Options ####

Il est possible de remplacer la virgule séparatrice des cardinalités par une chaîne quelconque, par exemple vide:

```
python mocodo.py --sep=""
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/basics-nocomma.png](http://dl.dropbox.com/u/3108405/mocodo-data/basics-nocomma.png)

### Dépendances fonctionnelles ###

#### Fichier d'entrée ####

```
CLIENT: Réf. client, Nom, Prénom, Adresse
DF, 0N CLIENT, 11 COMMANDE
COMMANDE: Num commande, Date, Montant
INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
PRODUIT: Réf. produit, Libellé, Prix unitaire
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/df.png](http://dl.dropbox.com/u/3108405/mocodo-data/df.png)

#### Options ####

Il est possible d'activer l'encerclement d'un autre sigle que DF, par exemple:

```
python mocodo.py --df=CIF
```

C'est ce sigle qui devra alors apparaître en entrée:

```
...
CIF, 0N CLIENT, 11 COMMANDE
...
```

Pour placer le sigle à la bonne hauteur dans ce cercle plus grand, il est de plus nécessaire de modifier (a priori une fois pour toutes) le ratio défini dans le dictionnaire `trebuchet` de `shapes`:

```
"dfTextHeightRatio"             : 1.00,
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/cif.png](http://dl.dropbox.com/u/3108405/mocodo-data/cif.png)

### Associations réflexives ###

#### Fichier d'entrée ####

```
HOMME: Num. SS, Nom, Prénom
ENGENDRER, 0N HOMME, 11 HOMME
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/reflexive.png](http://dl.dropbox.com/u/3108405/mocodo-data/reflexive.png)

### Placement sur plusieurs lignes ###

#### Fichier d'entrée ####

```
LACUS: blandit, elit, ligula
EROS, 11 LACUS, 1N TELLUS: metus, congue

NIBH, 1N LACUS, 11 TELLUS
TELLUS: tincidunt, bibendum, consequat, integer
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/mapping.png](http://dl.dropbox.com/u/3108405/mocodo-data/mapping.png)

L'ordre et la séparation des lignes de la description permet de spécifier à coût zéro un plongement grossier, mais qui se révèle souvent suffisant:

  * les éléments sont placés de gauche à droite dans l'ordre de leur énumération;
  * le retour à la ligne se fait en insérant une ligne blanche dans la description.

Par défaut, les centres des entités et des associations d'une même ligne sont alignés horizontalement. Les lignes sont centrées. Depuis la version 1.2, le système tente d'aligner verticalement les centres dont les abscisses sont égales à une constante près. Cette constante, nommée `attraction` peut être spécifiée, soit en argument, soit dans le fichier de paramètres `default.json`. Une valeur de 0 désactive l'attraction.

Les autres types d'alignement ou de décalage demandent à intervenir manuellement sur le fichier de sortie.

## Besoins plus avancés ##

### Identifiants multiples ###

#### Fichier d'entrée ####

```
POINT: lassitude, _longuitude, bravitude
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/multiple.png](http://dl.dropbox.com/u/3108405/mocodo-data/multiple.png)

### Identifiants faibles ###

#### Fichier d'entrée ####

```
ŒUVRE: Cote œuvre, Titre, Date parution
DF, 1N ŒUVRE, 11 EXEMPLAIRE
EXEMPLAIRE: -Num. exemplaire, État du livre, Date d'achat
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/weak.png](http://dl.dropbox.com/u/3108405/mocodo-data/weak.png)

Un soulignement pointillé dénote les identifiants faibles.

### Étiquettes et flèches sur les pattes ###

#### Fichier d'entrée ####

```
Personne1: Num. SS, Nom, Prénom, Sexe
Engendrer1, 0Nenfant Personne1, 02parent Personne1
Personne2: Num. SS, Nom, Prénom, Sexe
Engendrer2, 0N< Personne2, 1N> Personne2
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/legs.png](http://dl.dropbox.com/u/3108405/mocodo-data/legs.png)

Les définitions d'étiquettes sont prévues dans la syntaxe, mais encore ignorées par la version actuelle. À partir de la version 1.3, les flèches sont effectivement tracées.

### Styles ###

Plusieurs styles prédéfinis sont distribués avec l'application. Un style se définit comme la combinaison d'une palette de couleurs (répertoire `colors`) avec un dictionnaire de polices et de dimensions (répertoire `shapes`). Vous pouvez bien sûr créer les vôtres en vous inspirant des fichiers fournis. Si vous êtes particulièrement content d'un style, soumettez-le pour inclusion dans une prochaine distribution.

### Types ###

À partir de la version 1.4, chaque attribut peut être assorti d'un type (entre crochets):

```
CLIENT: Réf. client [varchar(8)], Nom [varchar(20)], Adresse [varchar(40)]
DF, 0N CLIENT, 11 COMMANDE
COMMANDE: Num commande [tinyint(4)], Date [date], Montant [decimal(5,2) DEFAULT '0.00']
INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
PRODUIT: Réf. produit [varchar(8)], Libellé [varchar(20)], Prix unitaire [decimal(5,2)]
```

Actuellement ignorés au niveau du MCD, les types sont utiles à la génération d'un modèle physique de données. À titre d'exemple, la distribution inclut le fichier de style `mysql.json` qui sert à établir la sortie suivante, directement importable par MySQL:

```
CREATE TABLE `PRODUIT` (
  `Réf. produit` varchar(8),
  `Libellé` varchar(20),
  `Prix unitaire` decimal(5,2),
  PRIMARY KEY(`Réf. produit`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `CLIENT` (
  `Réf. client` varchar(8),
  `Nom` varchar(20),
  `Adresse` varchar(40),
  PRIMARY KEY(`Réf. client`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `COMMANDE` (
  `Num commande` tinyint(4),
  `Date` date,
  `Montant` decimal(5,2) DEFAULT '0.00',
  `Réf. client` varchar(8),
  PRIMARY KEY(`Num commande`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `INCLURE` (
  `Num commande` tinyint(4),
  `Réf. produit` varchar(8),
  `Quantité` tinyint(4),
  PRIMARY KEY(`Num commande`, `Réf. produit`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

ALTER TABLE `COMMANDE` ADD FOREIGN KEY (`Réf. client`) REFERENCES `CLIENT` (`Réf. client`);

ALTER TABLE `INCLURE` ADD FOREIGN KEY (`Num commande`) REFERENCES `COMMANDE` (`Num commande`);

ALTER TABLE `INCLURE` ADD FOREIGN KEY (`Réf. produit`) REFERENCES `PRODUIT` (`Réf. produit`);
```

## Besoins spécifiques à la pédagogie ##

### Laisser vierges des attributs ou des cardinalités ###

Les MCD à trous sont des exercices classiques d'introduction aux bases de données. Mocodo offre deux méthodes distinctes pour les produire.

Vous pouvez « trouer » n'importe quel MCD en rendant complètement transparentes les couleurs des attributs, associations et cardinalités. Le style `blank` a été prédéfini à cet effet:

```
python mocodo.py --colors=blank
```

L'autre méthode (plus souple) demande à modifier le MCD d'entrée:

#### Fichier d'entrée ####

```
CLIENT: , , , 
PASSER, XX CLIENT, XX COMMANDE
COMMANDE: , , 
INCLURE, XX COMMANDE, XX PRODUIT: 
PRODUIT: , , 
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/blank.png](http://dl.dropbox.com/u/3108405/mocodo-data/blank.png)

  * Une liste de _n_ virgules permet de réserver la place de _n+1_ attributs;
  * les cardinalités `XX` n'apparaissent pas dans le MCD résultant.

### Dupliquer des entités ou des associations ###

#### Fichier d'entrée ####

```
ŒUVRE: 612.NAT.34, J'apprends à lire à mes souris blanches, mai 1975

DF1, XX ŒUVRE, XX EXEMPLAIRE1
DF2, XX ŒUVRE, XX EXEMPLAIRE2
DF3, XX ŒUVRE, XX EXEMPLAIRE3

EXEMPLAIRE1: 1, bon état, 12/6/1975
EXEMPLAIRE2: 2, bon état, 1/8/1977
EXEMPLAIRE3: 3, reliure rongée, 3/4/2005
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/extension.png](http://dl.dropbox.com/u/3108405/mocodo-data/extension.png)

Cette fonctionnalité permet de préparer des vues en extension, ou de figurer par exemple par le même symbole DF plusieurs dépendances fonctionnelles d'un MCD en compréhension.

  * Les suffixes numériques des entités ou des associations n'apparaissent pas dans le MCD résultant.