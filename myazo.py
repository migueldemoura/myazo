#!/usr/bin/env python3

from subprocess import run
import os
import platform
import shutil
import tempfile
import webbrowser
from PIL import Image
import pyperclip
import requests

# Settings
upload_script = 'https://'
secret = ''
clear_metadata = True
open_browser = True
copy_clipboard = True
output_url = True

tmp_file = '{}/{}.png'.format(tempfile.gettempdir(), next(tempfile._get_candidate_names()))

backends = {
    'Linux': {
        'gnome-screenshot': ['-a', '-f', tmp_file],
        'scrot': ['-s', tmp_file],
        'import': [tmp_file] # ImageMagick
    },
    'Darwin': { # macOS
        'screencapture': ['-i', tmp_file]
    },
    'Windows': {
        'snippingtool': ['/clip'] # '/clip' requires at least Win10 v.1703
    }
}

for utils in (utils for os_name, utils in backends.items() if os_name == platform.system()):
    for util, args in utils.items():
        if shutil.which(util) != None and run([util] + args).returncode == 0:
            break
    break

# If the util used stored the screenshot in the clipboard, output it to the tmp file
if util == 'snippingtool':
    from PIL import ImageGrab
    img = ImageGrab.grabclipboard()
    if img is not None:
        img.save(tmp_file, optimize=True)

if os.path.isfile(tmp_file) != True:
    print('Error: Failed to take screenshot.')
    exit(-1)

if clear_metadata:
    img = Image.open(tmp_file)
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(list(img.getdata()))
    new_img.save(tmp_file, optimize=True)

img = open(tmp_file, 'rb')

url = requests.post(('{}?s={}').format(upload_script, secret), files={'screenshot': img}).text

if open_browser:
    webbrowser.open(url)
if copy_clipboard:
    pyperclip.copy(url)
if output_url:
    print(url)

img.close()
os.remove(tmp_file)
