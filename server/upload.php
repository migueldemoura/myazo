<?php

// Configuration
$config = array_replace_recursive(
    [
        'secretBcrypt' => '',
        'saveDirName' => '/data/',
        'maxScreenshotSize' => 2 * 1048576
    ],
    file_exists('./config.php') ? include_once('./config.php') : []
);

$baseUri = 'https://' . $_SERVER['HTTP_HOST'] . $config['saveDirName'];
$saveDir = __DIR__ . $config['saveDirName'];
$screenshot = $_FILES['screenshot'];

if (!password_verify($_POST['secret'], $config['secretBcrypt'])) {
    http_response_code(401);
    exit();
}

if (
    // Make sure it is a successful single file upload
    !isset($screenshot['error']) ||
    is_array($screenshot['error']) ||
    $screenshot['error'] !== UPLOAD_ERR_OK ||
    // Verify size and mime type
    $screenshot['size'] > $config['maxScreenshotSize'] ||
    mime_content_type($screenshot['tmp_name']) !== 'image/png'
) {
    http_response_code(422);
    exit();
}

// Generate screenshot path
do {} while (
    file_exists($filename = bin2hex(
            function_exists('random_bytes') ? random_bytes(12) : openssl_random_pseudo_bytes(12)
        ) . '.png'
    )
);

// Create save directory and move screenshot to it
if (
    (is_writable($saveDir) || mkdir($saveDir, 0755, true)) &&
    move_uploaded_file($screenshot['tmp_name'], $saveDir . $filename)
) {
    // Print uploaded screenshot url
    exit($baseUri . $filename);
} else {
    http_response_code(500);
    exit();
}
