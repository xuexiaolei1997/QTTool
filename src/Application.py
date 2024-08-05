import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from MainWindow import MainWindow

class Application(QApplication):

    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.setApplicationName("Hello")
        self.setWindowIcon(QIcon(":/icons/resources/icons/排版版面.png"))
    
    def exec(_):
        self = Application
        self.mainWindow = MainWindow()
        self.mainWindow.show()
        return QApplication.exec()

import pictures_rc
