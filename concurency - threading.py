import concurrent.futures
import requests
import threading
import time
from bs4 import BeautifulSoup

thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.text
        print(title)
        return title


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor_result = executor.map(download_site, sites)
        results = [result for result in executor_result]
        return results


if __name__ == "__main__":
    sites = [
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
    start_time = time.time()
    results = download_all_sites(sites)
    duration = time.time() - start_time
    print(results)
    print(f"Downloaded {len(sites)} in {duration} seconds")