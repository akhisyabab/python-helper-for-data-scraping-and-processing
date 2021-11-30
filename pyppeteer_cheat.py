import asyncio
import time

from bs4 import BeautifulSoup
from pyppeteer import launch

async def run():
    vin = 'WBANV71090BZ49028'

    browser = await launch({
        'args': [
            '--ignore-certificate-errors',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--window-size=1920,1080',
            "--disable-accelerated-2d-canvas",
            "--disable-gpu"],
        'ignoreHTTPSErrors': True,
        'headless': False,
    })

    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
    await page.goto('https://www.stolencars24.eu/en/main.php', {
        'waitUntil': 'networkidle0'
    })

    await page.waitForSelector('input[name=vid]')
    await page.focus('input[name=vid]')
    await page.keyboard.type(vin, {'delay': 50})
    await page.click('input[type="submit"]')
    await page.waitForSelector('div[role="alert"]')


    res_text = await page.content()
    f = open('res.html', 'w+')
    f.write(res_text)
    f.close()

    results = None
    if 'Your PC is currently blocked from accessing our database' in str(res_text):
        results = 'blocked'
    if 'The vehicle you are searching for is not registered in our database as stolen' in str(res_text):
        results = False

    if results is None:
        soup = BeautifulSoup(res_text, 'html.parser')
        table = soup.find('table', attrs={'class': 'w3_table_trade'})
        trs = table.find_all('tr')
        results = {}
        for tr in trs:
            tds = tr.find_all('td')
            key = tds[0].text.strip()
            value = tds[1].text.strip()
            results[key] = value

    print(results)


asyncio.get_event_loop().run_until_complete(run())


async def run2():
    browser = await launch({
        'args': [
            '--ignore-certificate-errors',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--window-size=1920,1080',
            "--disable-accelerated-2d-canvas",
            "--disable-gpu"],
        'ignoreHTTPSErrors': True,
        'headless': False,
    })

    page = await browser.newPage()

    ## example for page evaluated select specifict element
    summary = await page.evaluate('''() => document.querySelector('div.vin-summary').outerHTML''')

    ## example for page evaluated select specifict elements
    specs = await page.evaluate('''() => [...document.querySelectorAll("div.specs-popoverlay div.features-container > div.id135_vntbl_col")].map(ele=>{
        return {
            key: ele.querySelector("b").textContent.replace(":", ""),
            value : Array.prototype.filter.call(ele.childNodes, (child)=>child.nodeType === Node.TEXT_NODE).map((child)=>child.textContent).join('').trim()
        }
    })''')