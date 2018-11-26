class Notice():
    def __init__(self, date, price, url, location=None, auction_type=None):
        self.date = date
        self.price = price
        self.url = url
        self.location = location
        self.auction_type = auction_type

    def __repr__(self):
        return str([self.date, self.price, self.url])