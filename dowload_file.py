from weakref import proxy
import aiohttp
import asyncio
from date_str import HourlyIterator
from get_CookieToken import get_CookieToken
import os


async def download_file(item, output_path, semaphore, progress_queue):
    file_name = item['name']
    hashUrl = item['hashUrl']
    d_url = item['d_url']
    CAKEPHP_cookie = item['cookie']
    fixedToken = item['token']

    url = 'https://sc-nc-web.nict.go.jp/wsdb_osndisk/fileSearch/download'
    
    headers = {
        "Cookie": f"CAKEPHP={CAKEPHP_cookie}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    data = {
        "_method": "POST",
        "data[FileSearch][is_compress]": "false",
        'data[FileSearch][fixedToken]': fixedToken,
        'data[FileSearch][hashUrl]': hashUrl,
        "action": "dir_download_dl",
        "filelist[0]": d_url,
        "dl_path": d_url 
    }

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data, headers=headers,proxy='http://127.0.0.1:7897') as response:
                if response.status != 200:
                    print(f"Failed to download file: {response.status}")
                    await progress_queue.put((file_name, -1, -1))  # 下载失败
                    return False
                
                total_size = int(response.headers.get('content-length', 0))
                if total_size == 0:
                    print("not exist:"+file_name)
                    return False
                chunk_size = 1024  # 设置块大小
                
                os.makedirs(output_path, exist_ok=True)
                file_path = os.path.join(output_path, file_name)
                
                downloaded_size = 0
                with open(file_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        await progress_queue.put((file_name, downloaded_size, total_size))
                
                await progress_queue.put((file_name, total_size, total_size))  # 下载完成

                return True
