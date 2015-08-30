
---


---


# Attention: cette documentation en ligne a été générée par conversion d'un document txt2tags en Google Code Wiki, qui  ne gère pas les italiques et le soulignement. Ceux-ci étant indispensables à la compréhension des exemples de MLD donnés, merci de vous reporter à la documentation PDF livrée avec le logiciel. #


---


---


# Passage aux modèles logique et physique #

À partir de la version 1.1, en plus d'une vue du schéma entité-association (MCD), Mocodo génère une ou plusieurs descriptions du schéma relationnel (MLD). La version 1.4 étend ce formalisme à la génération d'un modèle physique de données (en MySQL).

## Cas réguliers ##

### Algorithme ###

La séquence d'opérations suivante est réalisée:

  1. Pour chaque entité, une table de même nom et de mêmes attributs est créée. Le ou les identifiants de l'entité constituent la clef primaire de la table.
  1. Toute table issue d'une entité faible est renforcée, c'est-à-dire que la clef primaire de l'entité qu'elle détermine fonctionnellement vient s'adjoindre à sa clef primaire.
  1. Les associations sont traitées ainsi:
    * si toutes les pattes de l'association portent la cardinalité maximale N, une table de même nom et de mêmes attributs est créée. Sa clef primaire est constituée de l'ensemble des clefs primaires des tables issues des entités mises en jeu;
    * dans le cas contraire, c'est-à-dire si l'une des pattes de l'association porte la cardinalité (1,1), ou à défaut (0,1), l'entité distinguée se voit adjoindre:
      * en tant que clefs étrangères, l'ensemble des clefs primaires des autres entités mises en jeu;
      * en tant qu'attributs, l'ensemble des attributs de l'association.
  1. Les noms des attributs migrants sont éventuellement décorés du nom de leur entité d'origine et/ou de l'association de transit.
  1. Les attributs homonymes pouvant subsister à l'intérieur de chaque table sont différenciés par un suffixe numérique.
  1. L'ensemble de tables résultant est mis en forme en fonction du format de sortie souhaité (html, LaTeX, txt2tags, MySQL, etc.).

### Exemple du traitement des associations non DF ###

Le premier cas de l'opération 3 est illustré sur un MCD comportant des associations triple, double et réflexive dont toutes les cardinalités maximales sont à N.

> ![http://dl.dropbox.com/u/3108405/mocodo-data/mld1.png](http://dl.dropbox.com/u/3108405/mocodo-data/mld1.png)

  * **LACUS** (blandit, elit)
  * **TELLUS** (integer, odio)
  * **BIBENDUM** (#integer.1, #integer.2, consequat)
  * **FAUCIBUS** (#congue, #integer, ipsum)
  * **LIGULA** (#blandit, #congue, #integer, metus)
  * **EROS** (congue, nibh, tincidunt)

Notez la numérotation automatique des deux attributs homonymes de BIBENDUM.

### Exemple du traitement des associations non DF ###

On illustrera le deuxième cas de l'opération 3 par un MCD quasiment identique, à ceci près que certaines cardinalités maximales ont été ramenées à 1. Toutes les associations vont alors disparaître.

> ![http://dl.dropbox.com/u/3108405/mocodo-data/mld2.png](http://dl.dropbox.com/u/3108405/mocodo-data/mld2.png)

  * **EROS** (congue, nibh, tincidunt)
  * **LACUS** (blandit, elit, #congue, #integer, metus)
  * **TELLUS** (integer.1, odio, #integer.2, consequat, #congue, ipsum)

Notez la priorité de (1,1) sur (0,1) lors du traitement de l'association FAUCIBUS.

### Exemple de traitement des entités faibles ###

> ![http://dl.dropbox.com/u/3108405/mocodo-data/mld-weak.png](http://dl.dropbox.com/u/3108405/mocodo-data/mld-weak.png)

  * **BIBENDUM** (#blandit, #congue, #odio, integer)
  * **CONSEQUAT** (odio, faucibus, ipsum)
  * **LACUS** (blandit, elit, ligula, eros)
  * **METUS** (#blandit, congue, nibh, tincidunt)

Notez le renforcement de la clef primaire des tables METUS et BIBENDUM. Tout se passe comme si l'entité METUS possédait à l'origine un identifiant double.

## Cas irréguliers ##

Les règles de gestion peuvent parfois conduire à remettre en cause l'application mécanique de l'algorithme expliqué dans la sous-section précédente. Mocodo est capable de traiter certaines exceptions, pourvu qu'elles lui soient indiquées.

### Réduire une clef primaire ###

Il arrive qu'un sous-ensemble strict de l'ensemble des identifiants des entités mises en jeu dans une association dont toutes les pattes portent la cardinalité N, suffise à constituer la clef primaire de la table issue de cette association: cela se traduit par un dessoulignement des identifiants n'appartenant pas à ce sous-ensemble. Pour obtenir le même résultat avec Mocodo, il suffit de préfixer les entités concernées par une barre oblique.

#### Fichier d'entrée ####

```
LACUS: blandit, elit
LIGULA, 0N LACUS, 1N /EROS, 0N TELLUS: metus
EROS: congue, nibh, tincidunt

TELLUS: integer, odio
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/mld-reduc.png](http://dl.dropbox.com/u/3108405/mocodo-data/mld-reduc.png)

  * **EROS** (congue, nibh, tincidunt)
  * **LACUS** (blandit, elit)
  * **LIGULA** (#blandit, #congue, #integer, metus)
  * **TELLUS** (integer, odio)

Notez que la barre oblique de EROS n'apparaît pas dans le MCD, mais qu'elle conduit à la réduction de la clef primaire de LIGULA aux seuls identifiants des deux autres entités mises en jeu.

### Éviter les champs vides ###

En l'absence d'une cardinalité (1,1), Mocodo traite par défaut la cardinalité (0,1) comme une dépendance fonctionnelle. Or, lorsque le 0 est grand devant le 1 en termes de fréquence d'apparition, la plupart des cellules de la clef étrangère ainsi constituée restent vides. On forcera la conversion de l'association en table en préfixant d'une barre oblique l'une au moins des entités non distinguées par le (0,1).

#### Fichier d'entrée ####

```
LACUS: blandit, elit
LIGULA, 01 LACUS, 1N /EROS: metus
EROS: congue, nibh, tincidunt
```

#### Sortie brute ####

> ![http://dl.dropbox.com/u/3108405/mocodo-data/mld-add.png](http://dl.dropbox.com/u/3108405/mocodo-data/mld-add.png)

  * **LACUS** (blandit, elit)
  * **LIGULA** (#blandit, #congue, metus)
  * **EROS** (congue, nibh, tincidunt)

## Mise en forme ##

Le passage au relationnel se fait en deux étapes:

  1. la création d'une représentation **interne** complète du MLD;
  1. la traduction de celle-ci en une représentation **externe** dans le ou les formats de sortie souhaités.

Chaque format de sortie est défini dans un fichier JSON placé dans le répertoire `tables`. La distribution inclut des fichiers prêts à l'emploi pour les formats suivants:

  * **[Texte brut](http://fr.wikipedia.org/wiki/Fichier_texte)**. À ouvrir directement avec un éditeur de texte Unicode.
  * **[Html](http://fr.wikipedia.org/wiki/HTML).** À ouvrir directement avec un navigateur internet ou un programme de traitement de texte (dont Microsoft Word, OpenOffice, Apple Pages, etc.)
  * **[Txt2tags](http://fr.wikipedia.org/wiki/txt2tags).** À compiler avec le générateur de documents [Txt2tags](http://txt2tags.sourceforge.net/) pour une sortie dans de nombreux formats: HTML, XHTML, SGML, LaTeX, Lout, Man page, Wikipedia, Google Code Wiki, DokuWiki, MoinMoin, MagicPoint, PageMaker, texte brut.
  * **[LaTeX](http://fr.wikipedia.org/wiki/LaTeX)**. À compiler sous LaTeX pour une sortie de haute qualité aux formats PDF ou PostScript.
  * **[MySQL](http://www.mysql.fr/)**. À importer avec MySQL.

### Exemples ###

> ![http://dl.dropbox.com/u/3108405/mocodo-data/geo.png](http://dl.dropbox.com/u/3108405/mocodo-data/geo.png)

#### Sortie en texte brut ####

```
SOLLICITUDIN (_#diam.1_, _#elit_, _#diam.2_, _#ipsum_, lectus)
SEMPER (_#ultricies_, _#cras_, _#ligula_)
RISUS (_ultricies.1_, _cras.1_, elementum, #ultricies.2, #cras.2)
MAECENAS (_#ligula.1_, _#ligula.2_)
DIGNISSIM (_ligula_, massa, varius, #ultricies, #cras, #elit, nec)
CONSECTETUER (_elit_, sed)
--- SUSPENDISSE (_diam_)
LOREM (_#diam_, _ipsum_, dolor, sit, #elit, adipiscing)
```

#### Sortie en html ####

```
<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.0 Transitional//EN'>
<HTML>
<HEAD>
<META HTTP-EQUIV='Content-Type' CONTENT='text/html; charset=utf8'> 
</HEAD><BODY BGCOLOR='white' TEXT='black'>
<FONT SIZE='4'>
</FONT></CENTER>
<B>SOLLICITUDIN</B> (<U><I>diam.1</I></U>, <U><I>elit</I></U>, <U><I>diam.2</I></U>,
 <U><I>ipsum</I></U>, lectus)<BR>
<B>SEMPER</B> (<U><I>ultricies</I></U>, <U><I>cras</I></U>, <U><I>ligula</I></U>)<BR>
<B>RISUS</B> (<U>ultricies.1</U>, <U>cras.1</U>, elementum, <I>ultricies.2</I>,
 <I>cras.2</I>)<BR>
<B>MAECENAS</B> (<U><I>ligula.1</I></U>, <U><I>ligula.2</I></U>)<BR>
<B>DIGNISSIM</B> (<U>ligula</U>, massa, varius, <I>ultricies</I>, <I>cras</I>,
 <I>elit</I>, nec)<BR>
<B>CONSECTETUER</B> (<U>elit</U>, sed)<BR>
<!-- <B>SUSPENDISSE</B> (<U>diam</U>)<BR> -->
<B>LOREM</B> (<U><I>diam</I></U>, <U>ipsum</U>, dolor, sit, <I>elit</I>, adipiscing)<BR>
</BODY></HTML>
```

#### Sortie en txt2tags ####

```
%!encoding: utf8
- **SOLLICITUDIN** (__#diam.1__, __#elit__, __#diam.2__, __#ipsum__, lectus)
- **SEMPER** (__#ultricies__, __#cras__, __#ligula__)
- **RISUS** (__ultricies.1__, __cras.1__, elementum, #ultricies.2, #cras.2)
- **MAECENAS** (__#ligula.1__, __#ligula.2__)
- **DIGNISSIM** (__ligula__, massa, varius, #ultricies, #cras, #elit, nec)
- **CONSECTETUER** (__elit__, sed)
% - **SUSPENDISSE** (__diam__)
- **LOREM** (__#diam__, __ipsum__, dolor, sit, #elit, adipiscing)
```

Le résultat de la compilation de ce texte source apparaît ci-dessous, transformé en LaTeX ou en Google Code Wiki selon que vous lisez cette documentation (elle-même écrite en txt2tags) en PDF ou sur le site du programme:

  * **SOLLICITUDIN** (#diam.1, #elit, #diam.2, #ipsum, lectus)
  * **SEMPER** (#ultricies, #cras, #ligula)
  * **RISUS** (ultricies.1, cras.1, elementum, #ultricies.2, #cras.2)
  * **MAECENAS** (#ligula.1, #ligula.2)
  * **DIGNISSIM** (ligula, massa, varius, #ultricies, #cras, #elit, nec)
  * **CONSECTETUER** (elit, sed)
  * **LOREM** (#diam, ipsum, dolor, sit, #elit, adipiscing)

#### Sortie en LaTeX ####

Pour une mise en forme LaTeX plus souple, on choisira la sortie directe:

```
\begin{mld}
  \relat{Sollicitudin} & (\prim{\foreign{diam.1}}, \prim{\foreign{elit}},
 \prim{\foreign{diam.2}}, \prim{\foreign{ipsum}}, \attr{lectus})\\
  \relat{Semper} & (\prim{\foreign{ultricies}}, \prim{\foreign{cras}},
 \prim{\foreign{ligula}})\\
  \relat{Risus} & (\prim{ultricies.1}, \prim{cras.1}, \attr{elementum},
 \foreign{ultricies.2}, \foreign{cras.2})\\
  \relat{Maecenas} & (\prim{\foreign{ligula.1}}, \prim{\foreign{ligula.2}})\\
  \relat{Dignissim} & (\prim{ligula}, \attr{massa}, \attr{varius},
 \foreign{ultricies}, \foreign{cras}, \foreign{elit}, \attr{nec})\\
  \relat{Consectetuer} & (\prim{elit}, \attr{sed})\\
%   \relat{Suspendisse} & (\prim{diam})\\
  \relat{Lorem} & (\prim{\foreign{diam}}, \prim{ipsum}, \attr{dolor},
 \attr{sit}, \foreign{elit}, \attr{adipiscing})\\
\end{mld}
```

Les différentes commandes devront bien sûr être définies dans le préambule de votre document. À titre d'exemple, voici celles que j'utilise dans mes propres supports:

```
\usepackage[normalem]{ulem}

\newenvironment{mld}
{\par\begin{minipage}{\linewidth}\begin{tabular}{rp{0.7\linewidth}}}
{\end{tabular}\end{minipage}\par}
\newcommand{\relat}[1]{\textsc{#1}}
\newcommand{\attr}[1]{\emph{#1}}
\newcommand{\prim}[1]{\uline{#1}}
\newcommand{\foreign}[1]{\#\textsl{#1}}
```

> ![http://dl.dropbox.com/u/3108405/mocodo-data/latex.png](http://dl.dropbox.com/u/3108405/mocodo-data/latex.png)

#### Sortie en MySQL ####

Pour qu'elle soit exploitable directement, il convient d'ajouter un type entre crochets après chaque attribut. Voir la section _Syntaxe de description du MCD_, sous-section _Besoin plus avancés_ pour un exemple complet.

(Prière de consulter la documentation en PDF pour une restitution en qualité optimale.)

### Configuration ###

Vous pouvez configurer selon vos propres besoins la sortie tabulaire de Mocodo, soit en modifiant les fichiers de configuration existants dans le répertoire `tables`, soit en en créant de nouveaux (conseillé). Les paramètres sont les suivants:

`addForeignKey` (facultatif).
Au niveau physique, la prise en compte de clefs étrangères se fait _a posteriori_ par altération des tables créées précédemment. Vous devez combiner `%(table)s` (la table à altérer), `%(foreignKey)s` (la clef étrangère) et `%(foreignTable)s` (la table de référence).
`attributeWithType` (facultatif).
La manière de combiner un nom d'attribut avec son type lorsque celui-ci est donné dans le MCD d'entrée (entre crochets). La plupart des formats de sortie n'en tiennent pas compte: `"%(attribute)s"`, mais si l'on souhaite inclure cette information du modèle physique, on écrira par exemple pour MySQL: `"%(attribute)s %(attributeType)s"`.
`closing`.
Le texte à composer à la fin, typiquement des balises fermantes.
`columnSep`.
Une chaîne à insérer entre deux noms de colonnes consécutifs, typiquement une virgule, un retour-chariot ou une tabulation.
`comment`.
Si vous souhaitez que les tables réduites à un unique attribut soit commentées dans le résultat, et donc disparaissent à la compilation, précisez la syntaxe de commentaire du langage cible. Dans le cas contraire, mettez juste " `%s`" pour composer la table telle quelle.
`df`.
Pour limiter l'appauvrissement sémantique dû à la suppression des dépendances fonctionnelles, il est possible de préciser l'origine d'une clef étrangère en faisant référence, non seulement à son nom (`%(attribute)s`), mais aussi à celui de l'entité dont elle issue (`%(entity)s`) et/ou de l'association par laquelle elle a transité (`%(association)s`). On écrira par exemple: `"%(attribute)s de %(entity)s par %(association)s"`.
`distinguish`.
Les attributs résultants homonymes peuvent être numérotés automatiquement, par exemple en texte brut: `"%(label)s.%(count)s"`. Si l'on ne veut pas de cette différenciation, on écrira simplement: `"%(label)s"`.
`extension`.
L'extension du nom de fichier de sortie, sa base étant identique à celle du fichier de sortie graphique spécifié avec l'argument `output` du programme (par défaut, `sandbox`).
`foreignPrimary`.
La mise en forme à appliquer aux clefs simultanément primaires et étrangères, typiquement un soulignement et un dièse en préfixe. Mêmes possibilités que le paramètre `table`.
`foreign`.
La mise en forme à appliquer aux clefs étrangères, typiquement un dièse en préfixe. Mêmes possibilités que le paramètre `table`.
`lineSep`.
Une chaîne à insérer éventuellement entre deux `line`s consécutives.
`line`.
La manière de composer une table complète, typiquement le nom de la table (`%(table)s`) suivi du nom des colonnes (`%(columns)s`). Comme son nom ne l'indique pas, il est tout à fait possible que le résultat de la composition occupe plusieurs lignes.
`nonDf`.
Les clefs étrangères des autres types d'association pourront de la même manière se voir qualifier par le nom de leur entité d'origine: `"%(attribute)s de %(entity)s"`. Le paramètre `%(association)s` est disponible, mais inutile ici.
`opening`.
Le texte à composer au tout début, typiquement un préambule et des balises ouvrantes.
`primary`.
La mise en forme à appliquer aux attributs faisant partie de la clef primaire, typiquement un soulignement. Mêmes possibilités que le paramètre `table`.
`primarySep`.
Le séparateur de la liste d'attributs constituant la clef primaire, disponible dans le paramètre `%(primaryList)s` et utile pour la sortie en SQL.
`replace`.
Une liste de couples de motifs de recherche et de remplacement. Par exemple, en LaTeX, `[["_","\\_"],["\$","\\$"]]` permettra d'échapper tout les symboles de soulignement et tous les dollars. Notez que les motifs de recherche et de remplacement suivent la syntaxe des expressions régulières. Si vous rencontrez des erreurs en utilisant ce paramètre, reportez-vous au [chapitre correspondant de la documentation de Python](http://docs.python.org/library/re.html).
`simple`.
La mise en forme à appliquer aux attributs normaux, typiquement rien du tout. Mêmes possibilités que le paramètre `table`.
`strengthen`.
La conversion en relationnel d'une entité faible étant assez délicate, on pourra de la même manière vouloir l'expliciter: `"renforcement par %(attribute)s de %(entity)s transitant par %(association)s"`.
`table`.
La mise en forme à appliquer au nom de chaque table. Pour html, par exemple, `"<B>%s</B>"` signifie que le nom (représenté par `%s`) doit apparaître en gras. Un changement de casse peut être appliqué en remplaçant `%s` par `%(lower)s` (minuscules), `%(upper)s` (capitales), `%(capitalize)s` (capitale initiale, minuscules pour le reste) ou `%(title)s` (capitale à l'initiale de chaque mot, minuscules pour le reste).