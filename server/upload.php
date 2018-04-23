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

// Checks
if (
    // Secret
    password_verify($_POST['secret'], $config['secretBcrypt']) &&
    // Single file upload
    isset($screenshot['error']) &&
    !is_array($screenshot['error']) &&
    $screenshot['error'] === UPLOAD_ERR_OK &&
    // Size
    $screenshot['size'] <= $config['maxScreenshotSize'] &&
    // MIME type
    mime_content_type($screenshot['tmp_name']) === 'image/png'
) {
    // Get screenshot path
    do {} while (
        file_exists($filename = bin2hex(
                function_exists('random_bytes') ? random_bytes(12) : openssl_random_pseudo_bytes(12)
            ) . '.png'
        )
    );
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
