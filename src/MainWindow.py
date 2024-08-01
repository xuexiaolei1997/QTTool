import os
import sys
from queue import Queue

from PyQt5.QtWidgets import *

from common.Stack import Stack
from Components.FileBrowserDock import FileBrowserDock
from Components.TextFileEditor.TextFileEditor import TextFileEditor
from Components.MusicPlayer.MusicPlayer import MusicPlayer
from UI.UI_MainWindow import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.setAcceptDrops(True)

        # >> Define data
        self.data = Stack()

        # >> Setup UI
        self.setupUi(self)

        # >> File
        self.actionNew.triggered.connect(self.create_file)              # New
        self.actionOpen.triggered.connect(self.open_file)               # Open
        self.actionOpen_Folder.triggered.connect(self.open_folder)      # Open Folder
        # Save
        # Save as
        self.actionClose.triggered.connect(self.close)                  # Close

        # >> Edit
        
        # >> View
        self.music_player = None
        self.actionMusic.triggered.connect(self.open_music_player)

        # >> Help
        self.actionAbout.triggered.connect(self.show_about)

        self.show()
    
    def create_file(self):
        self.create_file_window(file_path="")
    
    def open_file(self):
        file_path, file_type = QFileDialog.getOpenFileName(self, "Select File", "./")
        if file_path:
            self.create_file_window(file_path)

    def create_file_window(self, file_path=""):
        """
        Create a TextFileEditor(subWindow) in workspace(mdiArea).
        """
        fileEditor = TextFileEditor(file_path)
        self.workspace.addSubWindow(fileEditor)
        fileEditor.show()
    
    def open_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Folder", "./")
        self.file_browser_dock = FileBrowserDock(self.dockWidget_Left, directory)
        self.file_browser_dock.fileSelected.connect(self.create_file_window)
    
    def open_music_player(self):
        if self.music_player is None:
            self.music_player = MusicPlayer(self)
        self.music_player.show()
    
    def close(self):
        sys.exit()

    def show_about(self):
        QMessageBox.information(None, "About", "This is About!", QMessageBox.StandardButton.Close)
