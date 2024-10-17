- **CLIENT** (<u>Réf. client</u>, Nom <sup>u1</sup>, Prénom <sup>u1</sup>, Adresse, Mail <sup>u2</sup>)
  - Le champ _Réf. client_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _CLIENT_.
  - Les champs _Nom_ et _Prénom_ étaient déjà de simples attributs de l'entité _CLIENT_. Il obéit à la contrainte d'unicité 1.
  - Le champ _Adresse_ était déjà un simple attribut de l'entité _CLIENT_.
  - Le champ _Mail_ était déjà un simple attribut de l'entité _CLIENT_. Il obéit à la contrainte d'unicité 2.

- **FOO** (<u>foo</u>, bar <sup>u1</sup>, biz <sup>u1 u2</sup>, buz <sup>u2</sup>, qux <sup>u3</sup>, quux <sup>u1 u2 u3</sup>)
  - Le champ _foo_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _FOO_.
  - Le champ _bar_ était déjà un simple attribut de l'entité _FOO_. Il obéit à la contrainte d'unicité 1.
  - Le champ _biz_ était déjà un simple attribut de l'entité _FOO_. Il obéit aux contraintes d'unicité 1 et 2.
  - Le champ _buz_ était déjà un simple attribut de l'entité _FOO_. Il obéit à la contrainte d'unicité 2.
  - Le champ _qux_ était déjà un simple attribut de l'entité _FOO_. Il obéit à la contrainte d'unicité 3.
  - Le champ _quux_ était déjà un simple attribut de l'entité _FOO_. Il obéit aux contraintes d'unicité 1, 2 et 3.

- **UTILISER** (<u>carnet</u> <sup>u1</sup>, <u>projet</u> <sup>u2</sup>, technicien <sup>u1 u2</sup>)
  - Le champ _carnet_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _UTILISER_. Il obéit en outre à la contrainte d'unicité 1.
  - Le champ _projet_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _UTILISER_. Il obéit en outre à la contrainte d'unicité 2.
  - Le champ _technicien_ était déjà un simple attribut de l'entité _UTILISER_. Il obéit aux contraintes d'unicité 1 et 2.
