# Lancement de l'application #

## Au plus simple ##

Le programme se lance à partir d'une console en tapant:

```
python mocodo.py
```

Invoqué sous cette forme, le script prend tous ses paramètres d'un fichier `default.json` situé dans son répertoire. Le texte du MCD lui-même se trouve aussi au même endroit, sous le nom de `sandbox.mcd`. Ne vous inquiétez pas si ces deux fichiers n'existent pas dans l'archive que vous avez téléchargée: lors du premier lancement, le script en créera automatiquement et de façon transparente une version adaptée à votre installation.

## Paramétrage occasionnel ##

Les arguments suivants sont reconnus:

  * `--attraction=`... ou `-a=`...
Distance horizontale (par défaut 40 pixels) en-deçà de laquelle les centres des boîtes seront alignés verticalement.
  * `--cleanup`
Termine immédiatement après avoir recréé dans le répertoire principal les fichiers `default.json` et `sandbox.mcd` à partir de ceux conservés dans le répertoire `pristine`, comme au premier lancement (voir plus loin).
  * `--colors=`... ou `-c=`...
Le nom de la palette de couleurs à utiliser, par défaut `bw`. Les palettes sont stockées dans le répertoire `colors`.
  * `--default=`...
Chemin du fichier de paramètres par défaut. En l'absence de ce paramètre, c'est le fichier `default.json` du répertoire du script qui est lu.
  * `--df=`...
Le sigle à afficher dans une dépendance fonctionnelle, par défaut `DF`.
  * `--encodings=`... ou `-e=`...
Les [encodages](http://docs.python.org/library/codecs.html#standard-encodings) à essayer pour lire le fichier d'entrée, séparés par des virgules, par défaut `utf8`.
  * `--extract` ou `-x`
Les paramètres géométriques sont placés dans un fichier JSON séparé, et non au début du script Python généré.
  * `--help` ou `-h`
Un court message d'aide.
  * `--input=`... ou `-i=`...
Le chemin complet du fichier d'entrée, par défaut `sandbox.mcd`. Les fichiers de sortie seront écrits dans le même répertoire.
  * `--language=`... ou `-l=`...
Le code de la langue à utiliser pour la localisation des messages, au cas où celle détectée automatiquement par le logiciel ne convient pas.
  * `--tables=`... ou `-m=`...
Les formats de sortie tabulaires (MLD ou MPD), séparés par des virgules. Cf. répertoire `tables`.
  * `--output=`... ou `-o=`...
Le format produit par le script Python généré en sortie, par défaut `svg` ou `nodebox` selon votre installation.
  * `--sep=`...
Le séparateur à afficher entre les cardinalités minimales et maximales, par défaut une virgule.
  * `--shapes=`... ou `-s=`...
Le nom du dictionnaire de définition des polices, dimensions, etc., cf. répertoire `shapes`.
  * `--tkinter`
Tkinter est utilisé pour calculer la dimension des chaînes.
  * `--version` ou  ou `-v`...
Le numéro de version.

#### Exemple ####

```
python mocodo.py --input="test.mcd" --colors="mondrian" --output="svg" --df="CIF"
```

## Paramétrage à long terme ##

Au premier lancement, Mocodo essaie de déterminer s'il opère sous Windows, Linux ou Mac OS X. Dans ce dernier cas, il cherche en outre si Nodebox est installé. Il crée alors un fichier de paramètres `default.json` adapté, fichier qu'il relira à chaque lancement ultérieur. Vous êtes encouragés à modifier ce fichier selon vos goûts. De la sorte, le style de vos MCD pourra être maintenu à moindre frais à travers tous vos documents. En cas de besoin, vous pourrez toujours ponctuellement passer outre ces réglages en en précisant d'autres en ligne de commande.

## Accents et symboles spéciaux ##

Les accents présents dans votre fichier d'entrée sont correctement gérés pourvu que vous ayez enregistré celui-ci dans l'encodage attendu par Mocodo en entrée: c'est par défaut _Unicode utf8_. Une tolérance existe: si Mocodo échoue à décoder votre fichier avec _utf8_, il se rabattra sur le codec d'Europe de l'Ouest associé historiquement à votre plateforme: _iso-8859-15_ pour Windows et Linux, _mac-roman_ pour Mac OS X.

Si les accents n'apparaissent pas correctement, vous aurez encore trois solutions:

  * soit, ré-enregistrer votre fichier en _utf8_ (conseillé) ou dans un encodage historique;
  * soit (à long terme), modifier dans `default.json` la liste des encodages pris en charge;
  * soit (ponctuellement), passer l'encodage de votre fichier en argument à `mocodo.py`.