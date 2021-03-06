from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import HTTPError
from json import loads


def get_hexagon_json(sector, hexagon):
    try:
        with urlopen("https://travellermap.com/api/credits?sector=%s&hex=%s" % (quote(sector), hexagon)) as url:
            json = loads(url.read().decode())
        return json
    except HTTPError:
        return -1


def get_jump_json(sector, hexagon, jumps):
    try:
        with urlopen("https://travellermap.com/data/%s/%s/jump/%d" % (quote(sector), hexagon, jumps)) as url:
            json = loads(url.read().decode())
        return json
    except HTTPError:
        return -1

# TODO Error Handling
# TODO Make into full library?
