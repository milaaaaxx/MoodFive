import sys

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("MoodFive")
window.resize(800,600)

layout = QVBoxLayout(window)
layout.setAlignment(Qt.AlignmentFlag.AlignTop)
layout.setContentsMargins(50, 120, 50, 80)

title = QLabel("How are you feeling today?")
title.setStyleSheet("font-size: 28px; font-weight: bold;")
layout.addWidget(title)
subtitle = QLabel("Select your mood from the options below:")
subtitle.setWordWrap(True)
layout.addWidget(subtitle)

window.show()
sys.exit(app.exec())