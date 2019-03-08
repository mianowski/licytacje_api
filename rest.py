import platform
import sys
import requests
import unicodedata
import urllib.parse

import re
from babel.numbers import parse_decimal

import pandas as pd

import notice
from bs_helpers import make_soup

NODE_URL = "http://www.licytacje.komornik.pl"

def get_search_soup(data):
    return make_soup(requests.post(NODE_URL+"/Notice/Search", data=data))

def get_notice_soup(id):
    return make_soup(requests.get(NODE_URL+"/Notice/Details/"+str(id)))

def get_soup(url):
    return make_soup(requests.get(url))


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
                
        # 'CategoryId': []
        # 'MobilityCategoryId': 
        # 'PropertyCategoryId': 
        # 'City': Wrocław
        # 'tbx-province': 
        # 'ProvinceId': 
        # 'AuctionsDate': 
        # 'Words': 
        # 'PriceFrom': 
        # 'PriceTo': 
        # 'ItemMin': 
        # 'ItemMax': 
        # 'OfficeId': 
        # 'JudgmentId': 
        # 'PublicationDateFrom': [08.02.2019]
        # 'PublicationDateTo': 
        # 'StartDateFrom': 
        # 'StartDateTo': 
        # 'SumMin': 
        # 'SumMax': 
        # 'Vat': 
        # 'TypeOfAuction': 
        }

    soup = get_search_soup(data)
    
    rows = get_rows(soup)
    auctions = []
    for row in rows[1:]:
        cols = get_cols(row)
        if (len(cols) > 7):
            url = NODE_URL + cols[7].contents[1].get('href')
            cur_notice = notice.Notice(url)
            
            auction = {
                'date': cols[2].get_text(strip=True),
                'url' : url,
                'price' : parse_price(cols[6].get_text(strip=True)),
                'kw' : cur_notice.get_kw_number(),
                'address': cur_notice.get_address()
            }
            auctions.append(auction)
    return pd.DataFrame(auctions)

if __name__=="__main__":
    pd.options.display.max_colwidth = 100
    auctions = get_report()
    if not auctions.empty:
        print(auctions.sort_values("price")[['address', 'url']])
