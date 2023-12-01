<?php

$b64 = array();

foreach(glob("*.png") as $file) {
	$b64[pathinfo($file, PATHINFO_FILENAME)] = "{background-image:url(data:image/png;base64," . base64_encode(file_get_contents($file)) . ");}";
}

$b64 = json_encode($b64, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
// $fp = fopen("icons.json", "w");
file_put_contents("icons2.json", $b64);
// fclose($fp);