import asyncio
from datetime import datetime, timedelta
from get_CookieToken import get_CookieToken
from search import generate_items
from display_progress import display_progress
from dowload_file import download_file
import os
from tqdm import tqdm
from time import sleep

async def consumer(queue, output_path, semaphore, progress_queue):
    while True:
        item = await queue.get()
        print(f"收到{item['name']} ")
        if item is None:
            queue.task_done()
            return True
        try:
            await download_file(item, output_path, semaphore, progress_queue)
            queue.task_done()
        except:
            file_path = os.path.join(output_path, item['name'])
            print(f'{file_path} 异常，重试中')
            continue
        


async def producer(queue, semaphore):
    while True:
        Tokie=get_CookieToken()
        JSTNow= (datetime.now()+ timedelta(hours=1))#.strftime('%Y-%m-%d-%H')
        print(f'JST: {JSTNow} tokie updated')
        async for item in generate_items(JSTNow, JSTNow, Tokie, semaphore):
            if item is None:
                print('未返回结果')
                continue
            await queue.put(item)
            print(f"已发现{item['name']} ")
        
        for i in tqdm(range(30), desc="延时30秒", unit="sec"):
            await asyncio.sleep(1)


async def main():
    MAX_CONCURRENCY=6
    queue = asyncio.Queue()
    progress_queue = asyncio.Queue()
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)  
    output_path = r'./UptoDate'

    producer_task = asyncio.create_task(producer(queue,semaphore))
    consumer_tasks = [asyncio.create_task(consumer(queue, output_path, semaphore, progress_queue))  for _ in range(MAX_CONCURRENCY)]
    display_task = asyncio.create_task(display_progress(progress_queue))

    await asyncio.gather(producer_task,*consumer_tasks)
    
    await display_task





if __name__ == "__main__":
    asyncio.run(main())        