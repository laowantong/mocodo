#!/usr/bin/python
# encoding: utf-8

import unittest
from tables import *
from mcd import Mcd


class TablesTest(unittest.TestCase):
	
	def testGeneralCase(self):
		clauses = """
		LOREM: -ipsum, dolor, sit
		AMET, 11 LOREM, 01 CONSECTETUER: adipiscing
		CONSECTETUER: elit, sed
		NON, 11 RISUS, 0N RISUS

		DF, 11 LOREM, 1N SUSPENDISSE
		SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
		TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
		RISUS: ultricies, _cras, elementum

		SUSPENDISSE: diam
		MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
		DIGNISSIM: ligula, massa, varius
		SEMPER, 0N RISUS, 1N DIGNISSIM
		"""
		t = Tables(Mcd(clauses.split("\n"),{"df": u"DF","sep": u","}))
		expected = {
			'CONSECTETUER': {'name': 'CONSECTETUER',
				'columns': [
					{'attribute':'elit', 'attributeType': None, 'primary': True, 'foreign': False},
					{'attribute':'sed', 'attributeType': None, 'primary': False, 'foreign': False},
				],
			},
			'DIGNISSIM': {'name': 'DIGNISSIM',
				'columns': [
					{'attribute':'ligula', 'attributeType': None, 'primary': True, 'foreign': False},
					{'attribute':'massa', 'attributeType': None, 'primary': False, 'foreign': False},
					{'attribute':'varius', 'attributeType': None, 'primary': False, 'foreign': False},
				],
			},
			'LOREM': { 'name': 'LOREM',
				'columns': [
					{'attribute':'ipsum', 'attributeType': None, 'primary': True, 'foreign': False},
					{'attribute':'dolor', 'attributeType': None, 'primary': False, 'foreign': False},
					{'attribute':'sit', 'attributeType': None, 'primary': False, 'foreign': False},
				],
			},
			'RISUS': { 'name': 'RISUS',
				'columns': [
					{'attribute':'ultricies', 'attributeType': None, 'primary': True, 'foreign': False},
					{'attribute':'cras', 'attributeType': None, 'primary': True, 'foreign': False},
					{'attribute':'elementum', 'attributeType': None, 'primary': False, 'foreign': False},
				],
			},
			'SUSPENDISSE': {'name': 'SUSPENDISSE',
				'columns': [
					{'attribute':'diam', 'attributeType': None, 'primary': True, 'foreign': False},
				],
			}
		}
		t.tablesFromEntities()
		self.assertEqual(t.tables,expected)
		expected.update({
			'LOREM': { 'name': 'LOREM',
				'columns': [
					{'format':'strengthen', 'attribute':'diam', 'attributeType': None, 'association': 'DF','entity': 'SUSPENDISSE', 'primary': True, 'foreign': True},
					{'attribute':'ipsum', 'attributeType': None, 'primary': True, 'foreign': False},
					{'attribute':'dolor', 'attributeType': None, 'primary': False, 'foreign': False},
					{'attribute':'sit', 'attributeType': None, 'primary': False, 'foreign': False},
				],
			}})
		t.strengthenWeakIdentifiers()
		self.assertEqual(t.tables,expected)
		expected.update({
			'SEMPER': { 'name': 'SEMPER',
				'columns': [
					{'format': 'nonDf', 'attribute': 'ultricies', 'attributeType': None, 'association': 'SEMPER', 'entity': 'RISUS', 'primary': True, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'cras', 'attributeType': None, 'association': 'SEMPER', 'entity': 'RISUS', 'primary': True, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'ligula', 'attributeType': None, 'association': 'SEMPER', 'entity': 'DIGNISSIM', 'primary': True, 'foreign': True},
				],
			},
			'SOLLICITUDIN': { 'name': 'SOLLICITUDIN',
				'columns': [
					{'format': 'nonDf', 'attribute': 'diam', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'SUSPENDISSE', 'primary': True, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'elit', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'CONSECTETUER', 'primary': True, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'diam', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'LOREM', 'primary': True, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'ipsum', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'LOREM', 'primary': True, 'foreign': True},
					{'attribute': 'lectus', 'attributeType': None, 'primary': False, 'foreign': False},
				],
			},
			'MAECENAS': { 'name': 'MAECENAS',
				'columns': [
					{'format': 'nonDf', 'attribute': 'ligula', 'attributeType': None, 'association': 'MAECENAS', 'entity': 'DIGNISSIM', 'primary': True, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'ligula', 'attributeType': None, 'association': 'MAECENAS', 'entity': 'DIGNISSIM', 'primary': True, 'foreign': True},
				],
			},
		})
		expected["RISUS"]["columns"].extend([
			{'format': 'df', 'attribute': 'ultricies', 'attributeType': None, 'association': 'NON', 'entity': 'RISUS', 'primary': False, 'foreign': True},
			{'format': 'df', 'attribute': 'cras', 'attributeType': None, 'association': 'NON', 'entity': 'RISUS', 'primary': False, 'foreign': True},
		])
		expected["DIGNISSIM"]["columns"].extend([
			{'format': 'df', 'attribute': 'ultricies', 'attributeType': None, 'association': 'TORTOR', 'entity': 'RISUS', 'primary': False, 'foreign': True},
			{'format': 'df', 'attribute': 'cras', 'attributeType': None, 'association': 'TORTOR', 'entity': 'RISUS', 'primary': False, 'foreign': True},
			{'format': 'df', 'attribute': 'elit', 'attributeType': None, 'association': 'TORTOR', 'entity': 'CONSECTETUER', 'primary': False, 'foreign': True},
			{'attribute': 'nec', 'attributeType': None, 'primary': False, 'foreign': False},
		])
		expected["LOREM"]["columns"].extend([
			{'format': 'df', 'attribute': 'elit', 'attributeType': None, 'association': 'AMET', 'entity': 'CONSECTETUER', 'primary': False, 'foreign': True},
			{'attribute': 'adipiscing', 'attributeType': None, 'primary': False, 'foreign': False},
		])
		t.processAssociations()
		self.assertEqual(t.tables,expected)
		format = {
			"extension": ".txt",
			"opening": "",
			"table": "%s",
			"primary": "_%s_",
			"simple": "%s",
			"foreign": "#%s",
			"foreignPrimary": "_#%s_",
			"columnSep": ", ",
			"line": "%(table)s (%(columns)s)",
			"lineSep": "\n",
			"closing": "",
			"comment": "--- %s",
			"replace": [],
			"strengthen": "%(attribute)s.%(association)s.%(entity)s(strengthen)",
			"df": "%(attribute)s.%(association)s.%(entity)s(df)",
			"nonDf": "%(attribute)s.%(association)s.%(entity)s(nonDf)",
			"distinguish": "%(label)s.%(count)s"
		}
		expected = """\
SOLLICITUDIN (_#diam.SOLLICITUDIN.SUSPENDISSE(nonDf)_, _#elit.SOLLICITUDIN.CONSECTETUER(nonDf)_, _#diam.SOLLICITUDIN.LOREM(nonDf)_, _#ipsum.SOLLICITUDIN.LOREM(nonDf)_, lectus)
SEMPER (_#ultricies.SEMPER.RISUS(nonDf)_, _#cras.SEMPER.RISUS(nonDf)_, _#ligula.SEMPER.DIGNISSIM(nonDf)_)
RISUS (_ultricies_, _cras_, elementum, #ultricies.NON.RISUS(df), #cras.NON.RISUS(df))
MAECENAS (_#ligula.MAECENAS.DIGNISSIM(nonDf).1_, _#ligula.MAECENAS.DIGNISSIM(nonDf).2_)
DIGNISSIM (_ligula_, massa, varius, #ultricies.TORTOR.RISUS(df), #cras.TORTOR.RISUS(df), #elit.TORTOR.CONSECTETUER(df), nec)
CONSECTETUER (_elit_, sed)
--- SUSPENDISSE (_diam_)
LOREM (_#diam.DF.SUSPENDISSE(strengthen)_, _ipsum_, dolor, sit, #elit.AMET.CONSECTETUER(df), adipiscing)"""
		self.assertEqual(t.getText(format),expected)
	
	def testForeignKeyAllNSpecialCase(self):
		clauses = """
		LOREM: -ipsum, dolor, sit
		CONSECTETUER: elit, sed
		SUSPENDISSE: diam
		SOLLICITUDIN, 0N SUSPENDISSE, 0N /CONSECTETUER, 0N LOREM: lectus
		"""
		t = Tables(Mcd(clauses.split("\n"),{"df": u"DF","sep": u","}))
		t.processAll()
		expected = { 'name': 'SOLLICITUDIN',
				'columns': [
					{'format': 'nonDf', 'attribute': 'diam', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'SUSPENDISSE', 'primary': True, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'elit', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'CONSECTETUER', 'primary': False, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'ipsum', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'LOREM', 'primary': True, 'foreign': True},
					{'attribute': 'lectus', 'attributeType': None, 'primary': False, 'foreign': False},
				],
			}
		self.assert_('SOLLICITUDIN' in t.tables)
		self.assertEqual(t.tables['SOLLICITUDIN'], expected)


	
	def testForeignKey01SpecialCase(self):
		clauses = """
		LOREM: -ipsum, dolor, sit
		CONSECTETUER: elit, sed
		SUSPENDISSE: diam
		SOLLICITUDIN, 01 SUSPENDISSE, 0N /CONSECTETUER, 0N /LOREM: lectus
		"""
		t = Tables(Mcd(clauses.split("\n"),{"df": u"DF","sep": u","}))
		t.processAll()
		expected = { 'name': 'SOLLICITUDIN',
				'columns': [
					{'format': 'nonDf', 'attribute': 'diam', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'SUSPENDISSE', 'primary': True, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'elit', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'CONSECTETUER', 'primary': False, 'foreign': True},
					{'format': 'nonDf', 'attribute': 'ipsum', 'attributeType': None, 'association': 'SOLLICITUDIN', 'entity': 'LOREM', 'primary': False, 'foreign': True},
					{'attribute': 'lectus', 'attributeType': None, 'primary': False, 'foreign': False},
				],
			}
	
	def testMySQLOutput(self):
		format = {
			"extension": "sql",
			"opening": "",
			"table": "`%s`",
			"primary": "`%s`",
			"simple": "`%s`",
			"foreign": "`%s`",
			"foreignPrimary": "`%s`",
			"attributeWithType": "%(attribute)s %(attributeType)s",
			"columnSep": ",\n  ",
			"line": "CREATE TABLE %(table)s (\n  %(columns)s,\n  PRIMARY KEY(%(primaryList)s)\n) ENGINE=InnoDB  DEFAULT CHARSET=utf8;",
			"lineSep": "\n\n",
			"primarySep": ", ",
			"closing": "",
			"comment": "/*\n%s\n*/",
			"strengthen":"%(attribute)s",
			"df":"%(attribute)s",
			"nonDf":"%(attribute)s",
			"distinguish":"%(label)s.%(count)s",
			"replace": [],
			"addForeignKey": "ALTER TABLE `%(table)s` ADD FOREIGN KEY (`%(foreignKey)s`) REFERENCES `%(foreignTable)s` (`%(foreignKey)s`) ON UPDATE CASCADE;"
		}
		clauses = """
		CLIENT: Réf. client [varchar(8)], Nom [varchar(20)], Prénom [varchar(20)], Adresse [varchar(40)]
		DF, 0N CLIENT, 11 COMMANDE
		COMMANDE: Num commande [tinyint(4)], Date [date], Montant [decimal(5,2) DEFAULT '0.00']
		INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
		PRODUIT: Réf. produit [varchar(8)], Libellé [varchar(20)], Prix unitaire [decimal(5,2) DEFAULT '0.00']
		"""
		t = Tables(Mcd(clauses.split("\n"),{"df": u"DF","sep": u","}))
		t.processAll()
		expected = """\
CREATE TABLE `PRODUIT` (
  `Réf. produit` varchar(8),
  `Libellé` varchar(20),
  `Prix unitaire` decimal(5,2) DEFAULT '0.00',
  PRIMARY KEY(`Réf. produit`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `CLIENT` (
  `Réf. client` varchar(8),
  `Nom` varchar(20),
  `Prénom` varchar(20),
  `Adresse` varchar(40),
  PRIMARY KEY(`Réf. client`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `COMMANDE` (
  `Num commande` tinyint(4),
  `Date` date,
  `Montant` decimal(5,2) DEFAULT '0.00',
  `Réf. client` varchar(8),
  PRIMARY KEY(`Num commande`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `INCLURE` (
  `Num commande` tinyint(4),
  `Réf. produit` varchar(8),
  `Quantité` tinyint(4),
  PRIMARY KEY(`Num commande`, `Réf. produit`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

ALTER TABLE `COMMANDE` ADD FOREIGN KEY (`Réf. client`) REFERENCES `CLIENT` (`Réf. client`) ON UPDATE CASCADE;

ALTER TABLE `INCLURE` ADD FOREIGN KEY (`Num commande`) REFERENCES `COMMANDE` (`Num commande`) ON UPDATE CASCADE;

ALTER TABLE `INCLURE` ADD FOREIGN KEY (`Réf. produit`) REFERENCES `PRODUIT` (`Réf. produit`) ON UPDATE CASCADE;"""
		self.assertEqual(t.getText(format),expected)
	#
	# The same, with automatic comment when one foreign table has only one attribute
	#
		clauses = """
		CLIENT: Réf. client [varchar(8)]
		DF, 0N CLIENT, 11 COMMANDE
		COMMANDE: Num commande [tinyint(4)], Date [date], Montant [decimal(5,2) DEFAULT '0.00']
		INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
		PRODUIT: Réf. produit [varchar(8)], Libellé [varchar(20)], Prix unitaire [decimal(5,2) DEFAULT '0.00']
		"""
		t = Tables(Mcd(clauses.split("\n"),{"df": u"DF","sep": u","}))
		t.processAll()
		expected = """\
CREATE TABLE `PRODUIT` (
  `Réf. produit` varchar(8),
  `Libellé` varchar(20),
  `Prix unitaire` decimal(5,2) DEFAULT '0.00',
  PRIMARY KEY(`Réf. produit`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

/*
CREATE TABLE `CLIENT` (
  `Réf. client` varchar(8),
  PRIMARY KEY(`Réf. client`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
*/

CREATE TABLE `COMMANDE` (
  `Num commande` tinyint(4),
  `Date` date,
  `Montant` decimal(5,2) DEFAULT '0.00',
  `Réf. client` varchar(8),
  PRIMARY KEY(`Num commande`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `INCLURE` (
  `Num commande` tinyint(4),
  `Réf. produit` varchar(8),
  `Quantité` tinyint(4),
  PRIMARY KEY(`Num commande`, `Réf. produit`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

/*
ALTER TABLE `COMMANDE` ADD FOREIGN KEY (`Réf. client`) REFERENCES `CLIENT` (`Réf. client`) ON UPDATE CASCADE;
*/

ALTER TABLE `INCLURE` ADD FOREIGN KEY (`Num commande`) REFERENCES `COMMANDE` (`Num commande`) ON UPDATE CASCADE;

ALTER TABLE `INCLURE` ADD FOREIGN KEY (`Réf. produit`) REFERENCES `PRODUIT` (`Réf. produit`) ON UPDATE CASCADE;"""
		self.assertEqual(t.getText(format),expected)

if __name__ == '__main__':
	unittest.main()