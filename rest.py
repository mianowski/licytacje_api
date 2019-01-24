import platform
import sys
import requests
import unicodedata
import urllib.parse
from bs4 import BeautifulSoup
import re
from babel.numbers import parse_decimal
import pandas as pd

import notice


"""
POST http://www.licytacje.komornik.pl/Notice/Search HTTP/1.1
Host: www.licytacje.komornik.pl
Proxy-Connection: keep-alive
Content-Length: 289
Cache-Control: max-age=0
Origin: http://www.licytacje.komornik.pl
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: http://www.licytacje.komornik.pl/Notice/Search
Accept-Encoding: gzip, deflate
Accept-Language: pl,en-US;q=0.9,en;q=0.8
Cookie: ASP.NET_SessionId=lrdwev2kco0bidh5f2lsmnph; licytacje.komornik.pl=cookiesPolicy=true; __utma=7112751.758720803.1540820573.1540820573.1540820573.1; __utmc=7112751; __utmz=7112751.1540820573.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)
"""
NODE_URL = "http://www.licytacje.komornik.pl"

def get_search_soup(data):
    return make_soup(requests.post(NODE_URL+"/Notice/Search", data=data))

def get_notice_soup(id):
    return make_soup(requests.get(NODE_URL+"/Notice/Details/"+str(id)))

def get_soup(url):
    return make_soup(requests.get(url))

def make_soup(result):
    return BeautifulSoup(result.content, 'html.parser')

# encoded_data = "Type=1&CategoryId=&MobilityCategoryId=&PropertyCategoryId=30&City=Wroc%C5%82aw&tbx-province=&ProvinceId=&AuctionsDate=&Words=&PriceFrom=&PriceTo=&ItemMin=&ItemMax=&OfficeId=&JudgmentId=&PublicationDateFrom=&PublicationDateTo=&StartDateFrom=&StartDateTo=&SumMin=&SumMax=&Vat=&TypeOfAuction="
# data = urllib.parse.parse_qs(encoded_data)
# data = {'Type': ['1'], 'PropertyCategoryId': ['30'], 'City': ['Wrocław']}

def get_rows(html_soup):
    return html_soup.find_all("tr")
    
def get_cols(row):
    return row.find_all("td")

def get_notices(html_soup):
    notices = html_soup.find_all("a", href=lambda href: href and "/Notice/Details" in href)
    return [ NODE_URL+str(notice.get("href")) for notice in notices]

def parse_price(text):
    return parse_decimal(text.replace('\xa0', '').replace(',', '.').replace(' zł', ''), locale='pl_PL')

def get_report():
    data = {
        'Type': ['1'], 
        'City': ['Wrocław'],
        # 'JudgmentId': ['1103']
        }

    soup = get_search_soup(data)
    
    rows = get_rows(soup)
    auctions = []
    for row in rows[1:]:
        cols = get_cols(row)
        url = NODE_URL + cols[7].contents[1].get('href')
        auction = {
            'date': cols[2].get_text(strip=True),
            'url' : url,
            'price' : parse_price(cols[6].get_text(strip=True)),
            'kw' : notice.get_kw_number(notice.get_preview(get_soup(url)))
        }
        auctions.append(auction)
    return pd.DataFrame(auctions)
    


if __name__=="__main__":
    auctions = get_report()
    print(auctions.sort_values("price"))

    