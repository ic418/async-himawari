import asyncio
import datetime
from get_CookieToken import get_CookieToken
from search import generate_items
from display_progress import display_progress
from dowload_file import download_file

async def consumer(queue, output_path, semaphore, progress_queue):
    item = await queue.get()
    if item is None:
        queue.task_done()
        return True
    while True:
        try:
            await download_file(item, output_path, semaphore, progress_queue)
            break
        except:
            continue
    # print(item['name'])
    queue.task_done()
    return True



async def producer(queue,start_date, end_date, Tokie, semaphore):
    async for item in generate_items(start_date, end_date, Tokie, semaphore):
        await queue.put(item)
    # 向队列中放入 None 以停止消费者
    await queue.put(None)
    return True


async def main():
    MAX_CONCURRENCY=1000
    queue = asyncio.Queue()
    progress_queue = asyncio.Queue()
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)  
    output_path = r'C:\himawari\downloads'

    Tokie = get_CookieToken()
    date=(2024, 5, 30, 19)
    start_date = datetime.datetime(2024, 5, 30, 0)
    end_date = datetime.datetime(2024, 5, 30, 23)
    # end_date=start_date


    producer_task = asyncio.create_task(producer(queue,start_date, end_date, Tokie, semaphore))
    consumer_tasks = [asyncio.create_task(consumer(queue, output_path, semaphore, progress_queue))  for _ in range(MAX_CONCURRENCY)]
    display_task = asyncio.create_task(display_progress(progress_queue))

    a=await asyncio.gather(producer_task,*consumer_tasks)
    
    await display_task





if __name__ == "__main__":
    asyncio.run(main())