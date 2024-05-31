from tqdm import tqdm
import asyncio
async def display_progress(progress_queue):
    # 用于存储进度条的字典
    progress_bars = {}

    while True:
        # await asyncio.sleep(1)
        file_name, downloaded_size, total_size = await progress_queue.get()

        # 如果进度条不存在，则创建一个新的进度条
        if file_name not in progress_bars:
            progress_bars[file_name] = tqdm(total=total_size, desc=file_name, unit='B', unit_scale=True)

        # 更新进度条
        progress_bars[file_name].update(downloaded_size - progress_bars[file_name].n)

        # 检查下载是否完成或失败
        if downloaded_size == -1:
            print(f"Failed to download {file_name}")
            progress_bars[file_name].close()
            del progress_bars[file_name]
        elif downloaded_size == total_size:
            print(f"Completed download of {file_name}")
            progress_bars[file_name].close()
            del progress_bars[file_name]
        progress_queue.task_done()