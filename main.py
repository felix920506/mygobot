import discord
import yaml
import json
import os
import imagegetter
import image_map
import asyncio
import random

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

def reload():
    global message_mappings
    with open('mygo.json', 'r', encoding='utf8') as mappingfile:
        message_mappings = json.load(mappingfile)

message_mappings = {}
reload()

# bot section
with open('token.txt', 'r', encoding='utf8') as tokenfile:
    bot_token = tokenfile.read().strip()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_message(ctx: discord.Message):
    if ctx.author.bot:
        return
    imgs = set()
    msg = ctx.content.lower()
    for key in message_mappings:
        if key in msg:
            value = message_mappings[key]
            imgs.update(value['value'])
    
    imgs = list(imgs)
    if len(imgs) > 0:
        img = imgs[random.randint(0, len(imgs)-1)]
        
        if SETTINGS['send-as-attachment']:
            file = await imagegetter.get_file_handle(img)
            fileObject = discord.File(file, f'{img}.jpg')
            await ctx.channel.send(file=fileObject)
        else:
            await ctx.channel.send(imagegetter.get_link(img))
    
    if await bot.is_owner(ctx.author):
        if ctx.content.strip() == "春日影":
            reload()
            print("為什麼要演奏春日影！")

bot.run(bot_token)

    
    

