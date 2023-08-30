----

# 1

```
client: ref_client [VARCHAR(8)], nom [VARCHAR(255)], prenom [VARCHAR(255)], adresse []
passer, 0N client, 11 commande
commande: num_commande [VARCHAR(8)], date [DATE], montant [DECIMAL(10,2)]
inclure, 1N commande, 0N produit: quantite [INTEGER]
produit: ref_produit [VARCHAR(8)], libelle [VARCHAR(50)], prix_unitaire [DECIMAL(10,2)]
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE client (
  ref_client VARCHAR(8),
  nom VARCHAR(255),
  prenom VARCHAR(255),
  adresse VARCHAR(42),
  PRIMARY KEY (ref_client)
);

CREATE TABLE commande (
  num_commande VARCHAR(8),
  date DATE,
  montant DECIMAL(10,2),
  ref_client VARCHAR(8),
  PRIMARY KEY (num_commande)
);

CREATE TABLE inclure (
  num_commande VARCHAR(8),
  ref_produit VARCHAR(8),
  quantite INTEGER,
  PRIMARY KEY (num_commande, ref_produit)
);

CREATE TABLE produit (
  ref_produit VARCHAR(8),
  libelle VARCHAR(50),
  prix_unitaire DECIMAL(10,2),
  PRIMARY KEY (ref_produit)
);

ALTER TABLE commande ADD FOREIGN KEY (ref_client) REFERENCES client (ref_client);
ALTER TABLE inclure ADD FOREIGN KEY (ref_produit) REFERENCES produit (ref_produit);
ALTER TABLE inclure ADD FOREIGN KEY (num_commande) REFERENCES commande (num_commande);
```

----

# 2

```
homme: num_ss [VARCHAR(8)], nom [VARCHAR(255)], prenom [VARCHAR(255)]
engendrer, 0N homme, 11 homme
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE homme (
  num_ss VARCHAR(8),
  nom VARCHAR(255),
  prenom VARCHAR(255),
  num_ss_1 VARCHAR(8),
  PRIMARY KEY (num_ss)
);

ALTER TABLE homme ADD FOREIGN KEY (num_ss_1) REFERENCES homme (num_ss);
```

----

# 3

```
gratte_ciel: latitude [DECIMAL(9,6)], _longitude [DECIMAL(9,6)], nom [VARCHAR(255)], hauteur [DECIMAL(10,2)], annee_de_construction []
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE gratte_ciel (
  latitude DECIMAL(9,6),
  longitude DECIMAL(9,6),
  nom VARCHAR(255),
  hauteur DECIMAL(10,2),
  annee_de_construction VARCHAR(42),
  PRIMARY KEY (latitude, longitude)
);
```

----

# 4

```
oeuvre: cote_oeuvre [], titre [], date_parution [DATE]
df, 1N oeuvre, _11 exemplaire
exemplaire: num_exemplaire [VARCHAR(8)], etat_du_livre [], date_d_achat [DATE]
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE exemplaire (
  cote_oeuvre VARCHAR(42),
  num_exemplaire VARCHAR(8),
  etat_du_livre VARCHAR(42),
  date_d_achat DATE,
  PRIMARY KEY (cote_oeuvre, num_exemplaire)
);

CREATE TABLE oeuvre (
  cote_oeuvre VARCHAR(42),
  titre VARCHAR(42),
  date_parution DATE,
  PRIMARY KEY (cote_oeuvre)
);

ALTER TABLE exemplaire ADD FOREIGN KEY (cote_oeuvre) REFERENCES oeuvre (cote_oeuvre);
```

----

# 5

```
date: date [DATE]
reserver1, /1N client1, 1N chambre1, 0N date: duree []
chambre1: numero [], prix [DECIMAL(10,2)]
client1: id_client [VARCHAR(8)]
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE chambre1 (
  numero VARCHAR(42),
  prix DECIMAL(10,2),
  PRIMARY KEY (numero)
);

CREATE TABLE reserver1 (
  numero VARCHAR(42),
  date DATE,
  id_client VARCHAR(8),
  duree VARCHAR(42),
  PRIMARY KEY (numero, date)
);

ALTER TABLE reserver1 ADD FOREIGN KEY (numero) REFERENCES chambre1 (numero);
```

----

# 6

```
date2: date [DATE]
df1, 0N date2, _11 reserver2
reserver2: _duree []
df2, 0N chambre2, _11 reserver2
chambre2: numero [], prix [DECIMAL(10,2)]
df3, 11 reserver2, 1N client2
client2: id_client [VARCHAR(8)]
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE chambre2 (
  numero VARCHAR(42),
  prix DECIMAL(10,2),
  PRIMARY KEY (numero)
);

CREATE TABLE reserver2 (
  numero VARCHAR(42),
  date DATE,
  duree VARCHAR(42),
  id_client VARCHAR(8),
  PRIMARY KEY (numero, date)
);

ALTER TABLE reserver2 ADD FOREIGN KEY (numero) REFERENCES chambre2 (numero);
```

----

# 7

```
lacus1: blandit [], elit []
+ligula1, 01 lacus1, 1N eros1: metus []
eros1: congue [], nibh [], tincidunt []
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE eros1 (
  congue VARCHAR(42),
  nibh VARCHAR(42),
  tincidunt VARCHAR(42),
  PRIMARY KEY (congue)
);

CREATE TABLE lacus1 (
  blandit VARCHAR(42),
  elit VARCHAR(42),
  PRIMARY KEY (blandit)
);

CREATE TABLE ligula1 (
  blandit VARCHAR(42),
  congue VARCHAR(42),
  metus VARCHAR(42),
  PRIMARY KEY (blandit)
);

ALTER TABLE ligula1 ADD FOREIGN KEY (congue) REFERENCES eros1 (congue);
ALTER TABLE ligula1 ADD FOREIGN KEY (blandit) REFERENCES lacus1 (blandit);
```

----

# 8

```
personne: num_ss [VARCHAR(8)], nom [VARCHAR(255)], prenom [VARCHAR(255)]
/XT\ personne <- homme1, femme: sexe [CHAR(1)]
homme1: 
femme: nom_de_jeune_fille [VARCHAR(255)]
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE personne (
  num_ss VARCHAR(8),
  nom VARCHAR(255),
  prenom VARCHAR(255),
  sexe CHAR(1),
  nom_de_jeune_fille VARCHAR(255),
  PRIMARY KEY (num_ss)
);
```

----

# 9

```
client3: ref_client [VARCHAR(8)], 1_nom [VARCHAR(255)], 1_prenom [VARCHAR(255)], adresse [], 2_mail [VARCHAR(255)]
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE client3 (
  ref_client VARCHAR(8),
  nom VARCHAR(255),
  prenom VARCHAR(255),
  adresse VARCHAR(42),
  mail VARCHAR(255),
  PRIMARY KEY (ref_client)
);

ALTER TABLE client3 ADD CONSTRAINT client3_u1 UNIQUE (nom, prenom);
ALTER TABLE client3 ADD CONSTRAINT client3_u2 UNIQUE (mail);
```

----

# 10

```
foo: foo [], 1_bar [], 12_biz [], 2_buz [], 3_qux [], 123_quux []
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE foo (
  foo VARCHAR(42),
  bar VARCHAR(42),
  biz VARCHAR(42),
  buz VARCHAR(42),
  qux VARCHAR(42),
  quux VARCHAR(42),
  PRIMARY KEY (foo)
);

ALTER TABLE foo ADD CONSTRAINT foo_u1 UNIQUE (bar, biz, quux);
ALTER TABLE foo ADD CONSTRAINT foo_u2 UNIQUE (biz, buz, quux);
ALTER TABLE foo ADD CONSTRAINT foo_u3 UNIQUE (qux, quux);
```

----

# 11

```
lacus: blandit [], elit []
ligula, 11 lacus, 1N eros, 0N tellus: metus []
eros: congue [], nibh [], tincidunt []  

bidendum, 0N tellus, 11 tellus: consequat []
tellus: integer [], odio []
faucibus, 11 tellus, 01 eros: ipsum []
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE eros (
  congue VARCHAR(42),
  nibh VARCHAR(42),
  tincidunt VARCHAR(42),
  PRIMARY KEY (congue)
);

CREATE TABLE lacus (
  blandit VARCHAR(42),
  elit VARCHAR(42),
  congue VARCHAR(42),
  integer VARCHAR(42),
  metus VARCHAR(42),
  PRIMARY KEY (blandit)
);

CREATE TABLE tellus (
  integer VARCHAR(42),
  odio VARCHAR(42),
  integer_1 VARCHAR(42),
  consequat VARCHAR(42),
  congue VARCHAR(42),
  ipsum VARCHAR(42),
  PRIMARY KEY (integer)
);

ALTER TABLE lacus ADD FOREIGN KEY (integer) REFERENCES tellus (integer);
ALTER TABLE lacus ADD FOREIGN KEY (congue) REFERENCES eros (congue);
ALTER TABLE tellus ADD FOREIGN KEY (congue) REFERENCES eros (congue);
ALTER TABLE tellus ADD FOREIGN KEY (integer_1) REFERENCES tellus (integer);
```

----

# 12

```
appartement: num_appart [VARCHAR(8)], nb_pieces [INTEGER]
composer, 0N etage, _11 appartement
etage: num_etage [VARCHAR(8)], nb_appartements [INTEGER]
appartenir, 1N immeuble, _11 etage
immeuble: num_immeuble [VARCHAR(8)], nb_etages [INTEGER]
se_situer, 0N rue, _11 immeuble
rue: code_rue [VARCHAR(8)], nom_rue [VARCHAR(255)]
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE appartement (
  code_rue VARCHAR(8),
  num_immeuble VARCHAR(8),
  num_etage VARCHAR(8),
  num_appart VARCHAR(8),
  nb_pieces INTEGER,
  PRIMARY KEY (code_rue, num_immeuble, num_etage, num_appart)
);

CREATE TABLE etage (
  code_rue VARCHAR(8),
  num_immeuble VARCHAR(8),
  num_etage VARCHAR(8),
  nb_appartements INTEGER,
  PRIMARY KEY (code_rue, num_immeuble, num_etage)
);

CREATE TABLE immeuble (
  code_rue VARCHAR(8),
  num_immeuble VARCHAR(8),
  nb_etages INTEGER,
  PRIMARY KEY (code_rue, num_immeuble)
);

CREATE TABLE rue (
  code_rue VARCHAR(8),
  nom_rue VARCHAR(255),
  PRIMARY KEY (code_rue)
);

ALTER TABLE appartement ADD FOREIGN KEY (code_rue, num_immeuble, num_etage) REFERENCES etage (code_rue, num_immeuble, num_etage);
ALTER TABLE etage ADD FOREIGN KEY (code_rue, num_immeuble) REFERENCES immeuble (code_rue, num_immeuble);
ALTER TABLE immeuble ADD FOREIGN KEY (code_rue) REFERENCES rue (code_rue);
```

----

# 13

```
soutenir, 01 etudiant, 0N [soutenance] date1: note_stage [TEXT]
etudiant: num_etudiant [VARCHAR(8)], nom [VARCHAR(255)], coordonnees []
date1: date [DATE]
repondre_de, 0N [visite] date1, 11 etudiant, 0N [responsable] enseignant
enseignant: num_enseignant [VARCHAR(8)], nom [VARCHAR(255)], coordonnees []
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE enseignant (
  num_enseignant VARCHAR(8),
  nom VARCHAR(255),
  coordonnees VARCHAR(42),
  PRIMARY KEY (num_enseignant)
);

CREATE TABLE etudiant (
  num_etudiant VARCHAR(8),
  nom VARCHAR(255),
  coordonnees VARCHAR(42),
  date_soutenance DATE,
  note_stage TEXT,
  date_visite DATE,
  num_enseignant_responsable VARCHAR(8),
  PRIMARY KEY (num_etudiant)
);

ALTER TABLE etudiant ADD FOREIGN KEY (num_enseignant_responsable) REFERENCES enseignant (num_enseignant);
```

----

# 14

```
client4: ref_client [VARCHAR(8)], nom [VARCHAR(255)], prenom [VARCHAR(255)], adresse []
passer1, 0N [ayant_commande] client4, 11 [note_ignoree] commande1
commande1: num_commande [VARCHAR(8)], date [DATE], montant [DECIMAL(10,2)]
inclure1, 1N [passee] commande1, 0N [commande] produit1: quantite [INTEGER]
produit1: ref_produit [VARCHAR(8)], libelle [VARCHAR(50)], prix_unitaire [DECIMAL(10,2)]
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE client4 (
  ref_client VARCHAR(8),
  nom VARCHAR(255),
  prenom VARCHAR(255),
  adresse VARCHAR(42),
  PRIMARY KEY (ref_client)
);

CREATE TABLE commande1 (
  num_commande VARCHAR(8),
  date DATE,
  montant DECIMAL(10,2),
  ref_client_ayant_commande VARCHAR(8),
  PRIMARY KEY (num_commande)
);

CREATE TABLE inclure1 (
  num_commande_passee VARCHAR(8),
  ref_produit_commande VARCHAR(8),
  quantite INTEGER,
  PRIMARY KEY (num_commande_passee, ref_produit_commande)
);

CREATE TABLE produit1 (
  ref_produit VARCHAR(8),
  libelle VARCHAR(50),
  prix_unitaire DECIMAL(10,2),
  PRIMARY KEY (ref_produit)
);

ALTER TABLE commande1 ADD FOREIGN KEY (ref_client_ayant_commande) REFERENCES client4 (ref_client);
ALTER TABLE inclure1 ADD FOREIGN KEY (ref_produit_commande) REFERENCES produit1 (ref_produit);
ALTER TABLE inclure1 ADD FOREIGN KEY (num_commande_passee) REFERENCES commande1 (num_commande);
```

----

# 15

```
ingenieur: ingenieur []
gerer, /1N responsable, 1N ingenieur, 1N projet
projet: projet []
responsable: responsable []
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE gerer (
  ingenieur VARCHAR(42),
  projet VARCHAR(42),
  responsable VARCHAR(42),
  PRIMARY KEY (ingenieur, projet)
);
```

----

# 16

```
projet3: projet []
affecter, /1N site, /1N projet3, 0N employe1
site: site []
employe1: employe []
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE affecter (
  projet VARCHAR(42),
  employe VARCHAR(42),
  site VARCHAR(42),
  PRIMARY KEY (projet, employe)
);

ALTER TABLE affecter ADD CONSTRAINT affecter_u1 UNIQUE (employe, site);
```

----

# 17

```
employe: employe []
df4, 1N employe, 11 affecter1
affecter1:
df5, _11 affecter1, 1N site1
site1: site []
projet1: projet []
df6, _11 affecter1, 1N projet1
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE affecter1 (
  projet VARCHAR(42),
  site VARCHAR(42),
  employe VARCHAR(42),
  PRIMARY KEY (projet, site)
);
```

----

# 18

```
technicien: technicien []
projet2: projet []
utiliser, /1N technicien, /1N carnet, /1N projet2
carnet: carnet []
```

```sql
CREATE DATABASE Untitled;
\c Untitled;

CREATE TABLE utiliser (
  carnet VARCHAR(42),
  projet VARCHAR(42),
  technicien VARCHAR(42),
  PRIMARY KEY (carnet, projet)
);

ALTER TABLE utiliser ADD CONSTRAINT utiliser_u1 UNIQUE (carnet, technicien);
ALTER TABLE utiliser ADD CONSTRAINT utiliser_u2 UNIQUE (projet, technicien);
```
