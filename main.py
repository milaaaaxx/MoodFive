import sys
import random

from song import SONGS

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QComboBox, QPushButton
from PySide6.QtCore import Qt
app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("MoodFive")
window.resize(800,600)

layout = QVBoxLayout(window)
layout.setAlignment(Qt.AlignmentFlag.AlignTop)
layout.setContentsMargins(50, 120, 50, 80)

title = QLabel("Whats the vibe today?")
title.setStyleSheet("font-size: 28px; font-weight: bold;")
layout.addWidget(title)

subtitle = QLabel("Pick your mood, We'll find your next 5 songs to obsess over:3")
subtitle.setWordWrap(True)
layout.addWidget(subtitle)

mood_selector = QComboBox()
mood_selector.addItems(["Thriving","just chilling", "In my yearning era", "brain has 47 tabs open lol", "main character energy","running on 2%" ])
layout.addWidget(mood_selector)

soundtrack_button = QPushButton("Soundtracks")
layout.addWidget(soundtrack_button)

result_label = QLabel("Your soundtrack is waiting...")
result_label.setWordWrap(True)
layout.addWidget(result_label)

def show_mood():
    selected_mood = mood_selector.currentText()
    matching_songs = SONGS[selected_mood]
    selected_songs = random.sample(matching_songs, 5)

    result_text = "your soundtrack just dropped:\n\n"

    for number, song in enumerate(selected_songs, start=1):
        result_text += f"{number}. {song}\n"

    result_label.setText(result_text)

soundtrack_button.clicked.connect(show_mood)

window.show()
sys.exit(app.exec())