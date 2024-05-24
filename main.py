"""
PyNotes
A very basic video player (mp4)
Exercise from the course "Le framework PySide" on the Docstring website (www.docstring.fr)

Author: Simon Salvaing
Date: 2024-05-23
"""

from PySide6.QtWidgets import QApplication

from package.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec()
