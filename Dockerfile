FROM webdevops/php-nginx:alpine-php7

COPY server /app
ENV WEB_DOCUMENT_INDEX=upload.php
