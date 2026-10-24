import json 

from urllib.parse import urlencode
from urllib.request import urlopen

parameters = {
    "term": "Losing My Religion REM",
    "entity": "song",
    "country": "NL",
    "limit": "5",
}

url = "https://itunes.apple.com/search?" + urlencode(parameters)

with urlopen(url, timeout=10) as response:
    data = json.load(response)

for track in data["results"]:
    print("Song:", track["trackName"])
    print("artist:",  track["artistName"])
    print("album:",  track["collectionName"])
    print("Cover:", track.get("artworkUrl100", "No cover available"))
    print()