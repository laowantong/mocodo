<?php
	$filename = $_POST["archiveName"];
	header("Content-type: application/octet-stream");
	header("Content-disposition: attachment; filename=\"{$filename}\"");
	readfile($_POST["path"] . "/" . $filename);
	exit();
?>
