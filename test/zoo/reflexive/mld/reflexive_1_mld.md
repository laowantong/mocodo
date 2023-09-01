- **COMPOSER** (<ins>pièce</ins>, <ins>pièce.1</ins>)
  - Les champs _pièce_ et _pièce.1_ constituent la clé primaire de la table. Leur table d'origine (_PIÈCE_) ayant été supprimée, ils ne sont pas considérés comme clés étrangères.

- **HOMME** (<ins>Num. SS</ins>, Nom, Prénom, _#Num. SS.1_)
  - Le champ _Num. SS_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _HOMME_.
  - Les champs _Nom_ et _Prénom_ étaient déjà de simples attributs de l'entité _HOMME_.
  - Le champ _Num. SS.1_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _ENGENDRER_ à partir de l'entité _HOMME_ en perdant son caractère identifiant.

----


**NB.** La table _PIÈCE_ a été supprimée car elle était réduite à la clé primaire de son entité d'origine.