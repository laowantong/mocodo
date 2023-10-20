<?php
// Remove the old sessions' subdirectories
$session_dir = __DIR__ . "/sessions";
if (file_exists($session_dir)) {
  $files = glob("{$session_dir}/*");
  foreach ($files as $file) {
    if (is_dir($file) && (time() - filemtime($file) > 24*60*60)) {
      $files2 = glob("{$file}/*");
      foreach ($files2 as $file2) {
        if (is_file($file2)) {
          unlink($file2);
        };
      };
      rmdir($file);
    };
  };
};
?>
