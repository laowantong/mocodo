#!/usr/bin/python
# encoding: utf-8

import re

class Tables:
	
	def __init__(self,mcd):
		self.mcd = mcd
		self.exclude = set()
	
	def processAll(self):
		self.tablesFromEntities()
		self.strengthenWeakIdentifiers()
		self.processAssociations()
		self.sort()
	
	def getText(self,format):
		def substitutions(s):
			for (pattern,repl) in format["replace"]:
				s = re.sub(pattern,repl,s)
			return s
		
		def case(fmt,s):
			if "%s" in fmt:
				return fmt % s
			return fmt % {
				"capitalize": s.capitalize(),
				"upper": s.upper(),
				"lower": s.lower(),
				"title": s.title(),
			}
		
		def distinguishLabels(columns):
			occurrences = {}
			for column in columns:
				occurrences[column["label"]] = occurrences.get(column["label"],0) + 1
			occurrences = dict(c for c in occurrences.iteritems() if c[1]>1)
			for column in reversed(table["columns"]):
				label = column["label"]
				if label in occurrences:
					column["count"] = occurrences[label]
					column["label"] = format["distinguish"] % column
					occurrences[label] -= 1
		
		lines = []
		foreignKeys = []
		for table in sorted(self.tables.values(),key=lambda v:v["index"]):
			labels = []
			for column in table["columns"]:
				column["label"] = (format[column["format"]] % column if "format" in column else column["attribute"])
			distinguishLabels(table["columns"])
			primaryList = []
			for column in table["columns"]:
				label = substitutions(column["label"])
				nature = {
					(True,True): "foreignPrimary",
					(True,False): "primary",
					(False,True): "foreign",
					(False,False): "simple",
				}[(column["primary"],column["foreign"])]
				label = case(format[nature],label)
				if column["primary"]:
					primaryList.append(label)
				if column["attributeType"]:
					label = format.get("attributeWithType","%(attribute)s") % ({"attribute":label,"attributeType":column["attributeType"]})
				labels.append(label)
			name = case(format["table"],substitutions(table["name"]))
			line = format["line"] % {
				"table": name,
				"columns":format["columnSep"].join(labels),
				"primaryList": format.get("primarySep","").join(primaryList),
				}
			if len(table["columns"]) == 1:
				line = format["comment"] % line
			if "addForeignKey" in format:
				for column in table["columns"]:
					if column["foreign"]:
						foreignKeys.append(format["addForeignKey"] % {
							"table": substitutions(table["name"]),
							"foreignTable": substitutions(column["entity"]),
							"foreignKey": substitutions(column["attribute"]),
						})
						if len(self.tables[column["entity"]]["columns"]) == 1:
							foreignKeys[-1] = format["comment"] % foreignKeys[-1]
			lines.append(line)
		lines.extend(foreignKeys)
		return format["opening"] + format["lineSep"].join(lines) + format["closing"]
	
	# private
	
	def tablesFromEntities(self):
		self.tables = {}
		for (name,entity) in self.mcd.entities.iteritems():
			self.tables[name] = {
				"name": entity.cartouche,
				"columns" : []
			}
			for attribute in entity.attributes:
				self.tables[name]["columns"].append({
					"attribute": attribute.label,
					"attributeType": attribute.attributeType,
					"primary": attribute.getCategory() in ("strong","weak"),
					"foreign": False,
				})
	
	def strengthenWeakIdentifiers(self):
		def strenghten():
			for association in self.mcd.associations.itervalues():
				for leg in association.legs:
					if leg.entityName == entityName and leg.cards[:2] == "11":
						for strongLegCandidate in association.legs:
							if strongLegCandidate.cards[1] == "N":
								self.tables[entityName]["columns"] = [
									{
										"format": "strengthen",
										"attribute": a["attribute"],
										"attributeType": a["attributeType"],
										"entity": self.mcd.entities[strongLegCandidate.entityName].cartouche,
										"association": association.cartouche,
										"primary": True,
										"foreign": True,
									} for a in self.tables[strongLegCandidate.entityName]["columns"] if a["primary"]
								] + self.tables[entityName]["columns"]
								self.exclude.add((entityName,association.name,strongLegCandidate.entityName))
								return
		for (entityName,entity) in self.mcd.entities.iteritems():
			for attribute in entity.attributes:
				if attribute.getCategory() == "weak":
					strenghten()
	
	def processAssociations(self):
		for association in self.mcd.associations.itervalues():
			(entityName,entityPriority) = (None,0)
			mayIdentify = True
			for leg in association.legs:
				currentEntityPriority = (2 if leg.cards[:2]=="11" else (1 if leg.cards[:2]=="01" else 0))
				if currentEntityPriority > entityPriority:
					entityName = leg.entityName
					entityPriority = currentEntityPriority
				mayIdentify = mayIdentify and leg.mayIdentify
			if entityName is None or (entityPriority == 1 and not mayIdentify):
				self.tables[association.name] = {
					"name": association.cartouche,
					"columns": [{
								"format": "nonDf",
								"attribute": a["attribute"],
								"attributeType": a["attributeType"],
								"entity": self.mcd.entities[leg.entityName].cartouche,
								"association": association.cartouche,
								"primary": leg.mayIdentify,
								"foreign": True
							} for leg in association.legs for a in self.tables[leg.entityName]["columns"] if a["primary"]
						] + [{
								"attribute":attribute.label,
								"attributeType": attribute.attributeType,
								"primary": False,
								"foreign": False
							}  for attribute in association.attributes
						]
					}
			else:
				strongColumns = []
				alreadyRejected = False
				for leg in association.legs:
					if leg.entityName != entityName or alreadyRejected:
						if (entityName,association.name,leg.entityName) not in self.exclude:
							self.tables[entityName]["columns"].extend({
									"format": "df",
									"attribute": a["attribute"],
									"attributeType": a["attributeType"],
									"entity": self.mcd.entities[leg.entityName].cartouche,
									"association": association.cartouche,
									"primary": False,
									"foreign": True,
								} for a in self.tables[leg.entityName]["columns"] if a["primary"])
					else:
						alreadyRejected = True
				self.tables[entityName]["columns"].extend([{"attribute":attribute.label, "attributeType": attribute.attributeType, "primary": False, "foreign": False} for attribute in association.attributes])
	
	def sort(self):
		index = 0
		for row in self.mcd.ordering:
			for box in row:
				if box.name in self.tables:
					self.tables[box.name]["index"] = index
				index += 1
	
