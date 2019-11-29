import urllib.parse

def get_gmaps_link(address: str):
    return "https://maps.google.com/maps/place/" + address.replace(" ", "+")

def get_osm_link(address: str):
    return "https://www.openstreetmap.org/search?query=" + urllib.parse.quote_plus(address)


if __name__=="__main__":
    address = "Rynek, Wrocław"
    print(get_gmaps_link(address))
    print(get_osm_link(address))