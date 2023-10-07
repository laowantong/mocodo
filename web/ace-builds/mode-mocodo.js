define("ace/mode/mocodo_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"], function(require, exports, module){"use strict";
var oop = require("../lib/oop");
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;

var MocodoHighlightRules = function() {
    // regexp must not have capturing parentheses. Use (?:) instead.
    // regexps are ordered -> the first match is used

    this.$rules = {
        start: [{
            include: "#indent"
        }, {
            include: "#comment"
        }, {
            include: "#phantoms"
        }, {
            include: "#constraint_clause"
        }, {
            include: "#inheritance_clause"
        }, {
            include: "#association_clause"
        }, {
            include: "#entity_clause"
        }, {
            include: "#invalid"
        }],
        "#indent": [{
            token: "text",
            regex: /^\s+/
        }],
        "#comment": [{
            token: "comment.line.magic.mocodo markup.bold",
            regex: /%%mocodo\b.*$/
        }, {
            token: "comment.line.normal.mocodo",
            regex: /%.*$/
        }],
        "#phantoms": [{
            token: "punctuation.separator.phantom.mocodo markup.italic",
            regex: /:[:\s]*$/
        }],
        "#association_clause": [{
            token: [
                "keyword.control.mocodo",
                "entity.other.attribute-name.association.mocodo markup.bold"
            ],
            regex: /((?:\+|-)?)((?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF])[^=<>,:\\]*[^-\[\]\\=<>,:\s\\])(?=\s*,\s*)/,
            push: [{
                token: "association.mocodo",
                regex: /$|^/,
                next: "pop"
            }, {
                include: "#association_legs"
            }, {
                defaultToken: "association.mocodo"
            }]
        }],
        "#association_legs": [{
            token: [
                "text",
                "keyword.control.card_hidden.mocodo",
                "keyword.control.card_prefix.mocodo",
                "entity.other.attribute-name.cardinality.mocodo",
                "keyword.control.arrow.mocodo",
                "text",
                "invisible.note.mocodo",
                "text",
                "heading.entity.mocodo",
                "text"
            ],
            regex: /(\s*,\s*)(?:((?:-)?)((?:[_\/])?)((?![-_\/])[\w?]{2}(?=[\s]*[^\w,\r$:])))?((?:[<>])?)(\s*)((?:\[.*?\])?)(\s*)((?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF])[^=<>,:\\]*[^-\[\]\\=<>,:\s\\])(\s*)/
        }, {
            include: "#association_attrs"
        }, {
            include: "#invalid"
        }],
        "#association_attrs": [{
            token: "attrs.mocodo",
            regex: /\s*:\s*/,
            push: [{
                token: "attrs.mocodo",
                regex: /$|^/,
                next: "pop"
            }, {
                include: "#typed_attr"
            }, {
                token: "punctuation.separator",
                regex: /\s*,\s*/
            }, {
                defaultToken: "attrs.mocodo"
            }]
        }],
        "#typed_attr": [{
            token: [
                "variable.attribute.mocodo",
                "typed_attribute.mocodo",
                "variable.parameter.datatype.mocodo markup.italic",
                "typed_attribute.mocodo"
            ],
            regex: /((?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s])(\s*)((?:\[.*?\])?)(\s*)/
        }],
        "#entity_clause": [{
            token: [
                "keyword.control.mocodo",
                "heading.entity.mocodo markup.bold",
                "entity.mocodo"
            ],
            regex: /((?:\+|-)?)((?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF])[^=<>,:\\]*[^-\[\]\\=<>,:\s\\])(\s*:\s*)/,
            push: [{
                token: "entity.mocodo",
                regex: /$|^/,
                next: "pop"
            }, {
                include: "#entity_first_attr"
            }, {
                defaultToken: "entity.mocodo"
            }]
        }],
        "#entity_first_attr": [{
            token: [
                "invisible.id_symbols.mocodo",
                "variable.attribute.mocodo",
                "invisible.alt_id_symbols.mocodo",
                "variable.attribute.mocodo markup.underline",
                "text",
                "variable.parameter.datatype.mocodo markup.italic"
            ],
            regex: /(?:((?:\d*0\d*_|_))((?:(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]|#(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]\s*>\s*(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]\s*>\s*(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]))|((?:[1-9]+_)?)((?:(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]|#(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]\s*>\s*(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]\s*>\s*(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]))|)(\s*)((?:\[.*?\])?)/,
            push: [{
                token: "text",
                regex: /$|^/,
                next: "pop"
            }, {
                include: "#entity_next_attrs"
            }, {
                include: "#invalid"
            }]
        }],
        "#entity_next_attrs": [{
            token: [
                "text",
                "invisible.id_symbols.mocodo",
                "variable.attribute.mocodo markup.underline",
                "invisible.alt_id_symbols.mocodo",
                "variable.attribute.mocodo",
                "text",
                "variable.parameter.datatype.mocodo markup.italic"
            ],
            regex: /(\s*,\s*)(?:((?:\d*0\d*_|_))((?:(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]|#(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]\s*>\s*(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]\s*>\s*(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]))|((?:[1-9]+_)?)((?:(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]|#(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]\s*>\s*(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]\s*>\s*(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]))|)(\s*)((?:\[.*?\])?)/
        }, {
            include: "#invalid"
        }],
        "#constraint_clause": [{
            token: [
                "support.function.constraint_name.mocodo markup.bold",
                "constraint.mocodo",
                "invisible.note.mocodo",
                "constraint.mocodo"
            ],
            regex: /(\([a-zA-Z\u00C0-\u024F\u1E00-\u1EFF\d_\s]{0,3}\))(\s*)((?:\[.*?\])?)(\s*)/,
            push: [{
                token: "constraint.mocodo",
                regex: /$|^/,
                next: "pop"
            }, {
                include: "#constraint_targets"
            }, {
                defaultToken: "constraint.mocodo"
            }]
        }],
        "#constraint_targets": [{
            token: [
                "string.regexp.constraint_leg.mocodo",
                "text",
                "support.type.box.mocodo"
            ],
            regex: /((?:<?(?:\.+|-+)>?)?)(\s*)((?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF])[^=<>,:\\]*[^-\[\]\\=<>,:\s\\])/
        }, {
            token: "text",
            regex: /\s*,\s*/
        }, {
            include: "#constraint_coords"
        }, {
            include: "#invalid"
        }],
        "#constraint_coords": [{
            token: [
                "coords.mocodo",
                "invisible.constraint_coords.mocodo markup.italic",
                "coords.mocodo",
                "invisible.constraint_coords.mocodo markup.italic"
            ],
            regex: /(\s*:\s*)((?:-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF])[^=<>,:\\]*[^-\[\]\\=<>,:\s\\]))(\s*,\s*)((?:-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF])[^=<>,:\\]*[^-\[\]\\=<>,:\s\\]))$/
        }],
        "#inheritance_clause": [{
            token: [
                "entity.other.attribute-name.inheritance.mocodo markup.underline markup.bold",
                "inheritance.mocodo",
                "heading.parent.mocodo",
                "inheritance.mocodo",
                "keyword.control.arrow.mocodo",
                "inheritance.mocodo"
            ],
            regex: /(\/(?:XT\d?|TX\d?|X\d?|T\d?|\d?)\\{1,2})(\s*)((?:(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF])[^=<>,:\\]*[^-\[\]\\=<>,:\s\\])?)(\s*)((?:<==?|<--?|--?>|==?>))(\s*)/,
            push: [{
                token: "inheritance.mocodo",
                regex: /$|^/,
                next: "pop"
            }, {
                include: "#inheritance_children"
            }, {
                defaultToken: "inheritance.mocodo"
            }]
        }],
        "#inheritance_children": [{
            token: "heading.child.mocodo",
            regex: /(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF])[^=<>,:\\]*[^-\[\]\\=<>,:\s\\]/
        }, {
            token: "text",
            regex: /\s*,\s*/
        }, {
            include: "#inheritance_attrs"
        }, {
            include: "#invalid"
        }],
        "#inheritance_attrs": [{
            token: "attrs.mocodo",
            regex: /\s*:\s*/,
            push: [{
                token: "attrs.mocodo",
                regex: /$|^/,
                next: "pop"
            }, {
                token: "invisible.inheritance_attribute.mocodo markup.italic",
                regex: /(?=[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF0-9])[^\[\]>,]*[^\[\]>,\s]/
            }, {
                token: "text",
                regex: /\s*,\s*/
            }, {
                include: "#invalid"
            }, {
                defaultToken: "attrs.mocodo"
            }]
        }],
        "#invalid": [{
            token: "invalid.illegal.mocodo",
            regex: /.+/
        }]
    }
    
    this.normalizeRules();
};

MocodoHighlightRules.metaData = {
    name: "Mocodo",
    scopeName: "source.mocodo"
}


oop.inherits(MocodoHighlightRules, TextHighlightRules);

exports.MocodoHighlightRules = MocodoHighlightRules;
});

define("ace/mode/mocodo",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/mocodo_highlight_rules"], function(require, exports, module){"use strict";
var oop = require("../lib/oop");
var TextMode = require("./text").Mode;
var MocodoHighlightRules = require("./mocodo_highlight_rules").MocodoHighlightRules;
var Mode = function () {
    this.HighlightRules = MocodoHighlightRules;
    this.$behaviour = this.$defaultBehaviour;
};
oop.inherits(Mode, TextMode);
(function () {
    this.lineCommentStart = "%";
    this.$id = "ace/mode/mocodo";
}).call(Mode.prototype);
exports.Mode = Mode;

});                (function() {
                    window.require(["ace/mode/mocodo"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            