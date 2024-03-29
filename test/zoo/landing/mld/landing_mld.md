- **AYANT-DROIT** (<ins>_#matricule_</ins>, <ins>nom ayant-droit</ins>, lien)
  - Le champ _matricule_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _EMPLOYÉ_ pour renforcer l'identifiant.
  - Le champ _nom ayant-droit_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _AYANT-DROIT_.
  - Le champ _lien_ était déjà un simple attribut de l'entité _AYANT-DROIT_.

- **COMPOSER** (<ins>_#réf. pièce composée_</ins>, <ins>_#réf. pièce composante_</ins>, quantité)
  - Les champs _réf. pièce composée_ et _réf. pièce composante_ constituent la clé primaire de la table. Ce sont des clés étrangères qui ont migré directement à partir de l'entité _PIÈCE_.
  - Le champ _quantité_ était déjà un simple attribut de l'association _COMPOSER_.

- **DÉPARTEMENT** (<ins>num. département</ins>, nom département)
  - Le champ _num. département_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _DÉPARTEMENT_.
  - Le champ _nom département_ était déjà un simple attribut de l'entité _DÉPARTEMENT_.

- **EMPLOYÉ** (<ins>matricule</ins>, nom employé, _#num. département!_)
  - Le champ _matricule_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _EMPLOYÉ_.
  - Le champ _nom employé_ était déjà un simple attribut de l'entité _EMPLOYÉ_.
  - Le champ à saisie obligatoire _num. département_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _EMPLOYER_ à partir de l'entité _DÉPARTEMENT_ en perdant son caractère identifiant.

- **FOURNIR** (<ins>_#num. projet_</ins>, <ins>_#réf. pièce_</ins>, <ins>_#num. société_</ins>, qté fournie)
  - Le champ _num. projet_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _PROJET_.
  - Le champ _réf. pièce_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _PIÈCE_.
  - Le champ _num. société_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _SOCIÉTÉ_.
  - Le champ _qté fournie_ était déjà un simple attribut de l'association _FOURNIR_.

- **PIÈCE** (<ins>réf. pièce</ins>, libellé pièce)
  - Le champ _réf. pièce_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _PIÈCE_.
  - Le champ _libellé pièce_ était déjà un simple attribut de l'entité _PIÈCE_.

- **PROJET** (<ins>num. projet</ins>, nom projet, _#matricule responsable?_)
  - Le champ _num. projet_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _PROJET_.
  - Le champ _nom projet_ était déjà un simple attribut de l'entité _PROJET_.
  - Le champ à saisie facultative _matricule responsable_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _DIRIGER_ à partir de l'entité _EMPLOYÉ_ en perdant son caractère identifiant.

- **REQUÉRIR** (<ins>_#num. projet_</ins>, <ins>_#réf. pièce_</ins>, qté requise)
  - Le champ _num. projet_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _PROJET_.
  - Le champ _réf. pièce_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _PIÈCE_.
  - Le champ _qté requise_ était déjà un simple attribut de l'association _REQUÉRIR_.

- **SOCIÉTÉ** (<ins>num. société</ins>, raison sociale, _#num. société mère?_)
  - Le champ _num. société_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _SOCIÉTÉ_.
  - Le champ _raison sociale_ était déjà un simple attribut de l'entité _SOCIÉTÉ_.
  - Le champ à saisie facultative _num. société mère_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _CONTRÔLER_ à partir de l'entité _SOCIÉTÉ_ en perdant son caractère identifiant.

- **TRAVAILLER** (<ins>_#matricule_</ins>, <ins>_#num. projet_</ins>)
  - Le champ _matricule_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _EMPLOYÉ_.
  - Le champ _num. projet_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _PROJET_.
