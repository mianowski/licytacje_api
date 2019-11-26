import os
import requests
import unicodedata
import urllib.parse

from babel.numbers import parse_decimal
from datetime import date
from datetime import datetime

import notice
from bs_helpers import make_soup


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
    import sqlite3
    import json
    from database import open_db, populate_db, create_db_table
    import pandas as pd


    def display_auctions(auctions):
        auctions_df = pd.DataFrame(auctions)
        pd.options.display.max_colwidth = 100
        if not auctions_df.empty:
            print(auctions_df.sort_values("price")[['address', 'url']])


    def save_auctions_to_db(auctions):
        try:
            with open_db() as con:
                table_name = 'auctions'
                create_db_table(table_name, {'id': 'varchar(16)', 'data': 'json'}, con)
                populate_db(auctions, table_name, con)
        except sqlite3.IntegrityError as e:
            print(e.args)    
    

    with open("config.json") as config_file:
        data_list = json.load(config_file)

    auctions = sum(map(get_report, data_list),[])
    save_auctions_to_db(auctions)
    display_auctions(auctions)
