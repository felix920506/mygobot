import yaml
import aiohttp
import aiofiles
import image_map
import os
import queue
import asyncio

with open('config.yml', 'r', encoding='utf8') as settingsfile:
    SETTINGS = yaml.load(settingsfile, yaml.Loader)

APIURL = SETTINGS['img-store-baseurl'].strip('/')

def get_link(name:str) -> str | None:
    return f'{APIURL}/{image_map.get_filename(name)}'

async def get_bytes_from_http(name:str):
    link = get_link(name)
    async with aiohttp.ClientSession() as session:
        res = await session.get(link)
        binary = res.read()
    return binary

async def download_file(name:str, force=False) -> None:
    filename = image_map.get_filename(name)
    if os.path.exists(f'./img/{filename}') and not force:
        return
    else:
        link = get_link(name)
        res = get_bytes_from_http(name)
        async with await aiofiles.open(f'./img/{filename}', 'wb') as file:
            await file.write(res)

async def get_file_handle(name: str) -> str | bytes:
    filename = image_map.get_filename(name)
    if SETTINGS['download-files']:
        await download_file(name)

    if os.path.exists(f'./img/{filename}'):
        return f'./img/{filename}'
    
    else:
        return await get_bytes_from_http(name)

async def download_thread(filequeue: queue.Queue) -> None:
    while not filequeue.empty:
        try:
            name = filequeue.get_nowait()
            await download_file(name)
        except:
            break
    pass

def download_all() -> None:
    file_list = image_map.get_all_names()
    filequeue = queue.Queue
    for file in file_list:
       filequeue.put(file)
    threadslist = []
    for i in range(SETTINGS['max-concurrent-downloads']):
        threadslist.append(lambda: download_thread(filequeue))
    
    asyncio.run(asyncio.gather(*threadslist))
    

    