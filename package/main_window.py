"""
main_window.py
Contains MainWindow class
"""

import sys
from functools import partial

from PySide6.QtCore import QStandardPaths, Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QMainWindow, QToolBar, QStyle, QFileDialog, QDialog, QSlider, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout, QMessageBox

from package.custom_video_widget import CustomVideoWidget


class MainWindow(QMainWindow):
    """User Interface (UI)"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyPlayer")
        self.current_movie_duration = 0
        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up user interface"""
        self.set_icons()
        self.create_widgets()
        self.create_actions()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def set_icons(self):
        """Sets UI icons"""
        self.open_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DriveCDIcon)
        self.play_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.pause_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
        self.previous_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward)
        self.back_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekBackward)
        self.forward_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekForward)
        self.stop_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        self.quit_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserStop)

    def create_widgets(self) -> None:
        """Creates UI widgets"""
        # central window
        self.central_window = QWidget()
        self.setCentralWidget(self.central_window)

        # player
        self.player = QMediaPlayer()
        self.video_widget = CustomVideoWidget()
        self.player.setVideoOutput(self.video_widget)
        self.audio_widget = QAudioOutput()
        self.player.setAudioOutput(self.audio_widget)

        # slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.lab_elapsed_time = QLabel("00:00")
        self.lab_remaining_time = QLabel("00:00")

        # toolbar and menu
        self.toolbar = QToolBar()
        self.file_menu = self.menuBar().addMenu("Fichier")
        self.play_menu = self.menuBar().addMenu("Lecteur")

    def create_actions(self):
        """Creates toolbar and menu actions"""
        self.act_open_tb = self.toolbar.addAction(self.open_icon, "Ouvrir la vidéo")
        self.act_open_menu = self.file_menu.addAction(self.open_icon, "Ouvrir la vidéo")
        self.act_play_tb = self.toolbar.addAction(self.play_icon, "Lire la vidéo")
        self.act_play_menu = self.play_menu.addAction(self.play_icon, "Lire la vidéo")
        self.act_pause_tb = self.toolbar.addAction(self.pause_icon, "Mettre en pause")
        self.act_pause_menu = self.play_menu.addAction(self.pause_icon, "Mettre en pause")
        self.act_previous_tb = self.toolbar.addAction(self.previous_icon, "Revenir au début")
        self.act_previous_menu = self.play_menu.addAction(self.previous_icon, "Revenir au début")
        self.act_back_tb = self.toolbar.addAction(self.back_icon, "-5 sec")
        self.act_back_menu = self.play_menu.addAction(self.back_icon, "Reculer de 5 secondes")
        self.act_forward_tb = self.toolbar.addAction(self.forward_icon, "+5 sec")
        self.act_forward_menu = self.play_menu.addAction(self.forward_icon, "Avancer de 5 secondes")
        self.act_stop_tb = self.toolbar.addAction(self.stop_icon, "Arrêter la lecture")
        self.act_stop_menu = self.play_menu.addAction(self.stop_icon, "Arrêter la lecture")
        self.act_quit_menu = self.file_menu.addAction(self.quit_icon, "Quitter PyPlayer")

        for action in self.toolbar.actions():
            if action != self.act_open_tb:
                action.setDisabled(True)
        for action in self.play_menu.actions():
            action.setDisabled(True)

    def create_layouts(self) -> None:
        """Creates UI layouts"""
        self.main_layout = QVBoxLayout()
        self.slider_layout = QHBoxLayout()
        self.addToolBar(self.toolbar)

    def add_widgets_to_layouts(self) -> None:
        """Adds widgets to layouts in UI"""
        # main layout
        self.central_window.setLayout(self.main_layout)
        self.main_layout.addWidget(self.video_widget)
        self.main_layout.addLayout(self.slider_layout)

        # slider layout
        self.slider_layout.addWidget(self.lab_elapsed_time)
        self.slider_layout.addWidget(self.slider)
        self.slider_layout.addWidget(self.lab_remaining_time)

        # stretch
        self.main_layout.setStretchFactor(self.video_widget, 1)

    def setup_connections(self) -> None:
        """Connects actions, shortcuts and widgets to functions"""
        self.player.playbackStateChanged.connect(self.update_buttons)
        self.player.mediaStatusChanged.connect(self.handle_media_status)

        # Actions
        self.act_open_tb.triggered.connect(self.open_video)
        self.act_open_menu.triggered.connect(self.open_video)
        self.act_play_tb.triggered.connect(self.player.play)
        self.act_play_menu.triggered.connect(self.player.play)
        self.act_pause_tb.triggered.connect(self.player.pause)
        self.act_pause_menu.triggered.connect(self.player.pause)
        self.act_previous_tb.triggered.connect(partial(self.player.setPosition, 0))
        self.act_previous_menu.triggered.connect(partial(self.player.setPosition, 0))
        self.act_back_tb.triggered.connect(self.go_back_5_sec)
        self.act_forward_tb.triggered.connect(self.go_forward_5_sec)
        self.act_stop_tb.triggered.connect(self.player.stop)
        self.act_stop_menu.triggered.connect(self.player.stop)
        self.act_quit_menu.triggered.connect(self.exit_player)

        # Slider necessary connections
        self.player.positionChanged.connect(self.update_slider)
        self.player.durationChanged.connect(self.update_slider_range)
        self.slider.sliderMoved.connect(self.set_video_position)

        # Back_5_sec button necessary connection
        self.player.positionChanged.connect(self.update_buttons)

        # Full screen
        # self.video_widget.

        # Keyboard shortcuts
        QShortcut(QKeySequence("Space"), self, self.toggle_pause)
        QShortcut(QKeySequence("Left"), self, self.go_back_5_sec)
        QShortcut(QKeySequence("Right"), self, self.go_forward_5_sec)
        QShortcut(QKeySequence("Esc"), self.video_widget,
                  partial(self.video_widget.setFullScreen, False))
        self.act_open_menu.setShortcut("Ctrl+O")
        self.act_stop_menu.setShortcut("Ctrl+W")
        self.act_previous_menu.setShortcut("P")
        self.act_quit_menu.setShortcut("Ctrl+Q")

    # End of UI
    # Below: methods in alphabetical order

    def exit_full_screen(self):
        pass

    def exit_player(self):
        """Displays a messageBox to ask to leave program ou not"""
        self.player.pause()
        msg_box = QMessageBox()
        msg_box.setText("Are you sure you want to leave PyPlayer?")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        choice = msg_box.exec()
        if choice == QMessageBox.StandardButton.No:
            msg_box.destroy()
        elif choice == QMessageBox.StandardButton.Yes:
            sys.exit()

    def go_back_5_sec(self):
        """Goes back 5 seconds"""
        self.player.setPosition(self.player.position() - 5000)

    def go_forward_5_sec(self):
        """Goes forward 5 seconds"""
        self.player.setPosition(self.player.position() + 5000)

    def handle_media_status(self, status):
        """Handles media status changes to reload video when reaching the end"""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.pause()

    def open_video(self):
        """Opens a video file with mp4 extension"""
        self.player.pause()
        file_dialog = QFileDialog(self)
        file_dialog.setMimeTypeFilters(["video/mp4"])
        movies_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
        file_dialog.setDirectory(movies_dir)
        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            movie = file_dialog.selectedUrls()[0]
            self.player.stop()
            self.player.setSource(movie)
            self.player.pause()
        else:
            self.player.play()

    def set_video_position(self, position):
        """Sets the video position based on the slider"""
        self.player.setPosition(position)

    def toggle_pause(self):
        """Toggles between pause and play"""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def update_buttons(self, state=None):
        if state is None:
            state = self.player.playbackState()

        """Updates button status, based on state"""
        self.act_play_tb.setDisabled(state == QMediaPlayer.PlaybackState.PlayingState)
        self.act_play_menu.setDisabled(state == QMediaPlayer.PlaybackState.PlayingState)
        self.act_pause_tb.setDisabled(state == QMediaPlayer.PlaybackState.PausedState)
        self.act_pause_menu.setDisabled(state == QMediaPlayer.PlaybackState.PausedState)
        self.act_stop_tb.setDisabled(state == QMediaPlayer.PlaybackState.StoppedState)
        self.act_stop_menu.setDisabled(state == QMediaPlayer.PlaybackState.StoppedState)
        self.act_previous_tb.setDisabled(state == QMediaPlayer.PlaybackState.StoppedState)
        self.act_previous_menu.setDisabled(state == QMediaPlayer.PlaybackState.StoppedState)
        self.act_back_tb.setDisabled(self.slider.value() == self.slider.minimum())
        self.act_back_menu.setDisabled(self.slider.value() == self.slider.minimum())
        self.act_forward_tb.setDisabled(self.slider.value() == self.slider.maximum())
        self.act_forward_menu.setDisabled(self.slider.value() == self.slider.maximum())

    def update_slider(self, position):
        """Updates the slider position"""
        self.slider.setValue(position)
        self.lab_elapsed_time.setText(format_time(position))
        self.lab_remaining_time.setText(format_time(self.current_movie_duration - position))

    def update_slider_range(self, duration):
        """Updates the slider range based on the video duration"""
        self.current_movie_duration = duration
        self.slider.setRange(0, duration)
        self.lab_remaining_time.setText(format_time(duration))


def format_time(duration_ms: int):
    """Formats duration in ms to a string mm:ss"""
    seconds = duration_ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    minutes %= 60
    seconds %= 60
    return f"{minutes:02}:{seconds:02}" if hours == 0 else f"{hours:02}:{minutes:02}:{seconds:02}"


if __name__ == '__main__':
    print("coucou")
