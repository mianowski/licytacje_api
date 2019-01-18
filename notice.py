from bs4 import BeautifulSoup
import re
class Notice():
    def __init__(self, date, price, url, location=None, auction_type=None):
        self.date = date
        self.price = price
        self.url = url
        self.location = location
        self.auction_type = auction_type

    def __repr__(self):
        return str([self.date, self.price, self.url])

def get_preview(details_soup):
    return details_soup.find("div", {"id": "Preview"})

def get_important(preview_soup):
    return [item.get_text() for item in preview_soup.find_all("strong")]

def get_kw_number(preview_soup):
    number = None
    importants = get_important(preview_soup)
    kw_list = list(filter(is_kw_number, importants))
    if kw_list:
        number = kw_list[0]

    return number


def get_address(preview_soup):
    raise NotImplementedError

def is_kw_number(string):
    return re.match(r'^\w{2}\d\w/\d{8}/\d$', string)
