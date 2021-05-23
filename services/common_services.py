from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import io


def get_soup(url):
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()
    return BeautifulSoup(page, 'html.parser')


def write_file_json(path, data):
    with io.open(path, 'w', encoding="utf-8") as output:
        json.dump(data, output, ensure_ascii=False)


def write_file_text(path, data, label):
    with io.open(path, 'a', encoding="utf-8") as output:
        for text in data:
            output.write(f"{label} {text}\n")
