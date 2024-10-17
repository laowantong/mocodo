- **CONTRAT** (<u>_#num prof_</u>, <u>date contrat</u>, salaire horaire contrat)
  - Le champ _num prof_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _VACATAIRE_ pour renforcer l'identifiant.
  - Le champ _date contrat_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _CONTRAT_.
  - Le champ _salaire horaire contrat_ était déjà un simple attribut de l'entité _CONTRAT_.

- **SALARIÉ** (<u>num prof</u>, nom prof, prénom prof, téléphone prof, date embauche salarié, échelon salarié, salaire salarié)
  - Le champ _num prof_ constitue la clé primaire de la table. Il était clé primaire de l'entité-mère _PROFESSEUR_ (supprimée).
  - Le champ _nom prof_ est un simple attribut. Il était simple attribut de l'entité-mère _PROFESSEUR_ (supprimée).
  - Le champ _prénom prof_ est un simple attribut. Il était simple attribut de l'entité-mère _PROFESSEUR_ (supprimée).
  - Le champ _téléphone prof_ est un simple attribut. Il était simple attribut de l'entité-mère _PROFESSEUR_ (supprimée).
  - Les champs _date embauche salarié_, _échelon salarié_ et _salaire salarié_ étaient déjà de simples attributs de l'entité _SALARIÉ_.

- **VACATAIRE** (<u>num prof</u>, nom prof, prénom prof, téléphone prof, statut vacataire)
  - Le champ _num prof_ constitue la clé primaire de la table. Il était clé primaire de l'entité-mère _PROFESSEUR_ (supprimée).
  - Le champ _nom prof_ est un simple attribut. Il était simple attribut de l'entité-mère _PROFESSEUR_ (supprimée).
  - Le champ _prénom prof_ est un simple attribut. Il était simple attribut de l'entité-mère _PROFESSEUR_ (supprimée).
  - Le champ _téléphone prof_ est un simple attribut. Il était simple attribut de l'entité-mère _PROFESSEUR_ (supprimée).
  - Le champ _statut vacataire_ était déjà un simple attribut de l'entité _VACATAIRE_.
