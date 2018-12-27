<?php

$file = new CURLFile('/srv/downloads/ml-datasets/test-images/me_laugh.jpg');
$data = ['file' => $file];

$ch = curl_init('http://localhost');

curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_PORT, 10080);
curl_setopt($ch, CURLOPT_SAFE_UPLOAD, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
$result = curl_exec($ch);
curl_close($ch);

var_dump($result);
