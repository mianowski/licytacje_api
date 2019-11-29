import sys
import json
import pprint
import sqlite3

from rest import get_report
from database import open_db, create_db_table, populate_db


def display_auctions(auctions):
    for auction in auctions:
        pprint.pprint(auction, indent=4)

def save_auctions_to_db(auctions):
    try:
        with open_db() as con:
            table_name = 'auctions'
            create_db_table(table_name, {'id': 'varchar(16)', 'data': 'json'}, con)
            populate_db(auctions, table_name, con)
    except sqlite3.IntegrityError as e:
        print(e.args)

def auctions():
    """
    Can be called in the form :
    python auctions.py config.json, where config.json is a file formed like
    [
        {
            'Type': ['1'], 
            'City': ['Wrocław'],
            'PublicationDateFrom': [get_current_date()]
            'PublicationDateFrom': ['12.04.2019']
            'JudgmentId': ['1103']
                    
            'CategoryId': []
            'MobilityCategoryId': 
            'PropertyCategoryId': 
            'City': Wrocław
            'tbx-province': 
            'ProvinceId': 
            'AuctionsDate': 
            'Words': 
            'PriceFrom': 
            'PriceTo': 
            'ItemMin': 
            'ItemMax': 
            'OfficeId': 
            'JudgmentId': 
            'PublicationDateFrom': [08.02.2019]
            'PublicationDateTo': 
            'StartDateFrom': 
            'StartDateTo': 
            'SumMin': 
            'SumMax': 
            'Vat': 
            'TypeOfAuction': 
        },
        {
            'Type': ['1'], 
            'City': ['Wrocławiu']
        }
        ]
    """
    with open(sys.argv[1]) as config_file:
        data_list = json.load(config_file)

    auctions = sum(map(get_report, data_list),[])
    auctions.sort(key=lambda auction: auction["price"])
    save_auctions_to_db(auctions)
    display_auctions(auctions)


if __name__=="__main__":
    auctions()


