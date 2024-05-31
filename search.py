import aiohttp
import asyncio
from date_str import HourlyIterator
from get_CookieToken import get_CookieToken
import datetime

from load_JSON import load_JSON

async def search(date,tokie,semaphore):
    '''
    返回一个迭代器，包含某一小时的所有图片链接
    date      1750-04-09-01 凌晨一点
    '''
    CAKEPHP_cookie=tokie['CAKEPHP']
    X_Csrftoken=tokie['FIXED_TOKEN']

    # 文件的URL
    url = 'https://sc-nc-web.nict.go.jp/wsdb_osndisk/fileSearch/search'

    headers = {

        "Cookie": f"CAKEPHP={CAKEPHP_cookie}",
        "HashToken": "bDw2maKV",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "X-CSRFToken": X_Csrftoken,

    }
    _day=date.replace('-', '/', 1)[:-3]
    _h=date[-2:]
    data={'searchPath': f'png/Pifd/{_day}/{_h}',
        'searchStr': f'*.png',
        'action': 'dir_download_dl'}

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data, headers=headers,proxy='http://127.0.0.1:7897') as response:
                if response.status != 200:
                    return response.status
                content =await response.text()
                return load_JSON(str(content))
                

async def generate_items(start,end, tokie,semaphore):
    '''date      1750-04-09-01 凌晨一点'''

    hourly_itor = HourlyIterator(start, end)
    for date in hourly_itor:
        img_items=await search(date=date,tokie=tokie,semaphore=semaphore)
        for img_item in img_items:
            item={
                'name':img_item['name'],
                'hashUrl':img_item['hashUrl'],
                'd_url':img_item['d_url'],
                'cookie': tokie['CAKEPHP'],
                'token':tokie['FIXED_TOKEN']

            }
            yield item


if __name__ == "__main__":
    async def main():
        queue = asyncio.Queue()
        progress_queue = asyncio.Queue()
        semaphore = asyncio.Semaphore(5)  # 允许5个并发下载
        output_path = './downloads'
        semaphore = asyncio.Semaphore(5)  # 允许5个并发下载
        Tokie = get_CookieToken()
        start_date = datetime.datetime(2023, 1, 1, 0)
        end_date = datetime.datetime(2024, 1, 1, 1)
        async for item in generate_items(start_date, end_date, Tokie, semaphore):
            print(item)




    asyncio.run(main())