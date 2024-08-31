import discord
import yaml
import json
import os
import imagegetter
import image_map
import asyncio

with open('config.yml', 'r', encoding='utf8') as configfile:
    SETTINGS = yaml.load(configfile, yaml.Loader)

# deal with settings
if SETTINGS['send-as-attachment'] & SETTINGS['download-files']:
    if not os.path.isdir('./img'):
        try:
            os.mkdir('./img')
        except:
            print('failed to make storage dir, quitting')
            exit()
    
    if SETTINGS['download-at-startup']:
        asyncio.run(imagegetter.download_all())
