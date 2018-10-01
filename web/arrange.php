<?php
session_start();
// $php_log = fopen("php.log", 'w') or die("can't open file");
// fwrite($php_log, "Log file\n");
if (!array_key_exists('text', $_POST)) {
    exit("Need a POST value.");
}

// Make a folder for this user
$path = str_replace(":", "_", "sessions/" . $_SERVER['REMOTE_ADDR'] . "-" . session_id()) ; // prevent the automatic substitution of : by / on Mac OS X (IPV6 syntax)
file_exists($path) or mkdir($path) or die('{"err": "PHP: Failed to create user folder."}');
chdir($path);

// Create the MCD text file
$title = preg_replace("/[^- _a-zA-Z0-9.]/","",$_POST['title']); # double-check js validation
$title = preg_replace("/^ *$/","Sans titre",$title); # double-check js validation
$_POST['input'] = "{$title}.mcd";
$chan = fopen($_POST['input'], 'w') or die('{"err": "PHP: Can\'t open MCD file."}');
$_POST['text'] = str_replace('"','',$_POST['text']); # double-check js validation
$_POST['text'] = str_replace('`','',$_POST['text']); # double-check js validation
$_POST['text'] = str_replace("\\'","'",$_POST['text']); # disable http://en.wikipedia.org/wiki/Magic_quotes
fwrite($chan, $_POST['text']);
fclose($chan);

// Prepare the contents of the options file
unset($_POST['text']);
unset($_POST['state']);
$_POST["guess_title"] = ($_POST["guess_title"] == "true");
$_POST['extract'] = TRUE;
$_POST['image_format'] = 'svg';
$_POST['language'] = 'fr';
$_POST['encodings'] = array("utf8");
$_POST['title'] = $title;

// Write it
$chan = fopen("params.json", 'w') or die('{"err": "PHP: Can\'t open \'params.json\' file."}');
fwrite($chan, json_encode($_POST));
fclose($chan);

// Launch the script
$command_line = "python ../../../mocodo.py --timeout=" . $_POST['timeout'] . " --" . $_POST['algo'];
// fwrite($php_log, $command_line . "\n");
// fwrite($php_log,$_POST['text']);
// fclose($php_log);
$out = array();
exec($command_line, $out);

// return the response
echo implode("\n", $out);
?>