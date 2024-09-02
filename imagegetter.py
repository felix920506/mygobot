import yaml
import aiohttp
import aiofiles
import image_map
import os
import queue
import asyncio
import io

with open('config.yml', 'r', encoding='utf8') as settingsfile:
    SETTINGS = yaml.load(settingsfile, yaml.Loader)

APIURL = SETTINGS['img-store-baseurl'].strip('/')

def get_link(name:str) -> str | None:
    return f'{APIURL}/{image_map.get_filename(name)}'

async def get_bytes_from_http(name:str):
    link = get_link(name)
    async with aiohttp.ClientSession() as session:
        res = await session.get(link)
        binary = await res.read()
    return binary

async def download_file(name:str, force=False) -> None:
    filename = image_map.get_filename(name)
    if os.path.exists(f'./img/{filename}') and not force:
        return
    else:
        print(f'downloading {name}')
        link = get_link(name)
        res = await get_bytes_from_http(name)
        file = await aiofiles.open(f'./img/{filename}', 'wb')
        await file.write(res)
        await file.close()

# intended for use with pycord attachment function only
async def get_file_handle(name: str) -> str | bytes:
    filename = image_map.get_filename(name)
    if SETTINGS['download-files']:
        await download_file(name)

    if os.path.exists(f'./img/{filename}'):
        return f'./img/{filename}'
    
    else:
        return io.BytesIO(await get_bytes_from_http(name))

async def download_thread(filequeue: queue.Queue) -> None:
    while not filequeue.empty():
        try:
            name = filequeue.get(timeout=1)
            await download_file(name)
        except:
            break

async def download_all() -> None:
    if not os.path.isdir('./img'):
        try:
            os.mkdir('./img')
        except:
            print('failed to make storage dir, quitting')
            exit()
    file_list = image_map.get_all_names()
    filequeue = queue.Queue()
    for file in file_list:
       filequeue.put(file)
    threadslist = []
    async with asyncio.TaskGroup() as tg:
        for i in range(SETTINGS['max-concurrent-downloads']):
            threadslist.append(tg.create_task(download_thread(filequeue)))
    
if __name__ == '__main__':
    asyncio.run(download_all())
    