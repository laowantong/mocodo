- **CONTRAT** (<ins>_#num prof_</ins>, <ins>date contrat</ins>, salaire horaire contrat)
  - Le champ _num prof_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _VACATAIRE_ pour renforcer l'identifiant.
  - Le champ _date contrat_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _CONTRAT_.
  - Le champ _salaire horaire contrat_ était déjà un simple attribut de l'entité _CONTRAT_.

- **PROFESSEUR** (<ins>num prof</ins>, nom prof, prénom prof, téléphone prof)
  - Le champ _num prof_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _PROFESSEUR_.
  - Les champs _nom prof_, _prénom prof_ et _téléphone prof_ étaient déjà de simples attributs de l'entité _PROFESSEUR_.

- **SALARIÉ** (<ins>_#num prof_</ins>, date embauche salarié, échelon salarié, salaire salarié)
  - Le champ _num prof_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité-mère _PROFESSEUR_.
  - Les champs _date embauche salarié_, _échelon salarié_ et _salaire salarié_ étaient déjà de simples attributs de l'entité _SALARIÉ_.

- **VACATAIRE** (<ins>_#num prof_</ins>, statut vacataire)
  - Le champ _num prof_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité-mère _PROFESSEUR_.
  - Le champ _statut vacataire_ était déjà un simple attribut de l'entité _VACATAIRE_.
