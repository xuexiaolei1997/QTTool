import os
import chardet
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget

class AnalysisData(QWidget):
    def __init__(self, file_path=""):
        super().__init__()