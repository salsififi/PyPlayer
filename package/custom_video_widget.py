"""
custom_video.py
A class necessary to define what happens when mouse is double-clicked on the video widget
"""

from PySide6.QtMultimediaWidgets import QVideoWidget


class CustomVideoWidget(QVideoWidget):
    def mouseDoubleClickEvent(self, event):
        if self.isFullScreen():
            self.setFullScreen(False)
        else:
            self.setFullScreen(True)
        event.accept()
