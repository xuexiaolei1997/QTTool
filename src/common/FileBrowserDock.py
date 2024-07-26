import os
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QMenu, QAction, QDockWidget

class FileBrowserDock(QDockWidget):

    # Signal: emit file path selected
    fileSelected = pyqtSignal(str)

    def __init__(self, parent: QDockWidget=None, directory="./"):
        super(FileBrowserDock, self).__init__('File Browser', parent)
        self.parent = parent
        self.directory = directory
        self.parent.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.model = QFileSystemModel()
        self.model.setRootPath(directory)

        # Create QTreeView & Set Model
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.model)
        self.file_tree.setRootIndex(self.model.index(directory))  # root dir
        self.file_tree.setSortingEnabled(True)  # sorted enabled

        # Define QTreeView CSS
        self.file_tree.setStyleSheet("""
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
        self.file_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.open_context_menu)

        # Set QTreeView into QDockWidget
        self.parent.setWidget(self.file_tree)
    
    def open_context_menu(self, position):
        index = self.file_tree.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu()
        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.open_file(index))
        menu.addAction(open_action)

        menu.exec_(self.file_tree.viewport().mapToGlobal(position))

    def open_file(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.fileSelected.emit(file_path)
        else:
            print(f"Cannot open: {file_path}")
