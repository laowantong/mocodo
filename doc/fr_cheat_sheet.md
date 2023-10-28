- Opérations de <span style="color:blue; font-family:monospace; font-weight:600;">conversion en bleu</span> et de <span style="color:green; font-family:monospace; font-weight:600;">réécriture en vert</span>.
- Survolez un nom d'opération pour voir ses éventuels alias.

| Sous-option | Description | Exemples | Explications |
| --: | :-- | :-- | :-- |
| <span style="color:green; font-family:monospace; font-weight:600">add</span> | cf. `create` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">anonymise</span> | cf. `drown` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">anonymize</span> | cf. `drown` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">append</span> | cf. `suffix` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">arrange</span> | réarrange la disposition, soit par Branch & Bound, soit avec un algorithme génétique | `` arrange `` | B&B sans contraintes |
|  |  | `` arrange:timeout=60 `` | B&B limité à une minute |
|  |  | `` arrange:wide `` | B&B privilégiant la largeur |
|  |  | `` arrange:current `` | B&B sur la grille courante |
|  |  | `` arrange:balanced=0 `` | B&B sur la plus petite grille équilibrée |
|  |  | `` arrange:balanced=1 `` | B&B sur la seconde plus petite grille équilibrée |
|  |  | `` arrange:algo=ga `` | algorithme génétique |
| <span style="color:green; font-family:monospace; font-weight:600">ascii</span> | réécrit les éléments donnés en ASCII | `` ascii:roles,labels `` | rôles, libellés des boîtes et des attributs en ASCII |
| <span style="color:blue; font-family:monospace; font-weight:600">ast</span> | crée l'arbre de syntaxe abstraite du texte source (pour le débogage) |  |  |
| <span title="Alias : camelcase, camel_case." style="color:green; font-family:monospace; font-weight:600">camel</span> | réécrit les éléments donnés en camelCase |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">camel_case</span> | cf. `camel` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">camelcase</span> | cf. `camel` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">capitalize</span> | réécrit les éléments donnés en capitalisant la première lettre de chaque mot |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">case_fold</span> | cf. `casefold` |  |  |
| <span title="Alias : case_fold." style="color:green; font-family:monospace; font-weight:600">casefold</span> | réécrit les éléments donnés en minuscules, mais plus agressivement que « lower » |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">chen</span> | convertit le modèle conceptuel dans la notation de Chen | `` chen `` | sans attributs |
|  |  | `` chen:attrs `` | avec attributs |
|  |  | `` chen:attrs --defer `` | calcule le rendu graphique via un service web |
|  |  | `` chen:layout=circo,mindist=2,scale=0.6 `` | ajoute des options arbitraires pour Graphviz |
| <span style="color:blue; font-family:monospace; font-weight:600">class_diagram</span> | cf. `uml` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">complete</span> | cf. `create` |  |  |
| <span title="Alias : add, insert, make, guess, infer, complete, new." style="color:green; font-family:monospace; font-weight:600">create</span> | essaie d'inférer les types, entités, CIFs ou flèches de DF à partir des éléments existants | `` guess:types `` | deviner les types manquants |
|  |  | `` create:types= `` | remplacer les types manquants par `[]` |
|  |  | `` create:types=TODO `` | remplacer les types manquants par `[TODO]` |
|  |  | `` make:entities `` | réparer l'oubli d'entités référencées dans des associations |
|  |  | `` create:dfs `` | mettre des DF partout où c'est possible |
|  |  | `` add:df_arrows `` | ajouter des flèches aux DF |
|  |  | `` add:cifs `` | ajouter les CIF correspondant aux agrégats |
|  |  | `` add:cifs=light `` | même chose en visualisation allégée |
|  |  | `` add:roles `` | mettre comme rôles le nom des associations partout où c'est utile |
| <span title="Alias : crowfoot, crowsfoot." style="color:blue; font-family:monospace; font-weight:600">crow</span> | convertit le modèle conceptuel dans la notation crow's foot | `` crow `` | format Graphviz |
|  |  | `` crow --defer `` | calcule le rendu graphique via un service web |
|  |  | `` crow:mmd `` | format Mermaid |
|  |  | `` crow:mermaid `` | idem |
| <span style="color:blue; font-family:monospace; font-weight:600">crowfoot</span> | cf. `crow` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">crowsfoot</span> | cf. `crow` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">cut</span> | cf. `slice` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">d2</span> | convertit le modèle conceptuel en un schéma relationnel au format D2 |  |  |
| <span title="Alias : data_dictionary." style="color:blue; font-family:monospace; font-weight:600">data_dict</span> | extrait tous les attributs du MCD dans une table | `` data_dict `` | tableau Markdown, trois colonnes |
|  |  | `` data_dict:label `` | liste Markdown, une colonne |
|  |  | `` data_dict:label,type='Description' `` | deux colonnes, un libellé personnalisé |
|  |  | `` data_dict:label='Attribut',type='Description' `` | deux colonnes, deux libellés personnalisés |
|  |  | `` data_dict:**box**='Entité ou<br>association',label,`type`=`'Type de données'` `` | mise en forme de certains libellés |
|  |  | `` data_dict:tsv `` | tableau TSV, trois colonnes |
|  |  | `` data_dict:tsv,label `` | liste des attributs séparés par des retours à la ligne |
| <span style="color:blue; font-family:monospace; font-weight:600">data_dictionary</span> | cf. `data_dict` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">dbml</span> | convertit le modèle conceptuel en un schéma relationnel au format DBML | `` dbml `` | version de base |
|  |  | `` dbml:b `` | avec _boilerplate_ |
| <span style="color:blue; font-family:monospace; font-weight:600">ddl</span> | cf. `sql` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">debug</span> | liste des informations internes relatives à la conversion en schéma relationnel |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">del</span> | cf. `delete` |  |  |
| <span title="Alias : del, suppress, erase, remove, hide, empty." style="color:green; font-family:monospace; font-weight:600">delete</span> | supprime les éléments donnés quand c'est possible | `` empty `` | ne garde que la structure et le nom des boîtes |
|  |  | `` delete:types,notes,attrs,cards `` | idem |
|  |  | `` delete:cards `` | remplace les cardinalités par `XX` |
|  |  | `` delete:card_prefixes `` | supprime les marqueurs d'entités faibles et d'agrégats |
|  |  | `` delete:dfs `` | supprime les entités indépendantes dont tous les attributs sont identifiants (et les DF qui les relient) |
| <span style="color:blue; font-family:monospace; font-weight:600">dependencies</span> | convertit le modèle conceptuel en un graphe de dépendances |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">diagram</span> | convertit le modèle conceptuel en un diagramme relationnel au format Mocodo | `` diagram `` | version de base |
|  |  | `` diagram:c `` | avec contraintes d'unicité et d'optionalité |
| <span style="color:green; font-family:monospace; font-weight:600">drain</span> | déplace tout attribut d'association (1,1) vers l'entité appropriée |  |  |
| <span title="Alias : drown_by_numbers, anonymize, anonymise." style="color:green; font-family:monospace; font-weight:600">drown</span> | remplace tous les noms d'éléments par un libellé générique numéroté |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">drown_by_numbers</span> | cf. `drown` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">echo</span> | réécrit le texte source tel quel |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">empty</span> | cf. `delete` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">erase</span> | cf. `delete` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">explode</span> | décompose toute association n-aire (*,N) en n associations binaires | `` explode arrange `` | décomposer les non-DF ternaires et plus, puis réarranger |
|  |  | `` explode:arity=3 arrange `` | idem |
|  |  | `` explode:weak arrange `` | idem, avec création d'entités faibles |
|  |  | `` explode:arity=2.5 arrange `` | étendre aux non-DF binaires porteuses d'attributs |
|  |  | `` explode:arity=2 arrange `` | étendre à toutes les non-DF binaires |
| <span style="color:green; font-family:monospace; font-weight:600">fix</span> | essaie de corriger les erreurs courantes dans les éléments donnés | `` fix:cards `` | normaliser les cardinalités en 01, 11, 0N et 1N |
| <span title="Alias : mirror, reflect." style="color:green; font-family:monospace; font-weight:600">flip</span> | applique au diagramme une symétrie verticale, horizontale ou diagonale | `` flip:v `` | symétrie verticale |
|  |  | `` flip:h `` | symétrie horizontale |
|  |  | `` flip:d `` | symétrie selon la seconde diagonale |
|  |  | `` flip:vhd `` | symétrie selon la première diagonale |
|  |  | `` flip:dhv `` | idem (ordre indifférent) |
| <span style="color:green; font-family:monospace; font-weight:600">grow</span> | ajoute des entités et associations aléatoires (par défaut : 10 nouvelles associations) | `` grow arrange `` | ajouter des éléments avec les paramètres par défaut, puis réarranger |
|  |  | `` grow:n=10 `` | nombre total d'associations à ajouter (défaut) |
|  |  | `` grow:arity_1=2 `` | nombre d'associations réflexives (défaut) |
|  |  | `` grow:arity_3=2 `` | nombre d'associations ternaires (défaut) |
|  |  | `` grow:arity_4=0 `` | nombre d'associations quaternaires (défaut) |
|  |  | `` grow:doubles=1 `` | nombre d'associations liant deux mêmes entités (défaut) |
|  |  | `` grow:composite_ids=1 `` | nombre d'identifiants composites (défaut) |
|  |  | `` grow:ent_attrs=4 `` | nombre maximal d'attributs par entité (défaut) |
|  |  | `` grow:assoc_attrs=2 `` | nombre maximal d'attributs par association (défaut) |
|  |  | `` grow:'*1-*N'=3 `` | nombre d'associations `*1-*N` (défaut) |
|  |  | `` grow:'01-11'=1 `` | nombre d'associations `01-11` (défaut) |
|  |  | `` grow:'_11-*N'=1 `` | une entité faible (zéro par défaut) |
|  |  | `` grow:'/1N-*N'=1 `` | un agrégat (zéro par défaut) |
|  |  | `` grow:from_scratch arrange `` | à partir d'un MCD vide |
|  |  | `` grow:grow:n=9,from_scratch,ent_attrs=3 obfuscate:labels=en4 create:roles lower:roles arrange `` | créer un MCD d'entraînement à la conversion en relationnel |
| <span style="color:green; font-family:monospace; font-weight:600">guess</span> | cf. `create` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">hide</span> | cf. `delete` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">html</span> | convertit le modèle conceptuel en un schéma relationnel au format HTML | `` html `` | version de base |
|  |  | `` html:b `` | avec _boilerplate_ |
|  |  | `` html:c `` | avec contraintes d'unicité et d'optionalité |
|  |  | `` html:e `` | avec explications |
|  |  | `` html:bce `` | avec _boilerplate_, contraintes et explications |
| <span style="color:green; font-family:monospace; font-weight:600">infer</span> | cf. `create` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">insert</span> | cf. `create` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">interval</span> | cf. `slice` |  |  |
| <span title="Alias : tex." style="color:blue; font-family:monospace; font-weight:600">latex</span> | convertit le modèle conceptuel en un schéma relationnel au format LaTeX | `` latex `` | version de base |
|  |  | `` latex:b `` | avec _boilerplate_ |
|  |  | `` latex:c `` | avec contraintes d'unicité et d'optionalité |
|  |  | `` latex:e `` | avec explications |
|  |  | `` latex:bce `` | avec _boilerplate_, contraintes et explications |
| <span style="color:blue; font-family:monospace; font-weight:600">link</span> | cf. `share` |  |  |
| <span title="Alias : lowercase, lower_case." style="color:green; font-family:monospace; font-weight:600">lower</span> | réécrit les éléments donnés en minuscules | `` lower:attrs,roles `` | attributs et rôles en minuscules |
| <span style="color:green; font-family:monospace; font-weight:600">lower_case</span> | cf. `lower` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">lowercase</span> | cf. `lower` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">make</span> | cf. `create` |  |  |
| <span title="Alias : md, mld." style="color:blue; font-family:monospace; font-weight:600">markdown</span> | convertit le modèle conceptuel en un schéma relationnel au format Markdown | `` markdown `` | version de base |
|  |  | `` markdown:c `` | avec contraintes d'unicité et d'optionalité |
|  |  | `` markdown:e `` | avec explications |
|  |  | `` markdown:ce `` | avec contraintes et explications |
| <span style="color:blue; font-family:monospace; font-weight:600">md</span> | cf. `markdown` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">mirror</span> | cf. `flip` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">mld</span> | cf. `markdown` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">ms_sql</span> | cf. `mssql` |  |  |
| <span title="Alias : ms_sql, sql_server, sqlserver." style="color:blue; font-family:monospace; font-weight:600">mssql</span> | convertit le modèle conceptuel en un modèle physique pour Microsoft SQL Server | `` mssql `` | version de base |
|  |  | `` mssql:b `` | avec _boilerplate_ |
| <span style="color:blue; font-family:monospace; font-weight:600">mysql</span> | convertit le modèle conceptuel en un modèle physique pour MySQL | `` mysql `` | version de base |
|  |  | `` mysql:b `` | avec _boilerplate_ |
| <span style="color:green; font-family:monospace; font-weight:600">new</span> | cf. `create` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">obfuscate</span> | cf. `randomize` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">obscure</span> | cf. `randomize` |  |  |
| <span title="Alias : oracle_db." style="color:blue; font-family:monospace; font-weight:600">oracle</span> | convertit le modèle conceptuel en un modèle physique pour Oracle DB | `` oracle `` | version de base |
|  |  | `` oracle:b `` | avec _boilerplate_ |
| <span style="color:blue; font-family:monospace; font-weight:600">oracle_db</span> | cf. `oracle` |  |  |
| <span title="Alias : pascalcase, pascal_case." style="color:green; font-family:monospace; font-weight:600">pascal</span> | rewrite the given elements in PascalCase |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">pascal_case</span> | cf. `pascal` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">pascalcase</span> | cf. `pascal` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">postgres</span> | cf. `postgresql` |  |  |
| <span title="Alias : postgres." style="color:blue; font-family:monospace; font-weight:600">postgresql</span> | convertit le modèle conceptuel en un modèle physique pour PostgreSQL | `` postgresql `` | version de base |
|  |  | `` postgresql:b `` | avec _boilerplate_ |
| <span title="Alias : prepend." style="color:green; font-family:monospace; font-weight:600">prefix</span> | préfixe les éléments donnés avec la chaîne donnée | `` prefix:roles='-' `` | force les rôles à remplacer le nom des clés étrangères lors du passage au relationnel |
| <span style="color:green; font-family:monospace; font-weight:600">prepend</span> | cf. `prefix` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">qr</span> | cf. `share` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">qr_code</span> | cf. `share` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">rand</span> | cf. `randomize` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">random</span> | cf. `randomize` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">randomise</span> | cf. `randomize` |  |  |
| <span title="Alias : rand, random, randomise, obfuscate, obscure." style="color:green; font-family:monospace; font-weight:600">randomize</span> | garde la structure, mais randomise les éléments donnés quand c'est possible | `` obfuscate `` | libellés remplacés par du Lorem Ipsum |
|  |  | `` obfuscate:labels=lorem `` | idem |
|  |  | `` obfuscate:labels=disparition `` | idem, lexique du roman de Perec |
|  |  | `` obfuscate:labels=en4 `` | idem, mots anglais de 4 lettres (SFW) |
|  |  | `` obfuscate:attrs=fr,boxes=fr5 `` | idem, mots français de longueur quelconque pour les attributs, de 5 lettres pour les boîtes |
|  |  | `` randomize:types `` | types randomisés avec les fréquences de `default_datatypes_fr.tsv`. |
| <span style="color:green; font-family:monospace; font-weight:600">reflect</span> | cf. `flip` |  |  |
| <span title="Alias : template, relation_template." style="color:blue; font-family:monospace; font-weight:600">relation</span> | convertit le modèle conceptuel en schéma relationnel avec le gabarit donné | `` relation:path/to/my_template.yaml `` | chemin relatif, extension obligatoire |
| <span style="color:blue; font-family:monospace; font-weight:600">relation_template</span> | cf. `relation` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">remove</span> | cf. `delete` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">repl</span> | cf. `replace` |  |  |
| <span title="Alias : substitute, sub, repl." style="color:green; font-family:monospace; font-weight:600">replace</span> | réécrit les éléments donnés en appliquant le motif « recherche/remplacement » donné | `` replace:boxes='DIRIGER/RÉPONDRE DE' `` | renomme une boîte |
|  |  | `` replace:texts='personel/personnel' `` | corrige une faute d'orthographe |
|  |  | `` replace:replace:texts='_/ ' `` | remplace les tirets bas par des espaces |
|  |  | `` replace:types='VARCHAR/VARCHAR2' `` | modifie un nom de type |
|  |  | `` replace:cards=0N/1N `` | remplace toutes les cardinalités 0N par 1N |
|  |  | `` replace:cards=1N//1N `` | crée des agrégats un peu partout |
|  |  | `` replace:cards='0/X' replace:cards='11/X1' replace:cards='1N/XN' `` | masque les cardinalités minimales |
|  |  | `` delete:card_prefixes replace:cards=11/_11 `` | ajoute des marqueurs d'entités faibles |
| <span title="Alias : url, link, qr, qr_code." style="color:blue; font-family:monospace; font-weight:600">share</span> | encode le MCD dans une URL pour Mocodo online | `` qr --defer `` | génère un QR code via un service web |
| <span style="color:green; font-family:monospace; font-weight:600">shorten</span> | cf. `truncate` |  |  |
| <span title="Alias : cut, interval." style="color:green; font-family:monospace; font-weight:600">slice</span> | réécrit les éléments donnés en n'en gardant qu'une tranche donnée | `` slice:boxes=5:10 `` | de l'indice 5 (inclus) à l'indice 10 (exclu) |
|  |  | `` slice:boxes=5: `` | supprime les 5 premiers caractères |
|  |  | `` slice:boxes=:5 `` | ne garde que les 5 premiers caractères |
|  |  | `` slice:boxes=:-5 `` | supprime les 5 derniers caractères |
|  |  | `` slice:boxes=: `` | équivalent de `echo` |
|  |  | `` slice:boxes= `` | idem |
|  |  | `` slice:boxes `` | idem |
| <span title="Alias : snakecase, snake_case." style="color:green; font-family:monospace; font-weight:600">snake</span> | réécrit les éléments donnés en snake_case |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">snake_case</span> | cf. `snake` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">snakecase</span> | cf. `snake` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">split</span> | décompose toute association n-aire (*,1) en n-1 associations binaires | `` split arrange `` | décomposer, puis réarranger |
| <span title="Alias : ddl." style="color:blue; font-family:monospace; font-weight:600">sql</span> | convertit le modèle conceptuel en un modèle physique pour SQL |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">sql_server</span> | cf. `mssql` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">sqlite</span> | convertit le modèle conceptuel en un modèle physique pour SQLite | `` sqlite `` | version de base |
|  |  | `` sqlite:b `` | avec _boilerplate_ |
| <span style="color:blue; font-family:monospace; font-weight:600">sqlserver</span> | cf. `mssql` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">sub</span> | cf. `replace` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">substitute</span> | cf. `replace` |  |  |
| <span title="Alias : append." style="color:green; font-family:monospace; font-weight:600">suffix</span> | suffixe les éléments donnés avec la chaîne donnée | `` suffix:boxes=1 `` | Ajoute un suffixe numérique au nom des boîtes en vue de mettre un MCD et sa copie sur le même diagramme. |
| <span style="color:green; font-family:monospace; font-weight:600">suppress</span> | cf. `delete` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">swap_case</span> | cf. `swapcase` |  |  |
| <span title="Alias : swap_case." style="color:green; font-family:monospace; font-weight:600">swapcase</span> | réécrit les éléments donnés en inversant la casse de chaque lettre |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">template</span> | cf. `relation` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">tex</span> | cf. `latex` |  |  |
| <span title="Alias : txt." style="color:blue; font-family:monospace; font-weight:600">text</span> | convertit le modèle conceptuel en un schéma relationnel au format texte | `` text `` | version de base |
|  |  | `` text:c `` | avec contraintes d'unicité et d'optionalité |
|  |  | `` html:e `` | avec explications |
|  |  | `` html:ce `` | avec contraintes et explications |
| <span title="Alias : titlecase, title_case." style="color:green; font-family:monospace; font-weight:600">title</span> | réécrit les éléments donnés en mettant la première lettre de chaque mot en majuscule |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">title_case</span> | cf. `title` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">titlecase</span> | cf. `title` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">trunc</span> | cf. `truncate` |  |  |
| <span title="Alias : trunc, shorten." style="color:green; font-family:monospace; font-weight:600">truncate</span> | tronque les éléments donnés à la longueur donnée (par défaut : 64) | `` truncate:boxes=10 `` | tronque les noms des boîtes à 10 caractères |
| <span style="color:blue; font-family:monospace; font-weight:600">txt</span> | cf. `text` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">uml</span> | cf. `uml` |  |  |
| <span title="Alias : uppercase, upper_case." style="color:green; font-family:monospace; font-weight:600">upper</span> | réécrit les éléments donnés en majuscules | `` upper:boxes `` | noms des boîtes en majuscules |
| <span style="color:green; font-family:monospace; font-weight:600">upper_case</span> | cf. `upper` |  |  |
| <span style="color:green; font-family:monospace; font-weight:600">uppercase</span> | cf. `upper` |  |  |
| <span style="color:blue; font-family:monospace; font-weight:600">url</span> | cf. `share` |  |  |
