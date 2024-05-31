import aiohttp
import asyncio
import os
from get_CookieToken import get_CookieToken


data_queue = asyncio.Queue()


async def download_file(item, output_path, semaphore):
    '''
     item={'name': 'hima920240520161000fd.png', 
                  'hashUrl': 'bDw2maKV', 
                  'd_url': '/osn-disk/webuser/wsdb/share_directory/bDw2maKV/png/Pifd/2024/05-20/16/hima920240520161000fd.png'}
    '''
    file_name=item['name']
    hashUrl=item['hashUrl']
    d_url=item['d_url']

    tokie=get_CookieToken()
    CAKEPHP_cookie=tokie['CAKEPHP']
    fixedToken=tokie['FIXED_TOKEN']
    url = 'https://sc-nc-web.nict.go.jp/wsdb_osndisk/fileSearch/download'
    
    headers = {
        "Cookie": f"CAKEPHP={CAKEPHP_cookie}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    data={
        "_method": "POST",
        "data[FileSearch][is_compress]": "false",
        'data[FileSearch][fixedToken]': fixedToken,
        'data[FileSearch][hashUrl]': hashUrl,
        "action": "dir_download_dl",
        "filelist[0]": d_url,
        "dl_path":d_url 
    }
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url,data=data,headers=headers) as response:
                if response.status != 200:
                    print(f"Failed to download file: {response.status}")
                    return False
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                chunk_size = 1024  # 设置块大小
                
                file_path=os.path.join(output_path,file_name)
                with open(file_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        print_progress_bar(downloaded_size, total_size)
                
                print()  # 换行
                return True

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    调用在循环中以创建进度条
    @params:
        iteration   - 当前迭代次数
        total       - 总迭代次数
        prefix      - 进度条前缀
        suffix      - 进度条后缀
        decimals    - 小数点位数
        length      - 进度条长度
        fill        - 进度条填充字符
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # 当完成时打印新行
    if iteration == total:
        print()

# 使用示例
item={'name': 'hima920240520000000fd.png', 
                  'hashUrl': 'bDw2maKV', 
                  'd_url': '/osn-disk/webuser/wsdb/share_directory/bDw2maKV/png/Pifd/2024/05-20/00/hima920240520000000fd.png'}
output_path = './'
semaphore = asyncio.Semaphore(5) 
asyncio.run(download_file(item=item, output_path=output_path, semaphore=semaphore))