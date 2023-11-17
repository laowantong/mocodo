<?php

session_start();
// $php_log = fopen("php.log", 'w') or die("can't open file");
// fwrite($php_log, "Log file\n");
// ini_set('display_errors', 1);
// ini_set('display_startup_errors', 1);
// error_reporting(E_ALL);
if (!array_key_exists('title', $_POST)) {
    exit("Need a POST value.");
}

// Make a folder for this user
$path = str_replace(":", "_", "sessions/" . $_SERVER['REMOTE_ADDR'] . "-" . session_id()) ; // prevent the automatic substitution of : by / on Mac OS X (IPV6 syntax)
file_exists($path) or mkdir($path) or die('{"err": "PHP: Failed to create user folder."}');
chdir($path);

// Double-check js validation
$title = preg_replace("/[^- _a-zA-Z0-9.]/","",$_POST['title']);
$title = preg_replace("/^ *$/","Sans titre",$title);
$title = preg_replace("/\.mcd$/","",$title);

// Disable SSL verification
stream_context_set_default([
	'ssl' => [
	  'verify_peer' => false,
	  'verify_peer_name' => false,
	],
  ]);

// Try to get the file from the lib url provided by the user
$mcd_url = $_POST['lib'] . "/{$title}.mcd";
$contents = file_get_contents($mcd_url) or "";

// If the file is not found, try to get it from mocodo.net
if ($contents == "") {
	$mcd_url = "https://mocodo.net/web/lib/{$title}.mcd";
	$contents = file_get_contents($mcd_url) or "";
};

echo $contents;
?>
