- **ANIMAL** (<ins>_#code espèce_</ins>, <ins>nom</ins>, <ins>date naissance</ins>, sexe, date décès, _#code espèce mère_, _#nom mère_, _#date naissance mère_, type alimentation, CARNIVORE, quantité viande, HERBIVORE, plante préférée)
  - Le champ _code espèce_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _ESPÈCE_.
  - Les champs _nom_ et _date naissance_ font partie de la clé primaire de la table. C'étaient déjà des identifiants de l'entité _ANIMAL_.
  - Les champs _sexe_ et _date décès_ étaient déjà de simples attributs de l'entité _ANIMAL_.
  - Le champ _code espèce mère_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _A MÈRE_ à partir de l'entité _ANIMAL_ en perdant son caractère identifiant.
  - Le champ _nom mère_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _A MÈRE_ à partir de l'entité _ANIMAL_ en perdant son caractère identifiant.
  - Le champ _date naissance mère_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _A MÈRE_ à partir de l'entité _ANIMAL_ en perdant son caractère identifiant.
  - Un champ entier _type alimentation_ est ajouté pour indiquer la nature de la spécialisation. Il est interprété comme un code binaire : bit 1 pour la première entité-fille, bit 2 pour la deuxième, etc. Peut être vide, du fait de l'absence de contrainte de totalité.
  - Un champ booléen _CARNIVORE_ est ajouté pour indiquer si on a affaire ou pas à la spécialisation de même nom.
  - Le champ _quantité viande_ a migré à partir de l'entité-fille _CARNIVORE_ (supprimée).
  - Un champ booléen _HERBIVORE_ est ajouté pour indiquer si on a affaire ou pas à la spécialisation de même nom.
  - Le champ _plante préférée_ a migré à partir de l'entité-fille _HERBIVORE_ (supprimée).

- **ESPÈCE** (<ins>code espèce</ins>, nom latin <sup>u1</sup>, nom vernaculaire)
  - Le champ _code espèce_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _ESPÈCE_.
  - Le champ _nom latin_ était déjà un simple attribut de l'entité _ESPÈCE_. Il constitue une clé alternative matérialisée par la contrainte d'unicité 1.
  - Le champ _nom vernaculaire_ était déjà un simple attribut de l'entité _ESPÈCE_.

- **OCCUPE** (<ins>_#code espèce_</ins>, <ins>_#nom_</ins>, <ins>_#date naissance_</ins>, <ins>num. enclos</ins>, date début, date fin)
  - Les champs _code espèce_, _nom_ et _date naissance_ font partie de la clé primaire de la table. Ce sont des clés étrangères qui ont migré directement à partir de l'entité _ANIMAL_.
  - Le champ _num. enclos_ fait partie de la clé primaire de la table. Sa table d'origine (_ENCLOS_) ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _date début_ a migré par l'association de dépendance fonctionnelle _OCCUPE_ à partir de l'entité _PÉRIODE_ en perdant son caractère identifiant. De plus, comme la table créée à partir de cette entité a été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _date fin_ a migré par l'association de dépendance fonctionnelle _OCCUPE_ à partir de l'entité _PÉRIODE_ en perdant son caractère identifiant. De plus, comme la table créée à partir de cette entité a été supprimée, il n'est pas considéré comme clé étrangère.

- **PEUT COHABITER AVEC** (<ins>_#code espèce_</ins>, <ins>_#code espèce commensale_</ins>, nb. max. commensaux)
  - Les champs _code espèce_ et _code espèce commensale_ constituent la clé primaire de la table. Ce sont des clés étrangères qui ont migré directement à partir de l'entité _ESPÈCE_.
  - Le champ _nb. max. commensaux_ était déjà un simple attribut de l'association _PEUT COHABITER AVEC_.

- **PEUT VIVRE DANS** (<ins>_#code espèce_</ins>, <ins>num. enclos</ins>, nb. max. congénères)
  - Le champ _code espèce_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _ESPÈCE_.
  - Le champ _num. enclos_ fait partie de la clé primaire de la table. Sa table d'origine (_ENCLOS_) ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _nb. max. congénères_ était déjà un simple attribut de l'association _PEUT VIVRE DANS_.

----


**NB.** Les tables _ENCLOS_ et _PÉRIODE_ ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine.
