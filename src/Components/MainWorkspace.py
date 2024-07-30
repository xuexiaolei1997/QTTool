import os
from PyQt5.QtGui import QDragLeaveEvent, QDragEnterEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMdiArea, QWidget

from UI.UI_MainWorkspace import Ui_MainWorkSpace

class MainWorkspace(Ui_MainWorkSpace, QMdiArea):
    def __init__(self, parent=None):
        super(MainWorkspace, self).__init__(parent)
        self.setupUi(self)
        self.allowed_enter_types = ["csv", "txt"]
        self.file_path = pyqtSignal(str)
        # self.setAcceptDrops(True)  # Enable drop events

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event) -> None:
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.file_path.emit(file_path)
        event.acceptProposedAction()