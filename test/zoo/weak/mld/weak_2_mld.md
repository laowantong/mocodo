- **Appartement** (<u>_#code rue_</u>, <u>_#num immeuble_</u>, <u>_#num étage_</u>, <u>num appart.</u>, nb pièces)
  - Le champ _code rue_, _num immeuble_, _num étage_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Étage_ pour renforcer l'identifiant.
  - Le champ _num appart._ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _Appartement_.
  - Le champ _nb pièces_ était déjà un simple attribut de l'entité _Appartement_.

- **Étage** (<u>_#code rue_</u>, <u>_#num immeuble_</u>, <u>num étage</u>, nb appartements)
  - Le champ _code rue_, _num immeuble_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Immeuble_ pour renforcer l'identifiant.
  - Le champ _num étage_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _Étage_.
  - Le champ _nb appartements_ était déjà un simple attribut de l'entité _Étage_.

- **Immeuble** (<u>_#code rue_</u>, <u>num immeuble</u>, nb étages)
  - Le champ _code rue_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Rue_ pour renforcer l'identifiant.
  - Le champ _num immeuble_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _Immeuble_.
  - Le champ _nb étages_ était déjà un simple attribut de l'entité _Immeuble_.

- **Rue** (<u>code rue</u>, nom rue)
  - Le champ _code rue_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Rue_.
  - Le champ _nom rue_ était déjà un simple attribut de l'entité _Rue_.
