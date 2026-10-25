from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QPixmap, QPainterPath
from PySide6.QtWidgets import QWidget


class VinylRecord(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(160, 160)
        self.angle = 0
        self.cover = QPixmap()

        self.animation_timer = QTimer(self)
        self.animation_timer.setInterval(16)
        self.animation_timer.timeout.connect(self.rotate_step)



    def start_rotation(self):
        self.angle = 0
        self.update()
        self.animation_timer.start()
        

    def rotate_step(self):
        self.angle = (self.angle + 3) % 360
        self.update()

    def stop_rotation(self):
        self.animation_timer.stop()

    def set_cover_data(self, image_data):
        image = QPixmap()
        
        if not image.loadFromData(image_data):
            return False

        self.cover = image.scaled(
            64,
            64,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.update()
        return True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.translate(80, 80)
        painter.rotate(self.angle)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#161616"))
        painter.drawEllipse(-76, -76, 152, 152)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor("#383838"), 1))
        
        for radius in [68, 59, 50, 41]:
            painter.drawEllipse(
                -radius,
                -radius,
                radius * 2,
                radius * 2, 
            )
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#d7ff85"))
        painter.drawEllipse(-32, -32, 64, 64)
        

        if self.cover.isNull():

            painter.setPen(QColor("#161616"))
            painter.setFont(QFont("Sans Serif", 9, QFont.Weight.Bold))
            painter.drawText(
            QRect(-30, -30, 60, 60),
            Qt.AlignmentFlag.AlignCenter,
            "MOOD\nFIVE",
        )
        else:
            painter.save()

            circle = QPainterPath()
            circle.addEllipse(-32, -32, 64, 64)
            painter.setClipPath(circle)

            painter.drawPixmap(
                -self.cover.width() // 2,
                -self.cover.height() // 2,
                self.cover,                 
           )
           
            painter.restore()
 
        painter.end()