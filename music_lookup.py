import sys
import json 

from urllib.parse import urlencode
from urllib.request import urlopen
from PySide6.QtWidgets import QApplication
from vinyl import VinylRecord 


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


if not data["results"]:
    print("no songs found woops:<")
    sys.exit()

track = data["results"][0]
cover_url = track.get("artworkUrl100")

if not cover_url:
    print("This result has no album cover")
    sys.exit()

print("Texting cover for:", track["trackName"], "-", track["collectionName"])

with urlopen(cover_url, timeout=10) as response:
    image_data = response.read()

app = QApplication(sys.argv)

record = VinylRecord()
record.setWindowTitle("Album cover test")

if not record.set_cover_data(image_data):
    print("coudnt read the image:<")
    sys.exit()

record.show()
record.start_rotation()

sys.exit(app.exec())