from bs4 import BeautifulSoup
import re
import requests
import logging

from .bs_helpers import make_soup


class Notice():
    def __init__(self, url):
        self.url = url
        self.details = self.get_details(url)
        self.preview = self.get_preview(self.details)
        self.address = self.get_address()

    def __repr__(self):
        return str(self.url)

    def save_to_file(self, path: str):
        with open(path, "w+") as f:
            f.write(self.preview.prettify())

    def get_details(self, url) -> BeautifulSoup:
        return make_soup(requests.get(url))

    def get_preview(self, details_soup: BeautifulSoup):
        return details_soup.find("div", {"id": "Preview"})

    def get_important(self, preview_soup: BeautifulSoup):
        return [item.get_text() for item in preview_soup.find_all("strong")]

    def get_kw_number(self):
        number = None
        importants = self.get_important(self.preview)
        kw_list = list(filter(is_kw_number, importants))
        if kw_list:
            number = kw_list[0]
        return number

    def get_address(self):
        address = self.details.find("input", {"id": "hidden_address"})['value']
        if address:
            return address
        return get_address_from_text(self.preview.get_text())


def get_address_from_text(text: str):
    address_regex = re.compile(
        r"(?:(?:(?:położon)(?:ej|ego|ym)(?: przy)?(?::)? )|(?:xxx przy )|(?:przy\\xa0))(.*?),(.*?)(?:,|dla| Sąd| wpisanego)")
    address = ""
    try:
        match = address_regex.search(text).group(0)
        match_groups = address_regex.search(text).groups()
        address = ''.join(match_groups)
    except:
        logging.error("Unable to find address for text: %s", text)
        pass
    return address


def is_kw_number(string):
    return re.match(r'^\w{2}\d\w/\d{8}/\d$', string)
