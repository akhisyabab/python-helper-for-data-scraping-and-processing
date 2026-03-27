# WRITING TO HTML FILE
import gzip
import requests
url = "https://example.com"
res = requests.get(url)

## without gzip
with open("page.html", "wb") as f:
    f.write(res.content)

## with gzip
with gzip.open("page.html.gz", "wt", encoding="utf-8") as f:
    f.write(res.text)

# ========================================== #
# READING
import gzip
from bs4 import BeautifulSoup

## without gzip
with open("page.html", "r", encoding="utf-8") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")

## with gzip
with gzip.open("page.html.gz", "rt", encoding="utf-8") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")


