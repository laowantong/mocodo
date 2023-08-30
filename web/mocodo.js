/*global $, jQuery*/
'use strict';
var request_lock = false;
var delays = {
  "15 secondes": 15,
  "30 secondes": 30,
  "1 minute": 60,
  "2 minutes": 120,
  "4 minutes": 240,
  "8 minutes": 480,
}
var flex = {
  "désactivée": 0,
  "peu perceptible": 0.25,
  "faible": 0.5,
  "normale": 0.75,
  "forte": 1.0,
  "très prononcée": 1.25,
}
var relation_formats = {
  "markdown_data_dict": {
    "default": false,
    "highlighting": "none",
    "title": "Option placée ici par commodité: un dictionnaire des données n&#39;a rien à voir avec un schéma relationnel.",
    "name": "Dictionnaire des données (Markdown)",
  },
  "text": {
    "default": false,
    "highlighting": "none",
    "name": "Texte brut",
  },
  "latex": {
    "default": false,
    "highlighting": "latex",
    "name": 'LaTeX',
  },
  "markdown": {
    "default": false,
    "highlighting": "markdown",
    "name": "Markdown",
  },
  "explain_html": {
    "default": false,
    "highlighting": "markup",
    "title": "S&#39;affiche également au-dessous du diagramme conceptuel.",
    "name": "Explications du schéma relationnel",
  },
  "diagram": {
    "default": false,
    "highlighting": "none",
    "title": "Résultat à réinjecter sous l&#39;onglet Entrée pour tracer un diagramme sagittal des relations.",
    "name": "Diagramme relationnel",
  },
  "dependencies": {
    "default": false,
    "highlighting": "graphviz",
    "name": "Graphe des dépendances",
  },
  // "": {
  //   "default": false,
  //   "highlighting": "json",
  //   "name": 'JSON',
  // },
  // "explain_markdown": {
  //   "default": false,
  //   "highlighting": "markdown",
  //   "name": "Markdown avec explications",
  // },
  "mysql": {
    "default": false,
    "highlighting": "sql",
    "name": "MySQL",
  },
  "oracle": {
    "default": false,
    "highlighting": "sql",
    "name": "Oracle",
  },
  "postgresql": {
    "default": false,
    "highlighting": "sql",
    "name": "PostgreSQL",
  },
  "sqlite": {
    "default": false,
    "highlighting": "sql",
    "name": "SQLite",
  },
}
function createTabs() {
  $('ul.tabs').each(function () { // based upon http://www.jacklmoore.com/notes/jquery-tabs
    $(this).find('a:not(.active)').each(function () {
      $($(this).attr('href')).hide();
    });
    $(this).on('click', 'a', function (e) {
      var $active = $(this).parent().siblings().children(".active");
      var $content = $($active.attr('href'));
      $active.removeClass('active');
      $content.hide();
      $active = $(this);
      $content = $($(this).attr('href'));
      $active.addClass('active');
      $content.show();
      e.preventDefault();
    });
  });
}
function activateTab(zone, target) {
  var $active = $(zone + ' a.active');
  if ("#" + $active.attr("id") === target) { return; }
  var $content = $($active.attr('href'));
  $active.removeClass('active');
  $content.hide();
  $active = $(target);
  $content = $($active.attr('href'));
  $active.addClass('active');
  $content.show();
}
function createOptions(id, items, selected) {
  $.each(items, function (i, elt) {
    $("#" + id).append("<option" + (elt === selected ? " selected='selected'" : "") + ">" + elt + "<\/option>");
  });
}
function createFormatCheckboxes() {
  var s = '';
  var items = Object.keys(relation_formats).map(function (key) {
    return {
      "id": key,
      "name": relation_formats[key]["name"],
      "default": relation_formats[key]["default"],
      "not_sql": relation_formats[key]["highlighting"] !== "sql",
      "title": relation_formats[key]["title"]
    }
  });
  $.each(items, function (index, elt) {
    if (elt["not_sql"]) {
      s = "<li><input type='checkbox' name=relations[]' value='" + elt["id"] + "'";
      if (elt["default"]) { s += " checked='checked'" };
      s += " onchange='markAsDirty();writeCookie()'\/> <label ";
      if (elt["title"]) { s += " title='" + elt["title"] + "'" };
      s += ">" + elt["name"] + "<\/label><\/li>";
      $("#relation_formats").append(s);
    }
  })
}
function refreshSize(geo) {
  var s = '<div><label>&nbsp;<\/label> ' +
    '<input value="' + geo.width + '" type="text" onfocus="markAsMoved()" name="width" id="width" min="0"\/> ' +
    '<input value="' + geo.height + '" type="text" onfocus="markAsMoved()" name="height" id="height" min="0"\/> ' +
    '<\/div>';
  $("#size").html(s);
}
function refreshCoordinates(geo) {
  var s = ''
  $.each(geo["cx"], function (i, itemx) {
    var key = itemx[0]
    var cx = itemx[1]
    var cy = geo["cy"][i][1]
    s += '<div><label>' + key + '<\/label> ' +
      '<input value="' + cx + '" type="text" onfocus="markAsMoved()" name="cx' + i + '" id="cx' + i + '" min="0"\/> ' +
      '<input value="' + cy + '" type="text" onfocus="markAsMoved()" name="cy' + i + '" id="cy' + i + '" min="0"\/> ' +
      '<\/div>';
  })
  $("#coords").html(s);
}
function refreshCardinalities(geo) {
  var s = '';
  $.each(geo["shift"], function (i, item) {
    s += '<div><label for="shift' + i + '">' + item[0] + '<\/label> <input value="' + item[1] + '" type="text"  onfocus="markAsMoved()" name="shift' + i + '" id="shift' + i + '"\/><\/div>';
  });
  $("#cards").html(s);
}
function refreshArrows(geo) {
  var s = '';
  $.each(geo["ratio"], function (i, item) {
    s += '<div><label for="ratio' + i + '">' + item[0] + '<\/label> <input value="' + item[1] + '" type="text"  onfocus="markAsMoved()" name="ratio' + i + '" id="ratio' + i + '"\/><\/div>';
  });
  $("#arrows").html(s);
}
function refreshDiagram(result) {
  $("#diagramOutput").html(result["svg"]);
  // switch to last page
  $(".diagram_page").each(function() { $(this).attr("visibility", "visible"); });
  $(".pager_dot").each(function() { $(this).attr("fill", "gray"); });
}
function refreshRelations(result) {
  var s = '';
  var supplement = '';
  var name = '';
  var highlighting = '';
  $.each(result["mld"], function (i, item) {
    name = relation_formats[item[0]]["name"];
    highlighting = relation_formats[item[0]]["highlighting"];
    s += `<fieldset class="listing">`;
    s += `<legend data-index=${i}>⧉ ${name}</legend>`;
    s += `<pre><code class="language-${highlighting}" id="code-${i}">`
    s += item[1];
    s += `</code></pre></fieldset>`;
    if (item[0] == "explain_html") {
      supplement = item[1].replace(new RegExp("&lt;", "g"), "<")
    };
  })
  $("#relationalOutput").html(s);
  $("#diagramOutputSupplement").html(supplement);
  var legends = document.getElementsByTagName("legend");
  for (var i = 0; i < legends.length; i++) {
    legends[i].addEventListener("click", function (event) {
      var index = event.target.dataset.index;
      var code = document.getElementById(`code-${index}`);
      navigator.clipboard.writeText(code.innerText + "\n");
      $(`#code-${index}`).highlight();
    })
  }
}

// stolen from https://stackoverflow.com/a/11589350/173003
$.fn.highlight = function () {
  $(this).each(function () {
    var el = $(this);
    el.before("<div/>")
    el.prev()
      .width(el.width())
      .height(el.height())
      .css({
        "position": "absolute",
        "backgroundColor": "#0000ff",
        "opacity": ".1"
      })
      .fadeOut(500);
  });
}
function generate() {
  if (request_lock) return;
  request_lock = true;
  $("#generateButton").addClass("fa-spin");
  var text = ace.edit("editor").getSession().getValue();
  $('textarea[name="text"]').val(text);
  $.ajax({
    type: "POST",
    url: "web/generate.php",
    data: $("#mainForm").serialize(),
    success: function (result) {
      result = $.parseJSON(result);
      if (result.hasOwnProperty("err")) {
        var error_message = result["err"].replace("<", "&lt;")
        $("#errorOutput").html("<pre>" + error_message + "</pre>");
        $("#errorTab").css("display", "inline");
        return;
      }
      var geo = $.parseJSON(result["geo"]);
      refreshSize(geo);
      refreshCoordinates(geo);
      refreshCardinalities(geo);
      refreshArrows(geo);
      $("#diagramOutput").removeClass('initial');
      $("#relationalOutput").removeClass('initial');
      refreshDiagram(result);
      refreshRelations(result);
      $("#title").val(result["title"]);
      $("#path").val(result["path"]);
      $("#archiveName").val(result["zip"]);
      if ($("#errorTab").hasClass('active')) {
        activateTab("#outputZone", "#diagramTab");
      }
      $("#errorTab").fadeOut();
      markAsReady();
      $("#downloadButton").fadeIn()
    },
    complete: function (data) {
      $("#generateButton").removeClass("fa-spin");
      request_lock = false;
    }
  });
};
function reorganize(algo) {
    $("#gear").addClass("fa-spin");
    $("#editor").addClass("flash");
    return $.ajax({
      type: "POST",
      url: "web/arrange.php",
      data: {
        algo: algo,
        text: ace.edit("editor").getSession().getValue(),
        timeout: delays[$("#delays").attr("value")]
      },
      success: function (result) {
        result = $.parseJSON(result);
        if (result.hasOwnProperty("err")) {
          var error_message = result["err"].replace("<", "&lt;")
          $("#errorOutput").html("<pre>" + error_message + "</pre>");
          $("#errorTab").css("display", "inline");
          return;
        }
        set_editor_content(result["text"]);
        if (!$("#diagramOutput").hasClass('initial') & algo!="fit=0" & algo!="fit=1") {
          request_lock = false;
          generate();
        }
      },
      complete: function (data) {
        $("#gear").removeClass("fa-spin");
        $("#editor").removeClass("flash");
        request_lock = false;
      }
    });
  };
function arrange(event) {
  if (request_lock) return;
  request_lock = true;
  if (event.shiftKey & event.altKey) {
    reorganize("fit=1").then(function () {reorganize("arrange=bb")});
  }
  else if (event.altKey) {
    reorganize("fit=0").then(function () {reorganize("arrange=bb")});
  }
  else if (event.shiftKey) {
    reorganize("arrange=bb");
  }
  else {
    reorganize("arrange=bb --organic");
  }
};
function reveal() {
  if (request_lock) return;
  request_lock = true
  $.ajax({
    type: "POST",
    url: "web/unbox.php",
    data: { title: $("#title").attr("value") },
    success: function (result) {
      if (result) {
        set_editor_content(result);
        if (!$("#diagramOutput").hasClass('initial')) {
          request_lock = false;
          generate();
        }
      }
    },
    complete: function (data) {
      request_lock = false;
    }
  });
};
function set_editor_content(text) {
  var editor = ace.edit("editor");
  editor.setValue(text);
  editor.selection.moveCursorFileStart();
  markAsDirty();
};
function markAsDirty() {
  $("#title").val($("#title").attr("value").replace(/[^A-Za-zÀ-ÖØ-öø-ÿ0-9 '\._-]/g, '-'));
  $("#state").val("dirty");
  $("#geoTab").fadeOut();
  $("#downloadButton").fadeOut();
};
function freezeTitle() {
  $("#guess_title").val($("#title").attr("value") == "" || $("#title").attr("value") == "Sans Titre");
};
function mayUnfreezeTitle() {
  if (/^tuto-\d\d\d\d$/.test($("#title").attr("value"))) {
    $("#guess_title").val(true);
  }
};
function changeTitleToNthTuto() {
  var index = $("select[id='tutorial'] option:selected").index();
  $("#title").val("tuto-" + ("000" + index).slice(-4));
  freezeTitle();
}
function markAsMoved() {
  $("#state").val("moved");
};
function markAsReady() {
  $("#state").val("ready");
  $("#geoTab").css("display", "inline");
};
function onBlur(elt) {
  if (/^ *$/i.test(elt.value)) {
    elt.value = elt.defaultValue;
  }
}
function onFocus(elt) {
  if (elt.value == elt.defaultValue) {
    elt.value = '';
  }
}
function writeCookie() {
  Cookies.set('mocodo-options', JSON.stringify($("#paramContents").find(":input").serializeArray()), { expires: 365 });
}
function readCookie() {
  var options = Cookies.get('mocodo-options');
  if (options) {
    var objects = $.parseJSON(options);
    $("#paramContents").find(":checkbox:checked").removeAttr("checked")
    $("#svg").prop("checked", true);
    $.each(objects, function (index, object) {
      var elt = $('[name="' + object.name + '"]');
      if (!elt[0]) { return };
      switch (elt[0].type) {
        case 'checkbox':
          elt.each(function () {
            if ($(this).attr('value') == object.value) {
              $(this).attr("checked", "checked");
            }
          });
          break;
        default:
          elt.val(object.value);
      }
    });
  }
}
$(document).keypress(function (e) {
  if (e.which == 13 && e.target.nodeName != "TEXTAREA") {
    return false
  };
});
$().ready(function () {
  createTabs();
	var editor = ace.edit("editor");
  // if it is launched from localhost, use the local pristine sandbox
  if (location.hostname == "localhost") {
    var pristine_sandbox = "/mocodo/mocodo/resources/pristine_sandbox.mcd";
  }
  else {
    var pristine_sandbox = "/resources/pristine_sandbox.mcd";
  }
  $.get(location.protocol + '//' + location.host + pristine_sandbox, function (data) {
    editor.setValue(data);
    editor.selection.moveCursorFileStart();
  });
  editor.session.setMode("ace/mode/mocodo");
  editor.setTheme("ace/theme/chrome");
	editor.setOptions({
    enableAutoIndent: false,
    showPrintMargin: false,
    showGutter: false,
    enableLiveAutocompletion: true,
	});
  editor.renderer.updateFull();
  var default_color = "brewer" + "+-"[Math.floor(Math.random() * 2)] + (Math.floor(Math.random() * 9) + 1);
  createOptions("colors", ["blank", "bw", "bw-alpha", "desert", "keepsake", "mondrian", "ocean", "pond", "wb", "xinnian", "brewer+1", "brewer-1", "brewer+2", "brewer-2", "brewer+3", "brewer-3", "brewer+4", "brewer-4", "brewer+5", "brewer-5", "brewer+6", "brewer-6", "brewer+7", "brewer-7", "brewer+8", "brewer-8", "brewer+9", "brewer-9"], default_color);
  createOptions("shapes", ["arial", "copperplate", "georgia", "mondrian", "sans", "serif", "times", "trebuchet", "verdana", "xinnian"], "verdana");
  createOptions("disambiguation", ["notes et numéros", "numéros seulement"], "notes et numéros");
  var items = Object.keys(delays).map(function (key) { return { "value": delays[key], "name": key } });
  items.sort(function (a, b) { return a["value"] - b["value"] });
  createOptions("delays", items.map(function (value, index) { return value["name"] }), "1 minute");
  items = Object.keys(flex).map(function (key) { return { "value": flex[key], "name": key } });
  items.sort(function (a, b) { return a["value"] - b["value"] });
  createOptions("flex", items.map(function (value, index) { return value["name"] }), "normale");
  createOptions("SQL_dialect", ["", "MySQL", "Oracle", "PostgreSQL", "SQLite"], "");
  createFormatCheckboxes();
  readCookie();
  createOptions("tutorial", ["MCD d'accueil", "Entité", "Attribut d'entité", "Association", "Attribut d'association", "Cardinalités", "Association de dépendance fonctionnelle", "Explication interactive des cardinalités", "Association réflexive", "Flèche sur une patte", "Schéma sur plusieurs rangées", "Réarrangement automatique", "Réarrangement automatique minimal", "Explication des cardinalités", "Rôle d'une patte pour le MLD", "MLD sous forme de diagramme relationnel", "Dévoilement progressif du schéma", "Entité faible (ou identification relative)", "Entité sans identifiant", "Identifiant composite", "Identifiants candidats", "MCD vide", "Boîtes homonymes", "Agrégation (ou pseudo-entité)", "Vue en extension", "Contrainte d'intégrité fonctionnelle (CIF)", "Contrainte sur associations", "Explication interactive d'une contrainte", "Héritage (ou spécialisation)"])
});
