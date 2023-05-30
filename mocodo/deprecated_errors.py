from mocodo.mocodo_error import MocodoError

MocodoError(21, _('"{clause}" does not constitute a valid declaration of an entity or association.').format(clause=clause)) # fmt: skip
MocodoError(24, _('Unknown specialization "{name}".').format(name=name)) # fmt: skip
MocodoError(11, _('Missing leg in association "{name}".').format(name=self.name)) # fmt: skip
MocodoError(42, _('Malformed constraint ratios "{ratios}".').format(ratios=self.ratios))
