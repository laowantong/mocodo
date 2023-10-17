<?php
session_start();
if (!array_key_exists('text', $_POST)) {
    exit("Need a POST value.");
}

// log all $_POST content
// $php_log = fopen("php.log", 'a') or die('{"err": "PHP: Can\'t open \'php.log\' file."}');
// fwrite($php_log, json_encode($_POST) . "\n");

if (strpos($_SERVER['HTTP_REFERER'], 'localhost')) {
  $mocodo = "~/opt/anaconda3/bin/mocodo";
  $web_url = "http://localhost:8898/mocodo/web/";
} else {
  $mocodo = "~/.local/bin/mocodo";
  $web_url = "https://www.mocodo.net/web/";
}

$transformations = array(
  "_url.url" => "url",
  "_data_dict_2.md" => "data_dict:label,type=_Description_",
  "_data_dict_3.md" => "data_dict",
  "_mld.html" => "html:e",
  "_mld.md" => "markdown",
  "_mld.txt" => "text",
  "_mld.mcd" => "diagram",
  "_mld_with_constraints.html" => "html:ce",
  "_mld_with_constraints.md" => "markdown:c",
  "_mld_with_constraints.txt" => "text:c",
  "_mld_with_constraints.mcd" => "diagram:c",
  "_dependencies.gv" => "dependencies",
  "_ddl.sql" => "sql",
  "_uml.puml" => "uml",
  "_ddl.dbml" => "dbml",
);


// Prevent the automatic substitution of : by / on Mac OS X (IPV6 syntax)
$user_path = "/sessions/" . str_replace(":", "_", $_SERVER['REMOTE_ADDR'] . "-" . session_id());
$local_path =  __DIR__ . $user_path;
// Make a folder for this user
file_exists($local_path) or mkdir($local_path) or die('{"err": "PHP: Failed to create user folder."}');
chdir($local_path); 

$postId = md5(serialize($_POST));

$title = preg_replace("/[^- _a-zA-Z0-9.]/","",$_POST['title']); # double-check js validation
$title = preg_replace("/^ *$/","Sans titre",$title); # double-check js validation
$_POST['input'] = "{$title}.mcd";

if ($_POST['png']) { $mocodo .= " --svg_to png"; };
if ($_POST['pdf']) { $mocodo .= " --svg_to pdf"; };

if ($_POST['state']=="moved") {
    $geo = json_decode(file_get_contents("{$title}_geo.json"),true);
    $geo['width'] = intval($_POST['width']);
    $geo['height'] = intval($_POST['height']);
    foreach ($geo["cx"] as $i => $value) {
      $geo["cx"][$i] = array($value[0],intval($_POST["cx".$i]));
      $geo["cy"][$i] = array($value[0],intval($_POST["cy".$i]));
    };
    foreach ($geo["shift"] as $i => $value) {
      $geo["shift"][$i] = array($value[0],floatval($_POST["shift".$i]));
    };
    foreach ($geo["ratio"] as $i => $value) {
      $geo["ratio"][$i] = array($value[0],floatval($_POST["ratio".$i]));
    };
    $chan = fopen("{$title}_geo.json", 'w') or die('{"err": "PHP: Can\'t open geo file."}');
    fwrite($chan, json_encode($geo, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    fclose($chan);
    $mocodo .= " --reuse_geo";
}
else {
    // Clean the directory up
    foreach (glob("*.*") as $filename) {
      unlink($filename);
    };
    // Create the MCD text file
    $chan = fopen($_POST['input'], 'w') or die('{"err": "PHP: Can\'t open MCD file."}');
    $_POST['text'] = str_replace('"','',$_POST['text']); # double-check js validation
    $_POST['text'] = str_replace('`','',$_POST['text']); # double-check js validation
    $_POST['text'] = str_replace("\\'","'",$_POST['text']); # disable http://en.wikipedia.org/wiki/Magic_quotes
    fwrite($chan, $_POST['text']);
    fclose($chan);

    // Prepare the contents of the options file
    unset($_POST['text']);
    unset($_POST['state']);
    $_POST['language'] = 'fr';
    $_POST['encodings'] = array("utf8");

    // Write it
    $chan = fopen("params.json", 'w') or die('{"err": "PHP: Can\'t open \'params.json\' file."}');
    fwrite($chan, json_encode($_POST));
    fclose($chan);
  };

if ($_POST['conversions']) {
  $transformation_options = "";
  $conversions = array();
  foreach ($_POST['conversions'] as $ext) {
    if ($ext == "_ddl.sql") {
      $transformation_options .= " " . $_POST['sql_case'] . ":labels";
    }
    if ($_POST['with_constraints']) {
      $option = $transformations[str_replace("_mld", "_mld_with_constraints", $ext)];
    } else {
      $option = $transformations[$ext];
    }
    $transformation_options .= " " . $option;
    $conversions[] = $ext;
  };
  $mocodo .= " -t{$transformation_options}";
};

// Launch the script

$out = array();
$command_line = "{$mocodo} 2>&1 >/dev/null";
// fwrite($php_log, $command_line . "\n");
exec($command_line, $out);

if (!empty($out)) {
    echo json_encode(array("err" => implode("\n",$out)));
    exit();
};

// make the archive
$zipName = iconv('UTF-8', 'ASCII//TRANSLIT', $title);
$zipName = str_replace("'", "", $zipName) . ".zip";
$zip = new ZipArchive();
if ($zip->open($zipName, ZIPARCHIVE::CREATE)!==TRUE) {
    die('{"err": "PHP: Can\'t open <{$zipName}>\n"}');
};

$zip->addFile("{$title}_geo.json");
$zip->addFile("{$title}.mcd");
$zip->addFile("{$title}.svg");
// The following instructions fail silently if the (optional) files do not exist
$zip->addFile("{$title}_static.svg");
$zip->addFile("{$title}.png");
$zip->addFile("{$title}.pdf");
foreach ($conversions as $ext) {
  $zip->addFile("{$title}{$ext}");
};
$zip->close();

// return the response
$svg = file_get_contents("{$title}.svg");
$count = 1;
$curLocale = setlocale(LC_ALL, 0); //gets current locale
setlocale(LC_ALL, "en_US.utf8"); //without this iconv removes accented letters. If you use another locale it will also fail
setlocale(LC_ALL, $curLocale); //set locale to what it was before   

$result = array(
    "svg" => str_replace('stroke="none" stroke-width="0"', 'stroke="#808080" stroke-width="1" stroke-dasharray="2,2"', $svg, $count),
    "geo" => file_get_contents("{$title}_geo.json"),
    "zipName" => $zipName,
    "zipURL" => $web_url . $user_path . "/" . $zipName,
    "conversions" => array(),
    "title" => $title,
);
foreach ($conversions as $ext) {
    $str = file_get_contents("{$title}{$ext}");
    $str = str_replace('<','&lt;', $str);
    $result["conversions"][] = array($ext, $str);
};
// fwrite($php_log, json_encode($result) . "\n");
echo json_encode($result);
?>
