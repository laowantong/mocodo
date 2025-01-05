/*global $, jQuery*/
'use strict';
const openInNewTab = (href) => {
  const a = document.createElement("a");
  a.target = "_blank";
  a.rel = "noopener noreferrer";
  a.href = href;
  a.style.display = "none";
  document.body.appendChild(a); // Append the link to the document
  a.click(); // Programmatically click the link
  document.body.removeChild(a); // Remove the link after clicking
};
const basthon_template = JSON.stringify({
  cells: [
    {
      metadata: { trusted: true },
      cell_type: "code",
      source: "from mocodo.magic import mocodo",
      execution_count: null,
      outputs: [],
    },
    {
      metadata: { trusted: true },
      cell_type: "code",
      source: 'mocodo("""\n%%mocodo {options}\n{source}\n""")',
      execution_count: null,
      outputs: [],
    },
  ],
  metadata: {
    kernelspec: {
      name: "python3",
      display_name: "Python 3",
      language: "python",
    },
  },
  nbformat: 4,
  nbformat_minor: 2,
});
var request_lock = false;
var conversions = {
  "_url.url": {
    "default": true,
    "highlighting": "none",
    "title": "URL d&#39;une session Mocodo online pré-remplie avec le texte-source de votre MCD.",
    "name": "Lien de partage du MCD",
  },
  "_mld.mcd": {
    "default": false,
    "highlighting": "none",
    "title": "Résultat à réinjecter sous l&#39;onglet Entrée pour tracer un diagramme sagittal des relations.",
    "name": "Diagramme relationnel en Mocodo, clés étrangères&nbsp;&nbsp;",
  },
  "_mld.html": {
    "default": false,
    "highlighting": "markup",
    "title": "Affiché également au-dessous du diagramme conceptuel. Cliquez sur un schéma de relation pour faire apparaître une explication du passage du MCD au MLD.",
    "name": "Schéma relationnel expliqué",
  },
  "_ddl.sql": {
    "default": false,
    "highlighting": "sql",
    "title": "DDL œcuménique, pour peu que vous utilisiez les types requis par le dialecte-cible (MySQL, SQLite, PostgreSQL, Oracle, SQL Server, etc.). Les libellés sont automatiquement privés de leurs accents et espaces pour éviter de polluer le code SQL avec des délimiteurs de chaînes, qui plus est non portables.",
    "name": "Script SQL de création des tables, libellés en&nbsp;&nbsp;",
  },
  "_data_dict_2.md": {
    "default": false,
    "highlighting": "markdown",
    "title": "Colonnes : attribut / descriptif.",
    "name": "Dictionnaire des données sur deux colonnes",
    "advanced": true,
  },
  "_data_dict_3.md": {
    "default": false,
    "highlighting": "markdown",
    "title": "Colonnes : entité ou association / attribut / type.",
    "name": "Dictionnaire des données sur trois colonnes",
    "advanced": true,
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
  "advanced_tutorial": {
    "name": "Tutoriel (2/2)",
    "title": "Cochez pour remplacer la première partie du tutoriel par la seconde.",
    "default": false,
    "onchange": "setTutorialKnowledge(event.target.checked)",
  },
  "weak": {
    "name": "Entité faible (ou identification relative), cardinalités notées&nbsp;&nbsp;",
    "title": "Cochez pour inclure des entités faibles dans les MCD aléatoires et certaines opérations de décomposition. Une entité faible est une entité dont l&#39;identifiant nécessite d&#39;être renforcé par une ou plusieurs entités dont elle dépend fonctionnellement. NB : laisser cette option non cochée ne vous empêchera pas de créer vous-même des entités faibles.",
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
  "assoc_ids": {
    "name": "Autoriser les identifiants supplémentaires dans les associations",
    "title": "Cochez pour activer cette possibilité, non prévue par Merise, mais qui permet dans certains cas de produire un même schéma relationnel à partir d&#39un schéma conceptuel plus simple.",
    "default": false
  },
  "reproductibility": {
    "name": "Reproductibilité des tirages pseudo-aléatoires",
    "title": "Cochez pour que la longueur de la première ligne du texte-source soit prise comme germe du générateur pseudo-aléatoire. Ainsi, les algorithmes randomisés produiront toujours la même sortie sur un même texte-source.",
    "default": false
  },
  "random": {
    "name": "Masquage et génération aléatoire",
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
    s = "<li>";
    s += '<span><input type="checkbox" name="' + group_name + '[]" id=' + key + ' value="' + key + '"';
    if (value["default"]) { s += " checked='checked'" };
    s += " onchange='markAsDirty();writeCookie()"
    if (value["onchange"]) { s += ";" + value["onchange"] }
    s += "'\/> <label for='" + key + "'";
    if (value["title"]) { s += " title='" + value["title"] + "'" };
    s += ">" + value["name"] + "<\/label><\/span><\/li>";
    if (value["advanced"]) {
      $("#" + group_name).find("details").append(s);
    } else {
      if ($("#" + group_name).find("details").length) {
        $("#" + group_name).find("details").before(s);
      } else {
        $("#" + group_name).append(s);
      }
    }
  })
}
function appendMenuToInput(menuId, inputId) {
  document.getElementById(inputId).parentNode.appendChild(document.getElementById(menuId));
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
    name = conversions[item[0]]["name"].replace(/,.*$/, "");
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
};
function sendToBasthon() {
  var text = ace.edit("editor").getSession().getValue();
  $('textarea[name="text"]').val(text);
  var data = $("#mainForm").serializeArray();
  data.push({ name: "basthon", value: true });
  if ($("#reproductibility").prop("checked")) {
    data.push({ name: "seed", value: text.indexOf("\n") });
  };
  if ($("#constraints").prop("checked")) {
    data.push({ name: "with_constraints", value: true })
  };
  $.ajax({
    type: "POST",
    url: "web/generate.php",
    data: $.param(data),
    success: function (result) {
      result = $.parseJSON(result);
      let ipynb = basthon_template;
      // if the source consists in only blank characters, replace %%mocodo by %mocodo
      if (/^\s*$/.test(result["source"])) {
        ipynb = ipynb.replace("%%mocodo", "%mocodo");
      }
      ipynb = ipynb.replace("{options}", result["options"]);
      ipynb = ipynb.replace("{source}", result["source"].replaceAll("\r", "").replaceAll("\n", "\\n"));
      ipynb = encodeURIComponent(ipynb);
      const url = new URL("https://notebook.basthon.fr");
      url.searchParams.set("ipynb", ipynb);
      openInNewTab(url.href);
    },
  });
};
function generate() {
  if (request_lock) return;
  request_lock = true;
  $("#refreshButton").hide();
  $("#rotatingButton").show();
  var text = ace.edit("editor").getSession().getValue();
  $('textarea[name="text"]').val(text);
  var data = $("#mainForm").serializeArray();
  if ($("#reproductibility").prop("checked")) {
    data.push({ name: "seed", value: text.indexOf("\n") });
  };
  if ($("#constraints").prop("checked")) {
    data.push({ name: "with_constraints", value: true })
  };
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
      // suppress the sessions older than 24 hours
      $.ajax({
        type: "POST",
        url: "web/purge.php",
        data: {}
      });
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
      args = args.replace("arrange,", "arrange:");
    }
    if (args.includes("explode")) {
      args = $("#weak").prop("checked") ? args.replace(":", ":weak,") : args.replace("weak,", "");
    };
    if (args.includes("grow")) {
      args = $("#weak").prop("checked") ? args.replace(":", ":_11-*N=1,") : args.replace("_11-*N=1,", "");
      args = $("#cluster").prop("checked") ? args.replace(":", ":/*N-*N=1,") : args.replace("/*N-*N=1,", "");
    };
    var text = ace.edit("editor").getSession().getValue();
    $('textarea[name="text"]').val(text);
    if ($("#reproductibility").prop("checked")) {
      args += " --seed=" + text.indexOf("\n");
    }
    return $.ajax({
      type: "POST",
      url: "web/rewrite.php",
      data: {
        args: args,
        text: text
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
        request_lock = false;
        generate();
      },
      complete: function (data) {
        $("#refreshButton").show();
        $("#rotatingButton").hide();
        $("#editor").removeClass("flash");
        request_lock = false;
      }
    });
  };
function get_from_lib() {
  if (request_lock) return;
  request_lock = true
  $.ajax({
    type: "POST",
    url: "web/get_from_lib.php",
    data: {
      title: $("#title").val(),
      lib: $("#lib").val(),
    },
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
function setPulsatingButton(is_visible, checkbox, button) {
  if (is_visible) {
    button.show().css("opacity", "1");
    checkbox.off("mouseenter");
    checkbox.off("mouseleave");
    button.removeClass("pulsating");
   } else {
    button.hide();
    button.addClass("pulsating");
    checkbox.on("mouseenter", function () { button.show(); });
    checkbox.on("mouseleave", function () { button.hide(); });
   }
};
function setDecompositionKnowledge(is_visible) {
  setPulsatingButton(is_visible, $("#decomposition").parent(), $("#explodeButton"));
};
function setRandomKnowledge(is_visible) {
  setPulsatingButton(is_visible, $("#random").parent(), $("#jokerButton"));
};
function setClusterKnowledge(is_visible) {
  is_visible ? $("#createCifs").show() : $("#createCifs").hide();
};
function setButtonPreviewOnHover(checkboxId, buttonId) {
  $('label[for="' + checkboxId + '"]').hover(function() {
    if ($("#" + checkboxId).prop("checked", false)) {
      $('#' + buttonId).fadeTo(500, 0.5);
    }
  }, function() {
    if ($("#" + checkboxId).prop("checked", false)) {
      $('#' + buttonId).hide();
    }
  });
}
var tutorialOptions = ["Tutoriel interactif (1/2)", "Entité", "Identifiant et attributs d'entité", "Identifiant composite", "Association", "Cardinalités", "Attribut d'association", "Association de dépendance fonctionnelle", "Association réflexive", "Schéma relationnel", "Rôles", "Diagramme relationnel (1)", "Diagramme relationnel (2)", "Inférence de types", "Génération du DDL", "Schéma sur plusieurs rangées", "Réarrangement automatique", "Réarrangement automatique avec contraintes", "Entraînement au passage au relationnel", "Pour aller plus loin...", "Tutoriel interactif (2/2)", "Entité faible (ou identification relative)", "Entité faible sans identifiant", "Identifiants candidats", "Héritage (ou spécialisation)", "Agrégation (ou pseudo-entité)", "Agrégation et contraintes d'unicité", "Agrégation multiple", "Contrainte d'intégrité fonctionnelle (CIF)", "Autres contraintes sur associations", "Explication interactive d'une contrainte", "Explication interactive des cardinalités", "Flèche sur une patte", "Dévoilement progressif du schéma", "Boîtes homonymes", "Vue en extension", "Décomposition des associations ternaires (1)", "Décomposition des associations ternaires (2)", "Pour aller plus loin..."];
var basicTutorialLimit = 20;
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
  $("#geoTab").fadeOut();
  $("#downloadButton").fadeOut();
  $("#state").val("dirty");
};
function changeTitleToNthTuto() {
  var index = $("select[id='tutorial'] option:selected").index();
  if ($("#advanced_tutorial").prop("checked")) {
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

var clickTimer = null;
var currentPopup = null;

function handleClick(element, rewrite_operation) {
  if (clickTimer != null) { // a double-click: call the default rewriting and close the popup menu if needed.
    if (currentPopup) {
      currentPopup.style.display = "none";
      currentPopup = null;
    };
    clearTimeout(clickTimer);
    clickTimer = null;
    rewrite(rewrite_operation);
  } else { // may be a simple click: if eventually so, switch the popup menu visibility.
    clickTimer = setTimeout(function () {
      clickTimer = null;
      if (currentPopup) {
        currentPopup.style.display = "none";
        currentPopup = null;
      } else {
        currentPopup = element.nextElementSibling;
        currentPopup.style.display = "block";
      }
    }, 350);
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
  }
  else {
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
  };
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
  createOptions("colors", ["blank", "bw", "bw-alpha", "desert", "dark", "dark-desert", "dark-ocean", "dark-pond", "keepsake", "mondrian", "ocean", "pond", "wb", "xinnian", "brewer+1", "brewer-1", "brewer+2", "brewer-2", "brewer+3", "brewer-3", "brewer+4", "brewer-4", "brewer+5", "brewer-5", "brewer+6", "brewer-6", "brewer+7", "brewer-7", "brewer+8", "brewer-8", "brewer+9", "brewer-9"], default_color);
  createOptions("shapes", ["arial", "copperplate", "georgia", "mondrian", "sans", "serif", "times", "trebuchet", "verdana", "xinnian"], "verdana");
  createCheckboxes(conversions, "conversions");
  createCheckboxes(knowledge, "knowledge");
  appendMenuToInput("sql_case", "_ddl.sql");
  appendMenuToInput("fk_format", "_mld.mcd");
  appendMenuToInput("strengthen_card", "weak");
  readCookie();
  setTutorialKnowledge($("#advanced_tutorial").prop("checked"))
  setDecompositionKnowledge($("#decomposition").prop("checked"));
  setRandomKnowledge($("#random").prop("checked"));
  setClusterKnowledge($("#cluster").prop("checked"));
  $("#basic").prop("checked", true);
  $("#basic").prop("disabled", true);
});
