import os
import sys
from queue import Queue

from PyQt5.QtWidgets import *

from common.Stack import Stack
from Components.FileBrowserDock import FileBrowserDock
from Components.TextFileEditor.TextFileEditor import TextFileEditor
from Components.MusicPlayer.MusicPlayer import MusicPlayer
from Components.Terminal.Terminal import Terminal
from Components.TabWidget.TabWidget import TabWidget
from Components.CDrawer.CDrawer import CDrawer
from UI.UI_MainWindow import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.setAcceptDrops(True)

        # >> Setup UI
        self.setupUi(self)
        self.extraUi()
        self.init_action()
    
    def extraUi(self):
        # Bottom
        self.tabWidget_Operation = TabWidget(self, "tabWidget_Operation", QTabWidget.West)
        self.dockWidget_Bottom.setWidget(self.tabWidget_Operation)
        self.tabWidget_Operation.show()

        # Right
        self.tabWidget_Draw = TabWidget(self, "tabWidget_Draw", QTabWidget.East)
        self.dockWidget_Draw.setWidget(self.tabWidget_Draw)
        self.tabWidget_Draw.show()
    
    def init_action(self):
        # >> File
        self.actionNewText_File.triggered.connect(self.create_text_file)    # New text
        self.actionOpenText_File.triggered.connect(self.open_text_file)     # Open text
        self.actionOpen_Folder.triggered.connect(self.open_folder)          # Open Folder
        self.actionClose.triggered.connect(self.close)                      # Close

        # >> Edit
        
        # >> View
        self.music_player = None
        self.actionMusicPlayer.triggered.connect(self.open_music_player)
        self.actionNew_Terminal.triggered.connect(self.open_terminal)

        # >> Help
        self.actionAbout.triggered.connect(self.show_about)
    
    def create_text_file(self):
        self.create_text_file_window(file_path="")
    
    def open_text_file(self):
        file_path, file_type = QFileDialog.getOpenFileName(self, "Select File", "./")
        if file_path:
            self.create_text_file_window(file_path)

    def create_text_file_window(self, file_path=""):
        """
        Create a TextFileEditor(subWindow) in workspace(mdiArea).
        """
        fileEditor = TextFileEditor(file_path)
        self.workspace.addSubWindow(fileEditor)
        fileEditor.show()
    
    def open_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Folder", "./")
        self.file_browser_dock = FileBrowserDock(self.dockWidget_Left, directory)
        self.file_browser_dock.fileSelected.connect(self.create_text_file_window)
    
    def open_music_player(self):
        if self.music_player is None:
            self.music_player = MusicPlayer(self)
            # self.rightDrawer = CDrawer(self,widget=self.music_player)
            # self.rightDrawer.setDirection(CDrawer.RIGHT)
        # self.rightDrawer.show()
        self.music_player.show()
    
    def open_terminal(self):
        if not self.dockWidget_Bottom.isVisible():
            self.dockWidget_Bottom.setVisible(True)

        terminal = Terminal(self, os.path.dirname(os.path.abspath(__file__)))
        added_index = self.tabWidget_Operation.addTab(terminal, "Terminal")
        self.tabWidget_Operation.setCurrentIndex(added_index)
        terminal.show()
    
    def close(self):
        sys.exit()

    def show_about(self):
        QMessageBox.information(None, "About", "This is About!", QMessageBox.StandardButton.Close)
