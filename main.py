import sys
import random

from song import SONGS
from functools import partial 
from vinyl import VinylRecord

from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QVBoxLayout,
    QComboBox, 
    QPushButton, 
    QFrame,
 )

from PySide6.QtCore import Qt

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("MoodFive")
window.resize(800,900)

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

def select_song(index, checked=False):
    active_song_label.setText(current_playlist[index])
    player_card.show()
    record.start_rotation()

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
