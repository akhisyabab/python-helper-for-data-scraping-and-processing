import asyncio
import requests
import time

from aiohttp import ClientSession
from bs4 import BeautifulSoup

links = [
    'https://en.wikipedia.org/wiki/Indonesia',
    'https://en.wikipedia.org/wiki/Singapore',
    'https://en.wikipedia.org/wiki/United_States',
    'https://en.wikipedia.org/wiki/Canada',
    'https://en.wikipedia.org/wiki/United_Kingdom',
    'https://en.wikipedia.org/wiki/Egypt',
    'https://en.wikipedia.org/wiki/Algeria',
    'https://en.wikipedia.org/wiki/South_Africa',
    'https://en.wikipedia.org/wiki/Brazil',
    'https://en.wikipedia.org/wiki/Argentina',
    'https://en.wikipedia.org/wiki/France'
]

# Asynchronous
async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        res = await session.get(url)
        res_text = await res.text()
        soup = BeautifulSoup(res_text, 'html.parser')
        title = soup.find('title').text
        print(title)
        return title


async def main(links):
    tasks = []
    # Sets the amount of concurrent requests per task
    sem = asyncio.Semaphore(10)
    async with ClientSession() as session:
        for url in links:
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)
        return await asyncio.gather(*tasks)

start_time = time.time()
asyncio.set_event_loop(asyncio.SelectorEventLoop())
results = asyncio.get_event_loop().run_until_complete(main(links))
duration = time.time() - start_time
print(results)
print(f"Downloaded {len(links)} sites in {duration} seconds")