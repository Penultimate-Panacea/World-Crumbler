from urllib.parse import quote
from urllib.request import urlopen
from json import loads


def get_hexagon_json(sector, hexagon):
    with urlopen("https://travellermap.com/data/%s/%s" % (quote(sector), hexagon)) as url:
        json = loads(url.read().decode())
    return json


def get_jump_json(sector, hexagon, jumps):
    with urlopen("https://travellermap.com/data/%s/%s/jump/%d" % (quote(sector), hexagon, jumps)) as url:
        json = loads(url.read().decode())
    return json


# TODO Error Handling
# TODO Make into full library?
