- **Appliquer** (<ins>_#employé_</ins>, <ins>_#projet_</ins>, <ins>_#compétence_</ins>)
  - Le champ _employé_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Employé_.
  - Le champ _projet_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Projet_.
  - Le champ _compétence_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Compétence_.

- **Compétence** (<ins>compétence</ins>, libellé)
  - Le champ _compétence_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Compétence_.
  - Le champ _libellé_ était déjà un simple attribut de l'entité _Compétence_.

- **Employé** (<ins>employé</ins>, nom)
  - Le champ _employé_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Employé_.
  - Le champ _nom_ était déjà un simple attribut de l'entité _Employé_.

- **Projet** (<ins>projet</ins>, date début, date fin)
  - Le champ _projet_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Projet_.
  - Les champs _date début_ et _date fin_ étaient déjà de simples attributs de l'entité _Projet_.
