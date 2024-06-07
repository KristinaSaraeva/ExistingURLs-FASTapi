import aiohttp
import asyncio
import sys
import requests
import time

async def submit_urls(urls):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8888/api/v1/tasks/", json=urls) as response:
            task_id = (await response.json())["id"]
            return task_id

async def get_task_status(task_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:8888/api/v1/tasks/{task_id}") as response:
            return await response.json()

def query_task_status(task_id):
    while True:
        response = requests.get(f"http://localhost:8888/api/v1/tasks/{task_id}")
        if response.status_code == 200:
            task_info = response.json()
            status = task_info["status"]
            result = task_info["result"]
            print(f"Task status: {status}, Result: {result}")
            if status == "ready":
                break
        else:
            print(f"Failed to query task status. Status code: {response.status_code}")
        time.sleep(5)  

if __name__ == "__main__":
    queryable_urls = sys.argv[1:]
    if len(sys.argv) < 2:
        print("Usage: python3 crawl.py <url1> <url2> <url3> ...")
        sys.exit(1)
    else:
        task_id = asyncio.run(submit_urls(queryable_urls))
        query_task_status(task_id)