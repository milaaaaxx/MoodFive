import sys
import random
import json
from song import SONGS
from functools import partial 


from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QVBoxLayout,
    QComboBox, 
    QPushButton, 
    QFrame,
 )

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import Qt, QUrl
from vinyl import VinylRecord
from urllib.parse import urlencode
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest,
    QNetworkReply,
)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("MoodFive")
window.resize(800,900)
network = QNetworkAccessManager(window)
audio_output = QAudioOutput(window)
audio_output.setVolume(0.35)

player = QMediaPlayer(window)
player.setAudioOutput(audio_output)

layout = QVBoxLayout(window)
layout.setAlignment(Qt.AlignmentFlag.AlignTop)
layout.setContentsMargins(30, 30, 30, 30)
layout.setSpacing(12)

title = QLabel("Whats the vibe today?:>")
title.setStyleSheet("font-size: 28px; font-weight: bold;")
layout.addWidget(title)

subtitle = QLabel("Pick your mood, We'll find your next 5 songs to obsess over:3")
subtitle.setWordWrap(True)
layout.addWidget(subtitle)

mood_selector = QComboBox()
mood_selector.addItems(list(SONGS))
layout.addWidget(mood_selector)

soundtrack_button = QPushButton("Soundtracks")
layout.addWidget(soundtrack_button)

player_card = QFrame()
player_card.setObjectName("playerCard")

player_layout = QVBoxLayout(player_card)
player_layout.setContentsMargins(24, 24, 24, 24)
player_layout.setSpacing(16)

player_caption = QLabel("YOUR DAILY SOUNDTRACK")
player_caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
player_layout.addWidget(player_caption)

record = VinylRecord()

player_layout.addWidget(
    record,
    alignment=Qt.AlignmentFlag.AlignHCenter,
)

active_song_label = QLabel("YOURR NEXTT OBSESSIONNN GOESS HERE")
active_song_label.setWordWrap(True)
active_song_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
active_song_label.setStyleSheet("font-size: 24px; font-weight: bold;")
player_layout.addWidget(active_song_label)

player_card.setStyleSheet("""
      QFrame#playerCard {
         background-color: #273345;
         color: #ffffff;
         border-radius: 20px;
        }
      QFrame#playerCard QLabel {
         color: #ffffff;
        }
    """)
layout.addWidget(player_card)
player_card.hide()

other_songs_layout = QVBoxLayout()
other_songs_layout.setSpacing(8)
layout.addLayout(other_songs_layout)

current_playlist = []

def sync_record(_=None):
    is_playing = (
        player.playbackState()
        == QMediaPlayer.PlaybackState.PlayingState
    )

    is_buffered = (
        player.mediaStatus()
        == QMediaPlayer.MediaStatus.BufferedMedia
    )

    if is_playing and is_buffered:
        record.animation_timer.start()
    else:
        record.stop_rotation()

def check_preview_position(position):
    if position >= 15000:
        player.stop()

def show_audio_error(error, message):
    record.stop_rotation()
    player_caption.setText("coudnttt playy thiss previeuww")
    print("audio error", message)

player.playbackStateChanged.connect(sync_record)
player.mediaStatusChanged.connect(sync_record)
player.positionChanged.connect(check_preview_position)
player.errorOccurred.connect(show_audio_error)

def fetch_bytes(url, song, on_succes):
    request = QNetworkRequest(QUrl(url))
    request.setTransferTimeout(10000)

    reply = network.get(request)

    def finished():
        try:
            if active_song_label.text() != song:
                return
            if reply.error() != QNetworkReply.NetworkError.NoError:
                player_caption.setText("Coudnt load the cover MY BADD:((")
                print(reply.errorString())
                return

            image_or_json = bytes(reply.readAll())
            on_succes(image_or_json)
        
        finally:
            reply.deleteLater()            

    reply.finished.connect(finished)

def clean_name(text):
    return "".join(character for character in text.casefold() if character.isalnum())

def load_cover(song):
    player.stop()
    player.setSource(QUrl())

    record.stop_rotation()
    record.cover = QPixmap()
    record.update()
    player_caption.setText("FINDINN YOURRR ALBUM COVER<3")

    title, separator, artist = song.partition(" - ")

    if not separator: 
        player_caption.setText("Checkkk the songtitle an artist")
        return
    
    parameters = {
        "term": f"{title} {artist}",
        "entity": "song",
        "country": "NL",
        "limit": 10,
    }

    search_url = "https://itunes.apple.com/search?" + urlencode(parameters)

    if song == "Tired - beabadoobee":
        search_url = (
             "https://itunes.apple.com/lookup"
            "?id=1444723452&country=NL"
        )

    def receive_search(raw_data):
        try:
            results = json.loads(raw_data)["results"]
        except (ValueError, KeyError, TypeError):
            player_caption.setText("woopsie coudnt read the results")
            return
         
        track = None
        
        for candidate in results:
            same_title = clean_name(candidate.get("trackName", "")) == clean_name(title)
            found_artist = candidate.get("artistName", "")

            if found_artist == 'Curtis "50 Cent" Jackson':
                found_artist = "50 Cent"

            same_artist = clean_name(found_artist) == clean_name(artist)

            if same_artist and same_title:
                track = candidate
                break
        
        if track is None:
            player_caption.setText("WOAH, no match SWRYY<3")
            return
        
        cover_url = track.get("artworkUrl100")

        if not cover_url:
            player_caption.setText("no cover available for this song SWRRYYYY")
            return
        
        def receive_image(image_data):
            if not record.set_cover_data(image_data):
                player_caption.setText("Coudnt read teh cover image...")
                return

            player_caption.setText(
                track.get("collectionName", "YOUR SOUNDTRACK")
            )

            preview_url = track.get("previewUrl")

            if not preview_url:
                player_caption.setText("no preview available for this song")
                return

            player.setSource(QUrl(preview_url))
            player.play()

        fetch_bytes(cover_url, song, receive_image)
    
    fetch_bytes(search_url, song, receive_search)


def select_song(index, checked=False):
    selected_song = current_playlist[index]
    active_song_label.setText(selected_song)
    player_card.show()

    load_cover(selected_song)

    while other_songs_layout.count() > 0 :
        item = other_songs_layout.takeAt(0)
        item.widget().deleteLater()
    
    for song_index, song in enumerate(current_playlist):
        if song_index == index:
            continue
        
        song_button = QPushButton(song)
        song_button.setMinimumHeight(48)
        song_button.setStyleSheet("""
          QPushButton {
             text-align: left;
             padding:12px;
             border-radius: 10px;
             background-color: #273345;
             color: #ffffff;
          }

          QPushButton:hover {
             background-color: #40516b;
             }
         """) 
        song_button.clicked.connect(
            partial(select_song, song_index)
        )
        other_songs_layout.addWidget(song_button)

def show_mood():
    selected_mood = mood_selector.currentText()
    matching_songs = SONGS[selected_mood]
    current_playlist.clear()
    current_playlist.extend(random.sample(matching_songs, 5))

    select_song(0)

soundtrack_button.clicked.connect(show_mood)

window.show()
sys.exit(app.exec()) 
