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
var conversions = {
  "_data_dict.md": {
    "default": false,
    "highlighting": "none",
    "title": "Trois colonnes : entité ou association / attribut / type.",
    "name": "Dictionnaire des données en Markdown",
  },
  "_mld.mcd": {
    "default": false,
    "highlighting": "none",
    "title": "Résultat à réinjecter sous l&#39;onglet Entrée pour tracer un diagramme sagittal des relations.",
    "name": "Diagramme relationnel en Mocodo",
  },
  "_mld.html": {
    "default": false,
    "highlighting": "markup",
    "title": "Affiché également au-dessous du diagramme conceptuel.",
    "name": "Schéma relationnel en HTML avec explications escamotables",
  },
  "_ddl.sql": {
    "default": false,
    "highlighting": "sql",
    "title": "DDL agnostique, mais veillez à utiliser les types requis par le dialecte-cible (MySQL, SQLite, PostgreSQL, Oracle, SQL Server, etc.). Les libellés sont automatiquement convertis en ASCII et snake case pour éviter de surcharger le code SQL avec des délimiteurs de chaînes.",
    "name": "Requêtes SQL de création des tables",
  },
  "_url.url": {
    "default": true,
    "highlighting": "none",
    "title": "URL d&#39;une session Mocodo online pré-remplie avec le texte-source de votre MCD.",
    "name": "Lien de partage du MCD",
  },
  "_dependencies.gv": {
    "default": false,
    "highlighting": "graphviz",
    "title": "Vue simplifiée des contraintes de clés étrangères. Copiez-collez le résultat sur le site donné en lien pour visualiser le diagramme.",
    "name": "Graphe des dépendances pour <a href='https://dreampuf.github.io/GraphvizOnline/' target='_blank'>Graphviz</a>",
    "advanced": true,
  },
  "_mld.txt": {
    "default": false,
    "highlighting": "txt",
    "name": "Schéma relationnel en texte brut",
    "advanced": true,
  },
  "_mld.tex": {
    "default": false,
    "highlighting": "tex",
    "name": "Schéma relationnel en LaTeX",
    "advanced": true,
  },
  "_mld.md": {
    "default": false,
    "highlighting": "markdown",
    "name": "Schéma relationnel en Markdown",
    "advanced": true,
  },
  "_uml.puml": {
    "default": false,
    "highlighting": "none",
    "title": "Copiez-collez le résultat sur le site donné en lien pour visualiser le diagramme.",
    "name": "Diagramme de classes UML pour <a href='https://www.plantuml.com/plantuml/uml' target='_blank'>PlantUML</a>",
    "advanced": true,
  },
  "_ddl.dbml": {
    "default": false,
    "highlighting": "dbml",
    "title": "DBML (database markup language) est un langage dédié simple et lisible conçu pour définir des structures de base de données.",
    "name": "Définition de la base en <a href='https://dbdiagram.io/' target='_blank'>DBML</a>",
    "advanced": true,
  },
}
var knowledge = {
  "basic": {
    "name": "Bases des bases",
    "title": "Acquis non négociables d&#39;une introduction aux bases de données : construction de modèles conceptuels simples, passage au relationnel, conversion en SQL.",
    "default": true
  },
  "weak": {
    "name": "Entité faible (ou identification relative)",
    "title": "Cochez pour inclure des entités faibles dans les MCD aléatoires et certaines opérations de décomposition. Une entité faible est une entité dont l&#39;identifiant nécessite d&#39;être renforcé par une ou plusieurs entités dont elle dépend fonctionnellement.",
    "default": false
  },
  "cluster": {
    "name": "Agrégation (ou pseudo-entité) / CIF",
    "title": "Cochez pour inclure une agrégation simple dans les MCD aléatoires et pour ajouter au menu « Révéler » une option permettant de la visualiser comme une Contrainte d&#39;intégrité fonctionnelle. Ces notions voisines traitent du cas où une des entités participant à une association est complètement déterminée par la connaissance d&#39;autres entités participantes : une ou plusieurs dans le cas général, toutes sous Mocodo.",
    "default": false,
    "onchange": "setClusterKnowledge(event.target.checked)",
  },
  "constraints": {
    "name": "Contraintes d'unicité et d'optionalité",
    "title": "Cochez pour faire apparaître dans le schéma relationnel les contraintes d&#39unicité en exposant, d&#39optionalité comme des « ? », et de non-optionalité comme des « ! ». Ces notations sont non standard et peuvent gêner la lecture. NB : quel que soit votre choix, Mocodo ajoute systématiquement les contraintes UNIQUE, NULL ou NOT NULL appropriées dans le code SQL généré.",
    "default": false
  },
  "random": {
    "name": "MCD masqués ou aléatoires",
    "title": "Cochez pour ajouter un bouton donnant accès à des opérations de masquage des libellés et de génération d&#39exercices aléatoires.",
    "default": false,
    "onchange": "setRandomKnowledge(event.target.checked)",
  },
  "decomposition": {
    "name": "Décomposition d'associations",
    "title": "Cochez pour ajouter un bouton donnant accès à des opérations de réécriture de certains types d&#39;associations.",
    "default": false,
    "onchange": "setDecompositionKnowledge(event.target.checked)",
  },
  "full_tutorial": {
    "name": "Tutoriel interactif (2/2)",
    "title": "Exigez des exemples d&#39;utilisation avancée de Mocodo online !",
    "default": false,
    "onchange": "setTutorialKnowledge(event.target.checked)",
  },
  "all_conversions": {
    "name": "Plus d'options de conversion",
    "title": "Cochez pour avoir accès à quelques options de conversion plus exotiques.",
    "default": false,
    "onchange": "setConversionKnowledge(event.target.checked)",
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
function createOptions(id, items, selected, on_demand_index) {
  $.each(items, function (i, elt) {
    $("#" + id).append("<option" + (elt === selected ? " selected='selected'" : "") + ">" + elt + "<\/option>");
  });
}
function createCheckboxes(group, group_name) {
  var s = '';
  $.each(group, function (key, value) {
    s = value["advanced"] ? "<li class='advanced'>" : "<li>";
    s += '<input type="checkbox" name="' + group_name + '[]" id=' + key + ' value="' + key + '"';
    if (value["default"]) { s += " checked='checked'" };
    s += " onchange='markAsDirty();writeCookie()"
    if (value["onchange"]) { s += ";" + value["onchange"] }
    s += "'\/> <label ";
    if (value["title"]) { s += " title='" + value["title"] + "'" };
    s += ">" + value["name"] + "<\/label><\/li>";
    $("#" + group_name).append(s);
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
  $.each(geo["cx"], function (i, item) {
    var key = item[0]
    var cx = item[1]
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
  var svg = result["svg"];
  var container = $("#diagramOutput");
  container.html(svg);
  var containerWidth = container.width();
  if (containerWidth) {
    var svgWidth = container.find("svg").width();
    if (svgWidth > containerWidth) {
      var scale = containerWidth / svgWidth;
      container.find("svg").attr("width", svgWidth * scale);
      container.find("svg").attr("height", container.find("svg").height() * scale);
    }
  }
  // switch to last page
  $(".diagram_page").each(function() { $(this).attr("visibility", "visible"); });
  $(".pager_dot").each(function() { $(this).attr("fill", "gray"); });
}
function refreshConvertOutput(result) {
  var s = '';
  var supplement = '';
  var name = '';
  var highlighting = '';
  $.each(result["conversions"], function (i, item) {
    name = conversions[item[0]]["name"];
    highlighting = conversions[item[0]]["highlighting"];
    s += `<fieldset class="listing">`;
    s += `<legend data-index=${i}>⧉ ${name}</legend>`;
    s += `<pre><code class="language-${highlighting}" id="code-${i}">`
    s += item[1];
    s += `</code></pre></fieldset>`;
    if (item[0] == "_mld.html") {
      supplement = item[1].replace(new RegExp("&lt;", "g"), "<")
    };
  })
  $("#convertOutput").html(s);
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
  $("#refreshButton").hide();
  $("#rotatingButton").show();
  var text = ace.edit("editor").getSession().getValue();
  $('textarea[name="text"]').val(text);
  var data = $("#mainForm").serializeArray();
  if ($("#constraints").prop("checked")) {
    for (var i = 0; i < data.length; i++) {
      if (data[i].value.startsWith("_mld")) {
        data[i].value += "_with_constraints";
      }
    }
  }
  $.ajax({
    type: "POST",
    url: "web/generate.php",
    data: $.param(data),
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
      $("#diagramOutput").removeClass('never_refreshed');
      $("#convertOutput").removeClass('never_refreshed');
      refreshDiagram(result);
      refreshConvertOutput(result);
      $("#title").val(result["title"]);
      $("#downloadButton").attr("href", result["zipURL"]);
      $("#downloadButton").attr("download", result["zipName"]);
      if ($("#errorTab").hasClass('active')) {
        activateTab("#outputZone", "#diagramTab");
      }
      $("#errorTab").fadeOut();
      markAsReady();
    },
    complete: function (data) {
      $("#refreshButton").show();
      $("#rotatingButton").hide();
      request_lock = false;
    }
  });
};
function rewrite(args) {
    if (request_lock) return;
    request_lock = true;
    $("#rotatingButton").show();
    $("#refreshButton").hide();
    $("#downloadButton").hide();
    $("#editor").addClass("flash");
    if (args.includes("arrange")) {
      args += ",timeout=" + delays[$("#delays").attr("value")];
      args = args.replace("arrange,", "arrange:");
    }
    if (args.includes("explode")) {
      args = $("#weak").prop("checked") ? args.replace(":", ":weak,") : args.replace("weak,", "");
    };
    if (args.includes("grow")) {
      args = $("#weak").prop("checked") ? args.replace(":", ":_11-*N=1,") : args.replace("_11-*N=1,", "");
      args = $("#cluster").prop("checked") ? args.replace(":", ":/*N-*N=1,") : args.replace("/*N-*N=1,", "");
    };
    return $.ajax({
      type: "POST",
      url: "web/rewrite.php",
      data: {
        args: args,
        text: ace.edit("editor").getSession().getValue()
      },
      success: function (result) {
        result = $.parseJSON(result);
        if (result.hasOwnProperty("err")) {
          var error_message = result["err"].replace("<", "&lt;")
          $("#errorOutput").html("<pre>" + error_message + "</pre>");
          $("#errorTab").css("display", "inline");
          return;
        }
        setEditorContent(result["text"]);
        if (!$("#diagramOutput").hasClass('never_refreshed')) {
          request_lock = false;
          generate();
        };
      },
      complete: function (data) {
        $("#refreshButton").show();
        $("#rotatingButton").hide();
        $("#editor").removeClass("flash");
        request_lock = false;
      }
    });
  };
function unbox() {
  if (request_lock) return;
  request_lock = true
  $.ajax({
    type: "POST",
    url: "web/unbox.php",
    data: { title: $("#title").attr("value") },
    success: function (result) {
      if (result) {
        setEditorContent(result);
        request_lock = false;
        generate();
      }
  },
    complete: function (data) {
      request_lock = false;
    }
  });
};
function setDecompositionKnowledge(is_visible) {
  is_visible ? $("#explodeButton").show() : $("#explodeButton").hide();
};
function setRandomKnowledge(is_visible) {
  is_visible ? $("#jokerButton").show() : $("#jokerButton").hide();
};
function setClusterKnowledge(is_visible) {
  is_visible ? $("#createCifs").show() : $("#createCifs").hide();
};
function setConversionKnowledge(is_visible) {
  is_visible ? $(".advanced").show() : $(".advanced").hide();
};

var tutorialOptions = ["Tutoriel interactif (1/2)", "Entité", "Identifiant et attributs d'entité", "Identifiant composite", "Association", "Cardinalités", "Attribut d'association", "Association de dépendance fonctionnelle", "Association réflexive", "Schéma relationnel", "Rôles", "Diagramme relationnel (1)", "Diagramme relationnel (2)", "Inférence de types", "Génération du DDL", "Schéma sur plusieurs rangées", "Réorganisation automatique", "Réorganisation automatique avec contraintes", "Pour aller plus loin...", "Explication interactive des cardinalités", "Flèche sur une patte", "MLD sous forme de diagramme relationnel", "Dévoilement progressif du schéma", "Entité faible (ou identification relative)", "Entité sans identifiant", "Identifiants candidats", "MCD vide", "Boîtes homonymes", "Agrégation (ou pseudo-entité)", "Vue en extension", "Contrainte d'intégrité fonctionnelle (CIF)", "Contrainte sur associations", "Explication interactive d'une contrainte", "Héritage (ou spécialisation)", "Rôle d'une patte pour le MLD"];
var basicTutorialLimit = 19;
function setTutorialKnowledge(is_advanced) {
  $("#tutorial").empty();
  if (is_advanced) {
    createOptions("tutorial", tutorialOptions.slice(basicTutorialLimit))
  } else {
    createOptions("tutorial", tutorialOptions.slice(0, basicTutorialLimit));
  }
}

function setEditorContent(text) {
  var editor = ace.edit("editor");
  editor.session.off('change', markAsDirty);
  editor.setValue(text + (text.slice(-1) == "\n" ? "" : "\n"));
  editor.session.on('change', markAsDirty);
  editor.selection.moveCursorFileStart();
};
function markAsDirty() {
  $("#title").val($("#title").attr("value").replace(/[^A-Za-zÀ-ÖØ-öø-ÿ0-9 '\._-]/g, '-'));
  $("#geoTab").fadeOut();
  $("#downloadButton").fadeOut();
  $("#state").val("dirty");
};
function changeTitleToNthTuto() {
  var index = $("select[id='tutorial'] option:selected").index();
  if ($("#full_tutorial").prop("checked")) {
    index += basicTutorialLimit;
  }
  $("#title").val("tuto-" + ("000" + index).slice(-4));
}
function markAsMoved() {
  $("#state").val("moved");
};
function markAsReady() {
  $("#geoTab").css("display", "inline");
  $('#downloadButton').css('display', 'inline-block');
  $("#state").val("ready");
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
            };
          });
          break;
        default:
          elt.val(object.value);
      }
    });
  }
}

var longClickTimeout = null;
var currentPopup = null;

function startCountdown(element) {
  longClickTimeout = setTimeout(function() { // When the timeout finally triggers,
    currentPopup = element.nextElementSibling;
    currentPopup.style.display = "block"; // show the popup menu.
    longClickTimeout = null;
  }, 500);
}
function stopCountdown(rewrite_operation) {
  if (longClickTimeout) { // If the timeout has not yet triggered,
    clearTimeout(longClickTimeout); // cancel it
    longClickTimeout = null;
    rewrite(rewrite_operation); // and call the default rewriting.
  }
}
function closePopup() {
  if (currentPopup) {
    currentPopup.style.display = "none";
  };
  currentPopup = null;
}
$(document).keypress(function (e) {
  if (e.which == 13 && e.target.nodeName != "TEXTAREA") {
    return false
  };
});
function make_editor_react_on_change(flag) {
  var editor = ace.edit("editor");
  if (flag) {
    editor.session.on('change', markAsDirty);
  } else {
    editor.session.off('change', markAsDirty);
  }
}
$().ready(function () {
  createTabs();
	var editor = ace.edit("editor");
  // if the hidden text area named "text" is not empty, use its content as the never_refreshed value of the editor
  var text = $('textarea[name="text"]').val();
  if (text) {
    editor.setValue(text);
    editor.selection.moveCursorFileStart();
    // get the current URL without the GET arguments
    var url = window.location.href.split('?')[0];
    // replace the current URL with the new URL without the GET arguments
    window.history.pushState({path: url}, '', url);  }
  else {
    // if it is launched from localhost, use the local pristine sandbox
    if (location.hostname == "localhost") {
      var pristine_sandbox = "/mocodo/mocodo/resources/pristine_sandbox.mcd";
    }
    else {
      var pristine_sandbox = "/resources/pristine_sandbox.mcd";
    }
  };
  $.get(location.protocol + '//' + location.host + pristine_sandbox, function (data) {
    editor.setValue(data);
    editor.selection.moveCursorFileStart();
  });
  editor.session.on('change', markAsDirty);
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
  var items = Object.keys(delays).map(function (key) { return { "value": delays[key], "name": key } });
  items.sort(function (a, b) { return a["value"] - b["value"] });
  createOptions("delays", items.map(function (value, index) { return value["name"] }), "1 minute");
  items = Object.keys(flex).map(function (key) { return { "value": flex[key], "name": key } });
  items.sort(function (a, b) { return a["value"] - b["value"] });
  createOptions("flex", items.map(function (value, index) { return value["name"] }), "normale");
  createCheckboxes(conversions, "conversions");
  createCheckboxes(knowledge, "knowledge");
  readCookie();
  setTutorialKnowledge($("#full_tutorial").prop("checked"))
  setDecompositionKnowledge($("#decomposition").prop("checked"));
  setRandomKnowledge($("#random").prop("checked"));
  setClusterKnowledge($("#cluster").prop("checked"));
  setConversionKnowledge($("#all_conversions").prop("checked"));
  $("#basic").prop("checked", true);
  $("#basic").prop("disabled", true);
});
