import os
from PyQt5.QtCore import *

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

class FileTree(QTreeView):

    # Signal: emit file path selected
    fileSelected_Open = pyqtSignal(str)
    fileSelected_Analysis = pyqtSignal(str)

    def __init__(self, parent=None, directory="./") -> None:
        super().__init__(parent)
        self.parent_ = parent
        self.directory = directory

        self.model = QFileSystemModel()
        self.model.setRootPath(directory)

        # Create QTreeView & Set Model
        self.setModel(self.model)
        self.setRootIndex(self.model.index(directory))  # root dir
        self.setSortingEnabled(True)  # sorted enabled

        # Define QTreeView CSS
        self.setStyleSheet("""
            QTreeView {
                background-color: #f0f0f0;
                alternate-background-color: #e0e0e0;
                selection-background-color: #a0a0ff;
                selection-color: #ffffff;
            }
            QTreeView::item {
                padding: 5px;
            }
            QTreeView::item:selected {
                background-color: #4a90e2;
                color: white;
            }
        """)

        # Click Right
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)
    
    def open_context_menu(self, position):
        index = self.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu()
        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.open_file(index))
        menu.addAction(open_action)

        analysis_action = QAction("Analysis", self)
        analysis_action.triggered.connect(lambda: self.analysis_file(index))
        menu.addAction(analysis_action)

        menu.exec_(self.viewport().mapToGlobal(position))

    def open_file(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.fileSelected_Open.emit(file_path)
        else:
            print(f"Cannot open: {file_path}")
    
    def analysis_file(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.fileSelected_Analysis.emit(file_path)
        else:
            print(f"Cannot open: {file_path}")


if __name__ == "__main__":
    import sys
    import os
    from PyQt5.QtWidgets import QApplication
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    firetree = FileTree()
    firetree.show()
    sys.exit(app.exec())