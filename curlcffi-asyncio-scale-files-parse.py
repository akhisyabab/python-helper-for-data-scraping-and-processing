import os
import json
import gzip
import asyncio
from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession

# CONFIG
IS_CONCURRENT = True
MAX_CONCURRENT = 20
BATCH_SIZE = 200

TRIMS_DIR = "./trims"
RESULTS_DIR = "./results"

os.makedirs(RESULTS_DIR, exist_ok=True)


def get_proxy():
    return {
        "http": "http://username:password@host:port",
        "https": "http://username:password@host:port"
    }


def safe_name(text: str) -> str:
    return text.replace("/", "_._").replace(" ", "._.")


def build_filename(year, make, model, trim):
    return f"{year}_{safe_name(make)}_{safe_name(model)}_{safe_name(trim)}.json.gz"


# Improved parser
def parse_html(html):
    try:
        soup = BeautifulSoup(html, "lxml")

        title = soup.title.string.strip() if soup.title and soup.title.string else None

        # Example safe extraction
        def safe_select(selector):
            el = soup.select_one(selector)
            return el.get_text(strip=True) if el else None

        data = {
            "title": title,
            # customize here:
            # "price": safe_select(".price"),
        }

        return data

    except Exception as e:
        return {"parse_error": str(e)}


async def fetch_and_save(session, item, existing_files, semaphore=None):
    year = item["year"]
    make = item["make"]
    model = item["model"]
    trim_name = item["trim_name"]
    url = item["trim_url"]

    filename = build_filename(year, make, model, trim_name)
    filepath = os.path.join(RESULTS_DIR, filename)

    # fast skip
    if filename in existing_files:
        return

    async def _do():
        for attempt in range(5):
            try:
                res = await session.get(
                    url,
                    timeout=30,
                    proxies=get_proxy()
                )

                if res.status_code == 200:
                    html = res.text

                    # non-blocking parsing
                    parsed = await asyncio.to_thread(parse_html, html)

                    result = {
                        "year": year,
                        "make": make,
                        "model": model,
                        "trim": trim_name,
                        "url": url,
                        "data": parsed
                    }

                    tmp = filepath + ".tmp"

                    with gzip.open(tmp, "wt", encoding="utf-8") as f:
                        json.dump(result, f, separators=(",", ":"))

                    os.replace(tmp, filepath)
                    existing_files.add(filename)  # prevent duplicate work potentially.

                    return

                elif res.status_code in (404, 410):
                    print(f"SKIP (not found): {url}")
                    return

                elif res.status_code in (403, 429):
                    print(f"BLOCKED {res.status_code}: retrying {url}")
                    await asyncio.sleep(2)
                    continue

                else:
                    print(f"Status {res.status_code}: {url}")

            except Exception as e:
                print(f"ERROR ({attempt+1}) {url} -> {e}")
                await asyncio.sleep(1)

        print(f"FAILED: {url}")

    if semaphore:
        async with semaphore:
            await _do()
    else:
        await _do()


def iter_items():
    for file in os.listdir(TRIMS_DIR):
        if not file.endswith(".json"):
            continue

        path = os.path.join(TRIMS_DIR, file)

        with open(path) as f:
            data = json.load(f)

        year = data["year"]
        make = data["make"]
        model = data["model"]

        for trim in data["trims"]:
            yield {
                "year": year,
                "make": make,
                "model": model,
                "trim_name": trim["trim_name"],
                "trim_url": trim["trim_url"]
            }


async def run_concurrent():
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    # preload existing files (FAST)
    existing_files = set(os.listdir(RESULTS_DIR))

    async with AsyncSession() as session:
        batch = []

        for item in iter_items():
            batch.append(fetch_and_save(session, item, existing_files, semaphore))

            if len(batch) >= BATCH_SIZE:
                await asyncio.gather(*batch, return_exceptions=True)
                batch.clear()

        if batch:
            await asyncio.gather(*batch, return_exceptions=True)


async def run_sequential():
    existing_files = set(os.listdir(RESULTS_DIR))

    async with AsyncSession() as session:
        for item in iter_items():
            await fetch_and_save(session, item, existing_files)


def start():
    if IS_CONCURRENT:
        asyncio.run(run_concurrent())
    else:
        asyncio.run(run_sequential())


if __name__ == "__main__":
    start()