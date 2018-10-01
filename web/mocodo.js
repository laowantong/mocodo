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
    "diagram": {
      "default": false,
      "highlighting": "none",
      "title": "Résultat à réinjecter sous l&#39;onglet Entrée pour tracer un diagramme sagittal des relations.",
      "name": "Diagramme relationnel",
    },
    "markdown_data_dict": {
      "default": false,
      "highlighting": "none",
      "title": "Option placée ici par commodité: un dictionnaire des données n&#39;a rien à voir avec un schéma relationnel.",
      "name": "Dictionnaire des données (Markdown)",
    },
    "html_verbose": {
      "default": false,
      "highlighting": "markup",
      "title": "S&#39;affiche également au-dessous du diagramme conceptuel.",
      "name": "Explications du schéma relationnel",
    },
    "html": {
      "default": true,
      "highlighting": "markup",
      "title": "S&#39;affiche également au-dessous du diagramme conceptuel.",
      "name": "HTML",
    },
    // "json": {
    //   "default": false,
    //   "highlighting": "json",
    //   "name": 'JSON',
    // },
    "latex": {
      "default": false,
      "highlighting": "latex",
      "name": '<span style="font-family: serif; font-style: normal; margin-right: -.7em;">L<span style="font-size: 0.9em; position: relative; top: -.1em; left: -0.4em;">A</span><span style="position: relative; left: -.5em;">T</span><span style="position: relative; top: .2em; left: -.6em;">E</span><span style="position: relative; left: -.7em;">X</span></span>',
    },
    "markdown": {
      "default": false,
      "highlighting": "markdown",
      "name": "Markdown",
    },
    // "markdown_verbose": {
    //   "default": false,
    //   "highlighting": "markdown",
    //   "name": "Markdown avec explications",
    // },
    "text": {
      "default": false,
      "highlighting": "none",
      "name": "Texte brut",
    },
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
function createOptions(id,items,selected) {
  $.each(items, function (i, elt) {
    $("#" + id).append("<option" + (elt === selected?" selected='selected'":"") + ">" + elt + "<\/option>");
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
      '<input value="' + geo.size[0] + '" type="text" onfocus="markAsMoved()" name="size_x" id="size_x" min="0"\/> ' +
      '<input value="' + geo.size[1] + '" type="text" onfocus="markAsMoved()" name="size_y" id="size_y" min="0"\/> ' +
      '<\/div>';
  $("#size").html(s);
}
function refreshCoordinates(geo) {
  var s = ''
  $.each(geo["cx"],function (i,itemx) {
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
  $.each(geo["shift"],function (i,item) {
    s += '<div><label for="shift' + i + '">' + item[0] + '<\/label> <input value="' + item[1] + '" type="text"  onfocus="markAsMoved()" name="shift' + i + '" id="shift' + i + '"\/><\/div>';
  });
  $("#cards").html(s);
}
function refreshArrows(geo) {
  var s = '';
  $.each(geo["ratio"],function (i,item) {
    s += '<div><label for="ratio' + i + '">' + item[0] + '<\/label> <input value="' + item[1] + '" type="text"  onfocus="markAsMoved()" name="ratio' + i + '" id="ratio' + i + '"\/><\/div>';
  });
  $("#arrows").html(s);
}
function refreshDiagram(result) {
  $("#diagramOutput").html(result["svg"]);
}
function refreshRelations(result) {
  var s = '';
  var supplement = '';
  $.each(result["mld"],function (i, item) {
    s += '<fieldset class="listing"><legend>' + relation_formats[item[0]]["name"] + '<\/legend><pre><code class="language-' + relation_formats[item[0]]["highlighting"] + '">' + item[1] + '</code><\/pre><\/fieldset>';
    if ((item[0]=="html" && !supplement) || item[0]=="html_verbose") {
      supplement = item[1].replace(new RegExp("&lt;","g"),"<")
    };
  })
  $("#relationalOutput").html(s);
  $("#diagramOutputSupplement").html(supplement);
}
function preconditions() {
  if (request_lock) {
    return false
  }
  if (/[^- _a-zA-Z0-9.]/i.test($("#title").val())) {
    alert("Le titre du MCD ne peut contenir que des lettres non accentuées, des chiffres, des espaces, des points et des tirets haut et bas.");
    return false
  }
  return true
}
function generate() {
  if (!preconditions()) return;
  request_lock = true
  $("#generateButton").addClass("fa-spin");
  $.ajax({
    type: "POST",
    url: "web/generate.php",
    data: $("#mainForm").serialize(),
    success: function (result) {
      result = jQuery.parseJSON(result);
      if (result.hasOwnProperty("err")) {
        var error_message = result["err"].replace("<","&lt;")
        $("#errorOutput").html("<pre>" + error_message + "</pre>");
        $("#errorTab").css("display","inline");
      } else {
        var geo = jQuery.parseJSON(result["geo"]);
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
          activateTab("#outputZone","#diagramTab");
        }
        $("#errorTab").fadeOut();
        markAsReady();
        $("#downloadButton").fadeIn()
      }
    },
    complete: function(data) {
      $("#generateButton").removeClass("fa-spin");
      request_lock = false;
    }
  });
};
function arrange(event, algo) {
  if (!preconditions()) return;
  var request_lock = true
  if (algo == "fit=0") {
    algo = "arrange=bb"
  }
  else if (algo == "arrange=bb") {
    if (event.altKey) {
      algo = 'arrange=bb --organic';
    }
    else if (!event.shiftKey) {
      algo = 'fit=0'
    }
  }
  $("#gear").addClass("fa-spin");
  $("#text").addClass("flash");
  $.ajax({
    type: "POST",
    url: "web/arrange.php",
    data: {
      algo: algo,
      text: $("#text").attr("value"),
      timeout: delays[$("#delays").attr("value")]
    },
    success: function (result) {
      $("#text").val(result);
      $("#text").scrollTop(0);
      markAsDirty();
      if (algo == 'fit=0') {
        arrange(event, algo);
      }
      else if (!$("#diagramOutput").hasClass('initial')) {
        request_lock = false;
        generate();
      }
    },
    complete: function(data) {
      $("#gear").removeClass("fa-spin");
      $("#text").removeClass("flash");
      request_lock = false;
    }
  });
};
function reveal(event) {
  if (!preconditions()) return;
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
    complete: function(data) {
      request_lock = false;
    }
  });
};
function markAsDirty() {
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
  $("#geoTab").css("display","inline");
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
    $.each(objects, function(index, object) {
      var elt = $('[name="'+object.name+'"]');
      switch(elt[0].type){
        case 'checkbox':
          elt.each(function() {
            if($(this).attr('value') == object.value) {
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
  $("#contact").html('<a href="3ai5to:&#'.replace('3','m').replace('5','l')+Array(109,111,99,111,100,111).join(";&#")+';@&#'+Array(119,105,110,103,105,46,110,101,116).join(";&#")+';">Contact<\/a>')
  createTabs();
  $.get("mocodo/pristine_sandbox.mcd", function (data) {$("#text").val(data)});
  var default_color = "brewer" + "+-"[Math.floor(Math.random() * 2)] + (Math.floor(Math.random() * 9) + 1);
  createOptions("colors",["blank","bw","desert","keepsake","mondrian","ocean","pond","wb","xinnian","brewer+1","brewer-1","brewer+2","brewer-2","brewer+3","brewer-3","brewer+4","brewer-4","brewer+5","brewer-5","brewer+6","brewer-6","brewer+7","brewer-7","brewer+8","brewer-8","brewer+9","brewer-9"],default_color);
  createOptions("shapes",["arial","copperplate","georgia","mondrian","sans","serif","times","trebuchet","verdana","xinnian"],"verdana");
  createOptions("disambiguation",["annotations et numéros", "numéros seulement"],"annotations et numéros");
  var items = Object.keys(delays).map(function (key) {return {"value": delays[key], "name": key}});
  items.sort(function(a,b) { return a["value"] - b["value"]});
  createOptions("delays",items.map(function (value, index) {return value["name"]}),"1 minute");
  items = Object.keys(flex).map(function (key) {return {"value": flex[key], "name": key}});
  items.sort(function(a,b) { return a["value"] - b["value"]});
  createOptions("flex",items.map(function (value, index) {return value["name"]}),"normale");
  createOptions("SQL_dialect",["", "MySQL","Oracle","PostgreSQL","SQLite"],"");
  createFormatCheckboxes();
  readCookie();
});
