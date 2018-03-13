<?php

// Settings
$secretBcrypt = '';

$baseUri = 'https://' . $_SERVER['HTTP_HOST'] . '/data/';
$saveDir = __DIR__ . '/data/';
$screenshot = $_FILES['screenshot'];

// Checks
if (
    // Secret
    password_verify($_GET['s'], $secretBcrypt) &&
    // Single file upload
    isset($screenshot['error']) &&
    !is_array($screenshot['error']) &&
    $screenshot['error'] === UPLOAD_ERR_OK &&
    // Size
    $screenshot['size'] <= 2 * 1048576 &&
    // MIME type
    mime_content_type($screenshot['tmp_name']) === 'image/png'
) {
    // Get screenshot path
    do {} while (file_exists($filename = bin2hex(random_bytes(12)) . '.png'));
    if (
        // Create save directory
        (is_writable($saveDir) || mkdir($saveDir, 0755, true)) &&
        move_uploaded_file($screenshot['tmp_name'], $saveDir . $filename)
    ) {
        // Print uploaded screenshot url
        exit($baseUri . $filename);
    }
}

exit($baseUri . 'error.png');
