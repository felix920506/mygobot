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

def get_images(message: str) -> set[str]:
    message = message.lower()
    imgs = set()

    if not message:
        return
    
    for key in message_mappings:
        if key in message:
            value = message_mappings[key]
            imgs.update(value['value'])
    
    for name in image_map.get_all_names():
        if message in name:
            imgs.add(name)

    return imgs

@bot.event
async def on_message(ctx: discord.Message):
    # ignore bots
    if ctx.author.bot:
        return
    
    # get images
    imgs = get_images(ctx.content)

    imgs = list(imgs)
    if len(imgs) > 0:
        img = imgs[random.randint(0, len(imgs)-1)]
        
        if SETTINGS['send-as-attachment']:
            file = await imagegetter.get_file_handle(img)
            if file is None:
                print(f'Could not send file {img}')
            fileObject = discord.File(file, f'{img}.jpg')
            try:
                await ctx.channel.send(file=fileObject)
            except discord.errors.Forbidden:
                print("permission denied when attempting to send message")
                
        else:
            try:
                await ctx.channel.send(imagegetter.get_link(img))
            except discord.errors.Forbidden:
                print("permission denied when attempting to send message")
    
    if await bot.is_owner(ctx.author):
        if ctx.content.strip() == "春日影":
            reload()
            print("為什麼要演奏春日影！")


# slash commands section
mygo = bot.create_group('mygo')

@mygo.command(description="搜尋表情包")
async def search(ctx: discord.ApplicationContext, message: discord.Option(str, name="訊息")):
    # get images
    imgs = get_images(message)

    imgs = list(imgs)
    if len(imgs) > 0:
        img = imgs[random.randint(0, len(imgs)-1)]
        
        if SETTINGS['send-as-attachment']:
            file = await imagegetter.get_file_handle(img)
            if file is None:
                print(f'Could not send file {img}')
            fileObject = discord.File(file, f'{img}.jpg')
            try:
                await ctx.respond(file=fileObject)
            except discord.errors.Forbidden:
                print("permission denied when attempting to send message")
                
        else:
            try:
                await ctx.respond(imagegetter.get_link(img))
            except discord.errors.Forbidden:
                print("permission denied when attempting to send message")

    else:
        # nothing found for this message
        await ctx.respond("沒有找到表情包", ephemeral=True)
bot.run(bot_token)

    
    

