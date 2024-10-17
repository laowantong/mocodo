- **Ligne de commande** (<u>commande</u>, <u>produit</u>, quantité)
  - Le champ _commande_ fait partie de la clé primaire de la table. Il a migré à partir de l'entité _Commande_ pour renforcer l'identifiant. Cependant, comme la table créée à partir de cette entité a été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _produit_ fait partie de la clé primaire de la table. Il a migré à partir de l'entité _Produit_ pour renforcer l'identifiant. Cependant, comme la table créée à partir de cette entité a été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _quantité_ était déjà un simple attribut de l'entité _Ligne de commande_.
<br>
----


**NB.** Les tables _Commande_ et _Produit_ ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine. Pour conserver de telles tables, préfixez d'un « + » la définition des entités d'origine.
