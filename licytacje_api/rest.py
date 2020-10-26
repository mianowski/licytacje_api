import os
import requests
import unicodedata
import urllib.parse
from pathlib import Path
from datetime import date
from datetime import datetime

from babel.numbers import parse_decimal
from bs4 import BeautifulSoup

from .bs_helpers import make_soup
from .notice import Notice


NODE_URL = "https://licytacje.komornik.pl"


def get_search_soup(data: dict):
    initial_resp = requests.get(NODE_URL+"/Notice/Search")
    initial_soup = make_soup(initial_resp)
    ver_token = get_verification_token(initial_soup)
    data["__RequestVerificationToken"] = ver_token
    resp = requests.post(NODE_URL+"/Notice/Search",
                         data=data, cookies=initial_resp.cookies)
    return make_soup(resp)


def get_notice_soup(id):
    return make_soup(requests.get(NODE_URL+"/Notice/Details/"+str(id)))


def get_soup(url):
    return make_soup(requests.get(url))


def get_rows(html_soup):
    return html_soup.find_all("tr")


def get_cols(row):
    return row.find_all("td")


def get_verification_token(html_soup: BeautifulSoup) -> str:
    ver_token = html_soup.find(
        "input", attrs={"name": "__RequestVerificationToken"})
    return ver_token.attrs["value"]


def get_notices(html_soup):
    notices = html_soup.find_all(
        "a", href=lambda href: href and "/Notice/Details" in href)
    return [NODE_URL+str(notice.get("href")) for notice in notices]


def parse_price(text: str):
    return parse_decimal(text.replace('\xa0', '').replace(',', '.').replace(' zł', ''), locale='pl_PL')


def get_current_date():
    return date.today().strftime("%d.%m.%Y")


def get_report(data: dict) -> dict:

    soup = get_search_soup(data)

    rows = get_rows(soup)
    auctions = []
    for row in rows[1:]:
        cols = get_cols(row)
        if (len(cols) > 8):

            url = NODE_URL + cols[8].contents[1].get('href')
            cur_notice = Notice(url)
            auction = {
                'date': datetime.strptime(cols[2].get_text(strip=True), "%d.%m.%Y"),
                'url': url,
                'price': parse_price(cols[6].get_text(strip=True)),
                'kw': cur_notice.get_kw_number(),
                'address': cur_notice.get_address()
            }
            auction['id'] = auction['date'].strftime(
                "%Y%m%d")+"-"+str(auction["price"].to_integral_exact())
            auctions.append(auction)

            files_dir = os.path.join("..", "notices")
            Path(files_dir).mkdir(parents=True, exist_ok=True)
            file_path = os.path.join(files_dir, auction['id'])
            cur_notice.save_to_file(file_path)
    return auctions
