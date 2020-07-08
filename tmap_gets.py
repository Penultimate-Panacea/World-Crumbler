from urllib.parse import quote
from urllib.request import urlopen
from json import loads


def get_json(sector, hexagon):
    with urlopen("https://travellermap.com/api/credits?sector=%s&hex=%s" % (quote(sector), hexagon)) as url:
        data = loads(url.read().decode())
    return data