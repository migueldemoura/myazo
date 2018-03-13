# Myazo

![Demo](https://raw.githubusercontent.com/migueldemoura/myazo/master/demo.gif)

Myazo is a self-hosted [Gyazo](https://gyazo.com/) alternative. It allows you to take a screenshot of part of your screen and automatically upload it to your own server.

It is comprised by a cross-platform client in Python which defers the actual taking of screenshot to OS built-in tools (macOS and Windows) or common utilities (GNU/Linux distributions). The server script, designed with cheap shared hosting in mind, is written with the ubiquitous PHP. Both the client and server are single files. You may separate the settings from the code if you wish.

## Compatibility

The following OSes have off-the-shelf compatibility. You can add more back ends for missing systems or configurations.

- GNU/Linux (presets for `gnome-screenshot`, `scrot` and `import` (ImageMagick))
- macOS
- Windows 10 version >= 1703

## Installation & Configuration

* Install [Python] 3.x and choose the version matching your CPU arch (x86 or x86-64);
* Install client requirements:

```shell
pip install -r requirements.txt
```

* Choose or generate a secret key and fill in the variable `secret` at `myazo.py`;
* Hash the secret key with bcrypt and fill in the variable `secretBcrypt` at `web/upload.php`;
You can do so with PHP itself:

```shell
php -r "echo password_hash('yoursecrethere', PASSWORD_DEFAULT);"
```

Or using any other way you prefer.

* Upload the `web/upload.php` to your webserver. Make sure directory listing is disabled;
* Enter the full public url of the `web/upload.php` script in the variable `upload_script` at `myazo.py`.

## Desktop Icon/Shortcut

* GNU/Linux

If you run `chmod +x myazo.py`, you can swap `Exec=python3 /path/to/myazo.py` with `Exec= /path/to/myazo.py`.

`~/.local/share/applications/myazo.desktop`
```
[Desktop Entry]
Name=Myazo
Comment=Screenshot
Exec=python3 /path/to/myazo.py
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
