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
  "diagram": {
    "default": false,
    "highlighting": "none",
    "title": "Résultat à réinjecter sous l&#39;onglet Entrée pour tracer un diagramme sagittal des relations.",
    "name": "Diagramme relationnel",
  },
  "html_verbose": {
    "default": true,
    "highlighting": "markup",
    "title": "S&#39;affiche également au-dessous du diagramme conceptuel.",
    "name": "Explications du schéma relationnel",
  },
  // "json": {
  //   "default": false,
  //   "highlighting": "json",
  //   "name": 'JSON',
  // },
  // "markdown_verbose": {
  //   "default": false,
  //   "highlighting": "markdown",
  //   "name": "Markdown avec explications",
  // },
  // "txt2tags": {
  //   "default": false,
  //   "highlighting": "none",
  //   "name": "txt2tags",
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
    if (item[0] == "html_verbose") {
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
      navigator.clipboard.writeText(code.innerText);
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
    $("#text").addClass("flash");
    return $.ajax({
      type: "POST",
      url: "web/arrange.php",
      data: {
        algo: algo,
        text: $("#text").attr("value"),
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
        $("#text").val(result["text"]);
        $("#text").scrollTop(0);
        markAsDirty();
        if (!$("#diagramOutput").hasClass('initial') & algo!="fit=0" & algo!="fit=1") {
          request_lock = false;
          generate();
        }
      },
      complete: function (data) {
        $("#gear").removeClass("fa-spin");
        $("#text").removeClass("flash");
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
function reveal(event) {
  if (request_lock) return;
  request_lock = true
  $.ajax({
    type: "POST",
    url: "web/unbox.php",
    data: { title: $("#title").attr("value") },
    success: function (result) {
      if (result) {
        $("#text").val(result);
        $("#text").scrollTop(0);
        markAsDirty();
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
function markAsDirty() {
  $("#title").val($("#title").attr("value").replace(/[^A-Za-zÀ-ÖØ-öø-ÿ0-9 '\._-]/g, '-'));
  $("#state").val("dirty");
  $("#geoTab").fadeOut();
  $("#downloadButton").fadeOut();
};
function freezeTitle() {
  $("#guess_title").val($("#title").attr("value") == "" || $("#title").attr("value") == "Sans Titre");
};
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
  $("#contact").html('<a href="3ai5to:&#'.replace('3', 'm').replace('5', 'l') + Array(109, 111, 99, 111, 100, 111).join(";&#") + ';@&#' + Array(119, 105, 110, 103, 105, 46, 110, 101, 116).join(";&#") + ';">Contact<\/a>')
  createTabs();
  $.get("mocodo/resources/pristine_sandbox.mcd", function (data) { $("#text").val(data) });
  var default_color = "brewer" + "+-"[Math.floor(Math.random() * 2)] + (Math.floor(Math.random() * 9) + 1);
  createOptions("colors", ["blank", "bw", "desert", "keepsake", "mondrian", "ocean", "pond", "wb", "xinnian", "brewer+1", "brewer-1", "brewer+2", "brewer-2", "brewer+3", "brewer-3", "brewer+4", "brewer-4", "brewer+5", "brewer-5", "brewer+6", "brewer-6", "brewer+7", "brewer-7", "brewer+8", "brewer-8", "brewer+9", "brewer-9"], default_color);
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
});
