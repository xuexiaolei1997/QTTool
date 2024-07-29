import os
import chardet
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget

from UI.UI_FileEditor import Ui_FileEditor

class TextFileEditor(Ui_FileEditor, QWidget):
    def __init__(self, file_path="") -> None:
        super().__init__()
        self.setupUi(self)
        self.file_path = file_path
        self.file_content = ""
        
        self.textEdit_main_editor.textChanged.connect(self.change_text)
        self.Button_save.clicked.connect(self.save_file)

        self.open_file(file_path)

    def change_text(self):
        self.file_content = self.textEdit_main_editor.toPlainText()
    
    def open_file(self, file_path):
        if file_path == "":
            if self.file_path == "":  # New
                self.file_path = file_path
                self.label_file_path.setText("Untitled")
                self.file_content = ""
                self.textEdit_main_editor.setText(self.file_content)
            return
        
        assert os.path.isfile(file_path), QMessageBox.critical(self, "Error", f"Path: {file_path} not include  file!", QMessageBox.StandardButton.Close)
        assert os.path.exists(file_path), QMessageBox.critical(self, "Error", f"File: {file_path} is not exists!", QMessageBox.StandardButton.Close)
        
        # encoding
        with open(file_path, 'rb') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
        
        # file content
        with open(file_path, 'r', encoding=encoding) as f:
            file_content = f.read()
        
        self.file_path = file_path
        self.label_file_path.setText(file_path)
        self.file_content = file_content
        self.textEdit_main_editor.setText(file_content)
        
    
    def show_table_view(self):
        pass

    def analysis_data(self):
        pass
    
    def save_file(self):
        if self.file_path == "":
            self.file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "./", "All Files (*);;Text Files (*.txt)")
            if self.file_path == "":
                return
        with open(self.file_path, 'w', encoding="utf8") as f:
            f.write(self.file_content)
        self.label_file_path.setText(self.file_path)
