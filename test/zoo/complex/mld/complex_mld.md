- **ANIMAL** (<u>_#code espèce_</u>, <u>nom</u>, <u>date naissance</u>, sexe, date décès, _#code espèce mère?_, _#nom mère?_, _#date naissance mère?_, type alimentation?, est carnivore!, quantité viande?, est herbivore!, plante préférée?)
  - Le champ _code espèce_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _ESPÈCE_ pour renforcer l'identifiant.
  - Les champs _nom_ et _date naissance_ font partie de la clé primaire de la table. C'étaient déjà des identifiants de l'entité _ANIMAL_.
  - Les champs _sexe_ et _date décès_ étaient déjà de simples attributs de l'entité _ANIMAL_.
  - Les champs à saisie facultative _code espèce mère_, _nom mère_ et _date naissance mère_ sont des clés étrangères. Ils ont migré par l'association de dépendance fonctionnelle _A MÈRE_ à partir de l'entité _ANIMAL_ en perdant leur caractère identifiant.
  - Un discriminateur à saisie facultative _type alimentation_ est ajouté pour indiquer la nature de la spécialisation. Peut être vide, du fait de l'absence de contrainte de totalité.
  - Un champ booléen à saisie obligatoire _est carnivore_ est ajouté pour indiquer si on a affaire ou pas à la spécialisation de même nom.
  - Le champ à saisie facultative _quantité viande_ a migré à partir de l'entité-fille _CARNIVORE_ (supprimée).
  - Un champ booléen à saisie obligatoire _est herbivore_ est ajouté pour indiquer si on a affaire ou pas à la spécialisation de même nom.
  - Le champ à saisie facultative _plante préférée_ a migré à partir de l'entité-fille _HERBIVORE_ (supprimée).

- **ESPÈCE** (<u>code espèce</u>, nom latin <sup>u1</sup>, nom vernaculaire)
  - Le champ _code espèce_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _ESPÈCE_.
  - Le champ _nom latin_ était déjà un simple attribut de l'entité _ESPÈCE_. Il obéit à la contrainte d'unicité 1.
  - Le champ _nom vernaculaire_ était déjà un simple attribut de l'entité _ESPÈCE_.

- **OCCUPE** (<u>_#code espèce_</u>, <u>_#nom_</u>, <u>_#date naissance_</u>, <u>num. enclos</u>, date début!, date fin!)
  - Les champs _code espèce_, _nom_ et _date naissance_ font partie de la clé primaire de la table. Ce sont des clés étrangères qui ont migré directement à partir de l'entité _ANIMAL_.
  - Le champ _num. enclos_ fait partie de la clé primaire de la table. Sa table d'origine (_ENCLOS_) ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Les champs à saisie obligatoire _date début_ et _date fin_ sont de simples attributs. Ils ont migré directement à partir de l'entité _PÉRIODE_ en perdant leur caractère identifiant. Cependant, comme la table créée à partir de cette entité a été supprimée, ils ne sont pas considérés comme clés étrangères.

- **PEUT COHABITER AVEC** (<u>_#code espèce_</u>, <u>_#code espèce commensale_</u>, nb. max. commensaux)
  - Les champs _code espèce_ et _code espèce commensale_ constituent la clé primaire de la table. Ce sont des clés étrangères qui ont migré directement à partir de l'entité _ESPÈCE_.
  - Le champ _nb. max. commensaux_ était déjà un simple attribut de l'association _PEUT COHABITER AVEC_.

- **PEUT VIVRE DANS** (<u>_#code espèce_</u>, <u>num. enclos</u>, nb. max. congénères)
  - Le champ _code espèce_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _ESPÈCE_.
  - Le champ _num. enclos_ fait partie de la clé primaire de la table. Sa table d'origine (_ENCLOS_) ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _nb. max. congénères_ était déjà un simple attribut de l'association _PEUT VIVRE DANS_.
<br>
----


**NB.** Les tables _ENCLOS_ et _PÉRIODE_ ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine. Pour conserver de telles tables, préfixez d'un « + » la définition des entités d'origine.
