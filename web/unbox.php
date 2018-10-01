<?php
session_start();
// $php_log = fopen("php.log", 'w') or die("can't open file");
// fwrite($php_log, "Log file\n");
if (!array_key_exists('title', $_POST)) {
    exit("Need a POST value.");
}

// Make a folder for this user
$path = str_replace(":", "_", "sessions/" . $_SERVER['REMOTE_ADDR'] . "-" . session_id()) ; // prevent the automatic substitution of : by / on Mac OS X (IPV6 syntax)
file_exists($path) or mkdir($path) or die('{"err": "PHP: Failed to create user folder."}');
chdir($path);

// Retrieve the MCD text file
$title = preg_replace("/[^- _a-zA-Z0-9.]/","",$_POST['title']); # double-check js validation
$title = preg_replace("/^ *$/","Sans titre",$title); # double-check js validation
$title = preg_replace("/\.mcd$/","",$title); # suppress optional .mcd extension
$filename = "../../box/{$title}.mcd";
if (file_exists($filename)) {
	$contents = file_get_contents("../../box/{$title}.mcd") or die('');
} else {
	$contents = '';
}
echo $contents;
?>