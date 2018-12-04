# Myazo

![Demo](https://raw.githubusercontent.com/migueldemoura/myazo/master/demo.gif)

Myazo is a self-hosted [Gyazo] alternative. It allows you to take a screenshot of part of your screen and automatically upload it to your own server.

It is comprised by a cross-platform client in Python which defers the actual taking of screenshot to OS built-in tools (macOS and Windows) or common utilities (GNU/Linux distributions). The server script, designed with cheap shared hosting in mind, is written with the ubiquitous PHP. Both the client and server are single files. You may separate the settings from the code if you wish.

It can also function as a mere Gyazo client, uploading directly to Gyazo's servers. In that case, you simply need the client and to set the configuration option `gyazo_server` to `True`. This mode won't send additional metadata like the Gyazo proprietary clients.

## Compatibility

### Client

* Python >= 3.5 (check with `python --version`)

The following OSes have off-the-shelf compatibility. You can add more back ends for missing systems or configurations.

* GNU/Linux (presets for `gnome-screenshot`, `xfce4-screenshooter`, `spectacle`, `scrot` and `import` (ImageMagick))
* macOS
* Windows 10 >= 1703 Creators Update (check with `winver` - Build >= 10.0.15063.251)

### Server

* PHP >= 5.6 (check with `php -v` or `php -r "echo phpinfo();"`)

## Installation

* Install [Python] 3 and choose the version matching your CPU arch (x86 or x86-64);
* Install client requirements:

```shell
pip install -r client/src/requirements.txt
```

On some GNU/Linux distributions, `pip3` is used for python3. If that's the case, swap `pip` with `pip3` in the command above.

* Choose or generate a secret key and fill in the variable `secret` at `client/src/myazo.py`;
* Hash the secret key with bcrypt and fill in the variable `secretBcrypt` at `server/src/upload.php`;
You can do so with PHP itself:

```shell
php -r "echo password_hash('yoursecrethere', PASSWORD_DEFAULT);"
```

If you don't have access to a php cli, create a `hash.php` file on your web server with `<?php file_put_contents(__FILE__, '<?php ' . password_hash('yoursecrethere', PASSWORD_DEFAULT));` and open it on your browser. Then, grab the hash from the `hash.php` source and delete the file.

* Upload `server/src/upload.php` to your web server;
* Disable directory listing so the list of uploaded screenshots isn't visible. For Apache, this can be done by uploading `server/src/.htaccess` to your web server's web root (or possibly any other directory, as long as it is a parent of the one where screenshots are stored).
* Enter the full public url of the `server/src/upload.php` script in the variable `upload_script` at `client/myazo.py`.

Alternatively, you may use the [Docker] and [Docker Compose] config files to deploy the server. Please note that you will need to configure HTTPS yourself.

## Configuration

There are two ways of configuring Myazo: either change the options in the scripts themselves, or use an external config file.

If an external file is found, Myazo extends the default config with the provided values. The following tables contain all options and where the user config file must be placed.

### Client

* Example Config: `client/src/config.ini.example`
* Placement Path: `~/.config/myazo/config.ini` (`~` refers to the user directory)

| Key                | Default                                | Description                                         |
|--------------------|----------------------------------------|-----------------------------------------------------|
| gyazo_server       | False                                  | Controls whether to use Gyazo's servers             |
| gyazo_direct_link  | True                                   | Controls whether to open Gyazo direct image url     |
| upload_script      | 'https://myazo.example.com/upload.php' | Full path to the upload.php file                    |
| secret             | 'hunter2'                              | Secret token                                        |
| clear_metadata     | True                                   | Controls clearing screenshot metadata before upload |
| open_browser       | True                                   | Controls open url in default browser after upload   |
| copy_clipboard     | True                                   | Controls copy url to clipboard after upload         |
| output_url         | True                                   | Controls print url to stdout after upload           |

Please note that if `gyazo_server` is set to `True`, `upload_script` and `secret` are ignored.

### Server

* Example Config: `server/src/config.php.example`
* Placement Path: `config.php` (relative to `upload.php`)

| Key                | Default                                | Description                                         |
|--------------------|----------------------------------------|-----------------------------------------------------|
| secretBcrypt       | ''                                     | Bcrypt hashed secret                                |
| saveDirName        | '/data/'                               | Writable directory where screenshots will be stored |
| maxScreenshotSize  | 2 * 1048576                            | Maximum size in bytes of uploaded screenshot        |
| screenshotMimeType | 'image/png'                            | MIME type of uploaded screenshot                    |

Please note that `maxScreenshotSize` may be capped externally by PHP and the web server.

## Desktop Icon/Shortcut

* GNU/Linux

Make sure the file is executable by running `chmod +x /path/to/myazo.py`.

`~/.local/share/applications/myazo.desktop`
```
[Desktop Entry]
Name=Myazo
Comment=Screenshot
Exec=/path/to/myazo.py
Terminal=false
Type=Application
Icon=applets-screenshooter
Categories=Utility;Graphics;
StartupNotify=false
```

* Windows

Rename `myazo.py` to `myazo.pyw` and create a new shortcut pointing to `C:\path\to\myazo.pyw`. Optionally, you can change the icon to a more fitting and better looking one (`shell32.dll`'s scissors one is decent). You can then pin the shortcut to the taskbar or start menu.

## License

MIT. See `License.md` for further information.

[Gyazo]: <https://gyazo.com/>
[Python]: <https://www.python.org/downloads/>
[Docker]: <https://docs.docker.com/>
[Docker Compose]: <https://docs.docker.com/compose/>
