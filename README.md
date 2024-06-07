## WEB CRAWLER 

The program consists of two files:
- server.py
- web_crawler.py 

For the client side aiohttp is used and  for the server side - FastAPI.
All the I/O code is asynchronous.

The workflow goes like this:
- server is started and listening on port 8888

- client (web_crawler.py) receives one or several queryable URLs as an argument:

`python web_crawler.py <url1> <url2> <url3> ...`</br>

- client submits all the URLs via HTTP POST request as a JSON list to a server endpoint (/api/v1/tasks/)

- server responds with HTTP 201 created and a task object (PyDantic)

- task object includes a status "running" and an ID (UUID4)

- server then starts asynchronously to send HTTP GET queries to submitted URLs and collect HTTP response codes

- client keeps periodically querying endpoint /api/v1/tasks/{received_task_id} until server
finishes processing all the URLs. Then task status should change to "ready" and task "result"
field should have a list of HTTP response codes for the submitted URLs

- client prints out tab separated HTTP response code and corresponding URL for every entry

async/await paradigm is used