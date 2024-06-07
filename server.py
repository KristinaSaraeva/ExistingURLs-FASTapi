from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uuid
import aiohttp
import uvicorn
import asyncio


app = FastAPI()

tasks = {}

class Task(BaseModel):
    id: uuid.UUID
    status: str
    result: list = []


@app.get("/")
def read_root():
    return {"message": "World"}


async def process_urls(task_id: uuid.UUID, urls: list[str]):
    print("processing", task_id)
    connector = aiohttp.TCPConnector(ssl=False) 
    async with aiohttp.ClientSession(connector=connector) as session:
        async def fetch_url(url):
            try:
                async with session.get(url) as response:
                    print("Status for", url, ":", response.status)
                    return url, response.status
            except aiohttp.ClientError:
                print("Exception for", url)
                return url, 500

        results = {}
        for url, status in await asyncio.gather(*[fetch_url(url) for url in urls]):
            tasks[task_id].result.append(status)
            if len(tasks[task_id].result) == len(urls):
                tasks[task_id].status = "ready"
            results[url] = status

        return results
    

@app.post("/api/v1/tasks/", response_model=Task, status_code=201)
async def create_task(urls: list[str],background_tasks: BackgroundTasks):
    task_id = uuid.uuid4()
    task = Task(id=task_id, status="running")
    tasks[task_id] = task
    print("task created", len(tasks))

    background_tasks.add_task(process_urls, task_id, urls)
    
    return tasks[task_id]

@app.get("/api/v1/tasks/{task_id}", response_model=Task)
async def read_task(task_id: uuid.UUID):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.get("/api/v1/tasks/")
async def read_tasks():
    return tasks

if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=8888, reload=True)

