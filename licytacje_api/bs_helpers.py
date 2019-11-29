from bs4 import BeautifulSoup

def make_soup(result):
    return BeautifulSoup(result.content, 'html.parser')