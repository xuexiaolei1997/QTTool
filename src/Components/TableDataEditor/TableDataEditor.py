import os
import re
import chardet
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from PyQt5.QtGui import *

from Components.TableDataEditor.UI_TableDataEditor import Ui_Form_TableEditor


class TableDataEditor(Ui_Form_TableEditor, QWidget):
    def __init__(self, file_path) -> None:
        super().__init__()
        self.file_path = file_path
