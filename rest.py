import platform
import sys
import os
import requests
import unicodedata
import urllib.parse


import re
from babel.numbers import parse_decimal

import pandas as pd
from datetime import date
from datetime import datetime

import notice
from bs_helpers import make_soup
from database import open_db, populate_db
import sqlite3

NODE_URL = "http://www.licytacje.komornik.pl"

def get_search_soup(data):
    return make_soup(requests.post(NODE_URL+"/Notice/Search", data=data))

def get_notice_soup(id):
    return make_soup(requests.get(NODE_URL+"/Notice/Details/"+str(id)))

def get_soup(url):
    return make_soup(requests.get(url))



def get_rows(html_soup):
    return html_soup.find_all("tr")
    
def get_cols(row):
    return row.find_all("td")

def get_notices(html_soup):
    notices = html_soup.find_all("a", href=lambda href: href and "/Notice/Details" in href)
    return [ NODE_URL+str(notice.get("href")) for notice in notices]

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
        if (len(cols) > 7):
            
            url = NODE_URL + cols[7].contents[1].get('href')
            cur_notice = notice.Notice(url)
            auction = {
                'date': datetime.strptime(cols[2].get_text(strip=True),"%d.%m.%Y"),
                'url' : url,
                'price' : parse_price(cols[6].get_text(strip=True)),
                'kw' : cur_notice.get_kw_number(),
                'address': cur_notice.get_address()
            }
            auction['id'] = auction['date'].strftime("%Y%m%d")+"-"+str(auction["price"].to_integral_exact())
            auctions.append(auction)

            file_path = os.path.join("notices", auction['id'])
            cur_notice.save_to_file(file_path)
    return auctions

if __name__=="__main__":
    
    
    data_list = [
        {
            'Type': ['1'], 
            'City': ['Wrocław'],
            # 'PublicationDateFrom': [get_current_date()]
            # 'PublicationDateFrom': ['12.04.2019']
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
        },
        {
            'Type': ['1'], 
            'City': ['Wrocławiu']
        }
        ]

    auctions = sum(map(get_report, data_list),[])
    try:
        with open_db() as con:
            table_name = 'auctions'

            populate_db(auctions, table_name, con)
    except sqlite3.IntegrityError as e:
        print(e.args)


    import pandas as pd
    auctions_df = pd.DataFrame(auctions)
    pd.options.display.max_colwidth = 100
    if not auctions_df.empty:
        print(auctions_df.sort_values("price")[['address', 'url']])
