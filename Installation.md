# Installation #

| **Pour...** | **Windows** | **Debian (Ubuntu, etc.)** | **Mac OS X** |
|:------------|:------------|:--------------------------|:-------------|
| ouvrir l'archive `.tar.gz` | [7-zip](http://www.framasoft.net/article1025.html) |                           |              |
| éditer le MCD d'entrée | [Notepad++](http://notepad-plus.sourceforge.net/fr/site.htm) |                           |              |
| lancer le script `mocodo` | [Python 2.6 ou 2.7](http://python.org/download/) | `sudo apt-get install python-tk` |              |
| voir le MCD produit | [Firefox](http://www.mozilla-europe.org/fr/firefox/) |                           |              |
| le retoucher et l'exporter | [Inkscape](http://www.inkscape.org/download/?lang=fr) | `sudo apt-get install inkscape` | [Nodebox 1.x](http://nodebox.net/code/index.php/Home) |

Mocodo lui-même est un simple petit script, qui peut être lancé directement à partir de l'endroit où vous aurez décompressé l'archive téléchargée. Mais il est juché sur des épaules de géants, notamment Python et Nodebox ou Inkscape. Le tableau ci-dessus résume ce que vous devriez avoir à installer selon votre système. Les cases vides signifient que le logiciel requis est pré-installé.

#### N.B. ####

Sur Mac et Linux, il se peut que vous ayez à mettre à jour en 2.6 ou 2.7 votre version de Python. Si vous tenez à faire fonctionner Mocodo avec Python 2.5, vous devrez installer le paquetage supplémentaire [simplejson](http://pypi.python.org/pypi/simplejson/).