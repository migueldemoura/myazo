#!/usr/bin/env python3

from configparser import ConfigParser
from pathlib import Path
from subprocess import run
import os
import platform
import shutil
import tempfile
import webbrowser
from PIL import Image
import pyperclip
import requests

# Configuration
config = ConfigParser()
config.read_dict({'Myazo': {
    'gyazo_server': False, # If True, upload_script and secret are ignored
    'gyazo_direct_link': True, # Ignored if gyazo_server is False
    'upload_script': 'https://myazo.example.com/upload.php',
    'secret': 'hunter2',
    'clear_metadata': True,
    'open_browser': True,
    'copy_clipboard': True,
    'output_url': True
}})
config.read(os.path.expanduser('~/.config/myazo/config.ini'))
config = config['Myazo']

tmp_file = '{}/{}.png'.format(tempfile.gettempdir(), next(tempfile._get_candidate_names()))

backends = {
    'Linux': {
        'gnome-screenshot': ['-a', '-f', tmp_file],
        'mv': ['$(xfce4-screenshooter -r -o ls)', tmp_file],
        # KDE Spectacle requires slight user interaction after selecting region
        'spectacle': ['-b', '-n', '-r', '-o', tmp_file],
        'scrot': ['-s', tmp_file],
        'import': [tmp_file] # ImageMagick
    },
    'Darwin': { # macOS
        'screencapture': ['-i', tmp_file]
    },
    'Windows': {
        'snippingtool': ['/clip'] # '/clip' requires at least Win10 1703
    }
}

for util, args in backends[platform.system()].items():
    if shutil.which(util) != None and run([util] + args).returncode == 0:
        break

# If the used util stored the screenshot in the clipboard, output it to the tmp file
if util == 'snippingtool':
    from PIL import ImageGrab
    img = ImageGrab.grabclipboard()
    if img is not None:
        img.save(tmp_file, optimize=True)

if os.path.isfile(tmp_file) != True:
    print('Error: Failed to take screenshot.')
    exit(-1)

if config.getboolean('clear_metadata'):
    img = Image.open(tmp_file)
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(list(img.getdata()))
    new_img.save(tmp_file, optimize=True)

img = open(tmp_file, 'rb')

if config.getboolean('gyazo_server'):
    r = requests.post(
        'https://upload.gyazo.com/upload.cgi',
        files={'imagedata': img}
    )
else:
    r = requests.post(
        config.get('upload_script'),
        data={'secret': config.get('secret')},
        files={'screenshot': img}
    )

if r.status_code != 200:
    print('Error: Failed to upload screenshot. Server returned status code {}.'.format(r.status_code))
    exit(-2)

if config.getboolean('gyazo_server') and config.getboolean('gyazo_direct_link'):
    # Convert the Gyazo link to a direct image
    # https://gyazo.com/hash > https://i.gyazo.com/hash.extension
    url = r.text.replace('//', '//i.') + Path(tmp_file).suffix
else:
    url = r.text

if config.getboolean('open_browser'):
    webbrowser.open(url)
if config.getboolean('copy_clipboard'):
    pyperclip.copy(url)
if config.getboolean('output_url'):
    print(url)

img.close()
os.remove(tmp_file)
