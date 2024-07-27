import os
import chardet
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QMdiSubWindow, QMessageBox, QFileDialog
from UI.UI_FileEditor import Ui_FileEditor


class FileEditorController(Ui_FileEditor, QWidget):
    def __init__(self, file_path="") -> None:
        super().__init__()
        self.setupUi(self)
        self.file_path = file_path
        self.file_content = ""

        self.Button_open.clicked.connect(self.choose_file)
        self.Button_save.clicked.connect(self.save_file)

        self.open_file(file_path)
    
    def choose_file(self,):
        file_path, file_type = QFileDialog.getOpenFileName(self, "Select File", "./")

        assert os.path.isfile(file_path), QMessageBox.critical(self, "Error", f"ath {file_path} is not a file!", QMessageBox.StandardButton.Close)
        assert os.path.exists(file_path), QMessageBox.critical(self, "Error", f"File {file_path} is not exists!", QMessageBox.StandardButton.Close)
        

        if file_path == "":
            return
        else:
            self.file_path = file_path
            self.open_file(file_path)
    
    def open_file(self, file_path):
        if file_path == "":
            self.file_path = file_path
            self.label_file_path.setText("Untitled")
            self.file_content = ""
            self.textEdit_main_editor.setText(self.file_content)
            return
        
        assert os.path.isfile(file_path), QMessageBox.critical(self, "Error", f"File {file_path} is not exists!", QMessageBox.StandardButton.Close)
        assert os.path.exists(file_path), QMessageBox.critical(self, "Error", f"File {file_path} is not exists!", QMessageBox.StandardButton.Close)
        
        with open(file_path, 'rb') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
        
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
            QMessageBox.critical(self, "Error", "")
        with open(self.file_path, 'w') as f:
            f.write(self.file_content)
