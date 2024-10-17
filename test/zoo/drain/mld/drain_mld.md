- **Entreprise** (<u>nom entreprise</u>, adresse, téléphone)
  - Le champ _nom entreprise_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Entreprise_.
  - Les champs _adresse_ et _téléphone_ étaient déjà de simples attributs de l'entité _Entreprise_.

- **Étudiant** (<u>num étudiant</u>, nom, _#num. stage_ <sup>u1</sup>, date signature, date?, note stage)
  - Le champ _num étudiant_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Étudiant_.
  - Le champ _nom_ était déjà un simple attribut de l'entité _Étudiant_.
  - Le champ _num. stage_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _Attribuer_ à partir de l'entité _Stage_ en perdant son caractère identifiant. Il obéit en outre à la contrainte d'unicité 1.
  - Le champ _date signature_ a migré à partir de l'association de dépendance fonctionnelle _Attribuer_.
  - Le champ à saisie facultative _date_ est un simple attribut. Il a migré par l'association de dépendance fonctionnelle _Soutenir_ à partir de l'entité _Date_ en perdant son caractère identifiant. Cependant, comme la table créée à partir de cette entité a été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _note stage_ a migré à partir de l'association de dépendance fonctionnelle _Soutenir_.

- **Stage** (<u>num. stage</u>, sujet, _#nom entreprise!_, date proposition)
  - Le champ _num. stage_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Stage_.
  - Le champ _sujet_ était déjà un simple attribut de l'entité _Stage_.
  - Le champ à saisie obligatoire _nom entreprise_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _Proposer_ à partir de l'entité _Entreprise_ en perdant son caractère identifiant.
  - Le champ _date proposition_ a migré à partir de l'association de dépendance fonctionnelle _Proposer_.
<br>
----


**NB.** La table _Date_ a été supprimée car elle était réduite à la clé primaire de son entité d'origine. Pour conserver de telles tables, préfixez d'un « + » la définition des entités d'origine.
