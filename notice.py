from bs4 import BeautifulSoup
import re
import requests
from bs_helpers import make_soup
class Notice():
    def __init__(self, url):
        self.url = url
        self.details = self.get_details(url)
        self.preview = self.get_preview(self.details)
        self.address = self.get_address()

    def __repr__(self):
        return str(self.url)

    def get_details(self, url):
        return make_soup(requests.get(url))


    def get_preview(self, details_soup):
        return details_soup.find("div", {"id": "Preview"})

    def get_important(self, preview_soup):
        return [item.get_text() for item in preview_soup.find_all("strong")]

    def get_kw_number(self):
        number = None
        importants = self.get_important(self.preview)
        kw_list = list(filter(is_kw_number, importants))
        if kw_list:
            number = kw_list[0]

        return number


    def get_address(self):
        address_regex = re.compile(r"(?:położone)(?:j|go)(?: przy)?(?::)? (.*) (.*)(?:, dla)")
        address = ""
        try:
            address = address_regex.search(self.preview.get_text()).groups()
        except:
            pass
        return address


def is_kw_number(string):
    return re.match(r'^\w{2}\d\w/\d{8}/\d$', string)

if __name__=="__main__":
    address_regex = re.compile(r"(?:położone)(?:j|go)(?: przy)?(?::)? (.*) (.*)(?:, dla)")
    text_0 = "Komornik Sądowy przy Sądzie Rejonowym dla Wrocławia-Fabrycznej Tomasz Kinastowski na podstawie art. 953 kpc podaje do publicznej wiadomości, że w dniu 27-02-2019 o godz. 09:15 w budynku Sądu Rejonowego dla Wrocławia-Fabrycznej z siedzibą przy Świebodzka 5, 50-047 Wrocław, pokój 201, odbędzie się druga licytacja ułamkowej części nieruchomości należącej do dłużnika: Mieczkowska Ewa, położonej przy Jeżowska 46, 54-049 M. Wrocław, dla której SĄD REJONOWY WROCŁAW IV WYDZIAŁ KSIĄG WIECZYSTYCH prowadzi księgę wieczystą o numerze WR1K/00010199/4."
    text_1 = " Komornik Sądowy   (dawniej Rew.XII)przy Sądzie Rejonowym dla Wrocławia-KrzykówBartosz BorkowskiZ-ca Asesor Anna Tomków-Bąk Kancelaria Komornicza we Wrocławiu50-425 Wrocław ul.Krakowska 19-23tel.793402989  e-mail: sekretariat@komornik.wroclaw.plKm 2022/17L I C Y T A C J A  O D W O Ł A N A !OBWIESZCZENIE O PIERWSZEJ LICYTACJI NIERUCHOMOŚCI nr KW WR1K/00140239/7Komornik Sądowy przy Sądzie Rejonowym dla Wrocławia-Krzyków Bartosz Borkowski Z-ca Asesor Anna Tomków-Bąk  (tel. 793 402 989) na podstawie art. 953 kpc podaje do publicznejwiadomości, że: w dniu 31-01-2019r. o godz. 10:00  w budynku Sądu Rejonowego dla Wrocławia-Krzyków mającego siedzibę przy ul.Podwale 30 we Wrocławiu w sali nr  133, odbędzie się pierwsza licytacja lokalu mieszkalnego  należącego do dłużnika: Ewa Żurawska stanowiącą odrębną nieruchomość oraz udział związany z własnością lokalu położonego: 52-204 Wrocław, ul. Obrońców Poczty Gdańskiej 64/1, dla którego Sąd Rejonowy dla Wrocławia-Krzyków IV Wydział Ksiąg Wieczystych prowadzi księgę wieczystą nr KW WR1K/00140239/7.Lokal mieszkalny na parterze i piętrze wielorodzinnego, trzykondygnacyjnego / w tym użytkowe poddasze / , wzniesionego w roku 2000 budynku wykonanego w systemie tradycyjnym wchodzącym skład w skład zespołu mieszkaniowego o charakterze  kondominium zlokalizowanego przy ulicach Ułańskiej i Obrońców Poczty Gdańskiej .Lokal składa się z  czterech pokoi , kuchni , 2 łazienek , hallu , przedpokoju i wiatrołapu . Powierzchnia użytkowa lokalu 93,64 m2. Do lokalu przynależy komórka nr 28 o powierzchni 3,75 m2  a ponadto właściciel lokalu nr 1 posiada prawo do wyłącznego  korzystania z dwóch ogródków o powierzchniach 12,80 m2 oraz 65,30 m2 . Wyposażenie w media pełne . Z  własnością lokalu  łączy się  udział  wynoszący  340/10000 w nieruchomości objętej  księgą  wieczystą  KW nr  WR1K/00091657/4. Zgodnie z zapisem obowiązującego  planu  zagospodarowania przestrzennego teren na  którym położona jest  przedmiotowa nieruchomość to teren zabudowy mieszkaniowej jedno- i  wielorodzinnej .Obecny sposób wykorzystania nieruchomości jest zgodny z przeznaczeniem terenu  w planie zagospodarowania przestrzennego .Suma oszacowania wynosi 350 000,00zł, zaś cena wywołania jest równa 3/4 sumy oszacowania i wynosi     262 500,00zł.  Licytant przystępujący do przetargu powinien złożyć rękojmię w wysokości jednej dziesiątej sumy oszacowania, to jest 35 000,00zł. Rękojmia powinna być wpłacona na konto komornika:ING Bank Śląski S.A. Oddział we Wrocławiu 48 1050 1575 1000 0023 5320 2100z dopiskiem:"
    print(re.search(address_regex, text_0).groups())
    print(re.search(address_regex, text_1).groups())
