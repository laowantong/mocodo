<?php
session_start();

// $php_log = fopen("php.log", 'w') or die("can't open file");

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
$_POST['language'] = 'fr';
$_POST['encodings'] = array("utf8");
$_POST['title'] = $title;

// Write it
$chan = fopen("params.json", 'w') or die('{"err": "PHP: Can\'t open \'params.json\' file."}');
fwrite($chan, json_encode($_POST));
fclose($chan);

// Launch the script

if (strpos($_SERVER['HTTP_REFERER'], 'localhost')) {
    $mocodo = "~/opt/anaconda3/bin/mocodo";
  } else {
    $mocodo = "~/.local/bin/mocodo";
};
$command_line = "{$mocodo} -t " . escapeshellcmd($_POST['args']) . " 2>&1";

// Execute the command and test the exit code.
// If it is not 0, return an array with a key "err" and the error message.

$out = array();
exec($command_line, $out, $exitCode);
if ($exitCode) {
    echo json_encode(array("err" => implode("\n", $out)));
    exit();
}

// Otherwise, retrieve the updated input file and return it
// in an array with a key "text".

$chan = fopen($_POST['input'], 'r') or die('{"err": "PHP: Can\'t open MCD file."}');
$contents = fread($chan, filesize($_POST['input']));

echo json_encode(array("text" => $contents));

?>