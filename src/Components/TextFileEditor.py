import os
import chardet
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget

from UI.UI_FileEditor import Ui_FileEditor

class TextFileEditor(Ui_FileEditor, QWidget):
    def __init__(self, file_path="") -> None:
        super().__init__()
        self.setupUi(self)

        # Current file path
        self.file_path = file_path
        self.file_content = ""

        # File size
        self.max_file_size = 4  # Unit: M
        
        # Action
        self.textEdit_main_editor.textChanged.connect(self.change_text)
        self.Button_save.clicked.connect(self.save_file)

        # Init open
        self.open_file(file_path)

    def update_file_info(self, file_path, title, file_content):
        self.file_path = file_path
        self.label_file_path.setText(title)
        self.file_content = file_content
        self.textEdit_main_editor.setText(self.file_content)

    def change_text(self):
        self.file_content = self.textEdit_main_editor.toPlainText()
    
    def open_file(self, file_path):
        if file_path == "":
            if self.file_path == "":  # New
                self.update_file_info(file_path, "Untitled", "")
            return
        
        # Validation
        assert os.path.isfile(file_path), QMessageBox.critical(self, "Error", f"Path: {file_path} not include  file!", QMessageBox.StandardButton.Close)
        assert os.path.exists(file_path), QMessageBox.critical(self, "Error", f"File: {file_path} is not exists!", QMessageBox.StandardButton.Close)
        
        # Check file size
        file_info = os.stat(file_path)
        file_size = file_info.st_size
        if file_size * 8 / 1024 / 1024 > self.max_file_size:
            QMessageBox.critical(self, "Eroor", f"Opened file should be smaller than {self.max_file_size} M.", QMessageBox.StandardButton.Ok)
            return

        # Ensure encoding type
        with open(file_path, 'rb') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
        
        # File content
        with open(file_path, 'r', encoding=encoding) as f:
            file_content = f.read()
        
        self.update_file_info(file_path, file_path, file_content)
    
    def save_file(self):
        if self.file_path == "":
            self.file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "./", "All Files (*);;Text Files (*.txt)")
            if self.file_path == "":
                return
        with open(self.file_path, 'w', encoding="utf8") as f:
            f.write(self.file_content)
        self.label_file_path.setText(self.file_path)

    def close(self) -> bool:
        if self.textEdit_main_editor.toPlainText() != self.file_content:
            box = QMessageBox(self)
            box.setWindowTitle("QMessageBox Demo")
            box.setText("Are you sure you want to do this?")
            box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            box.buttonClicked.connect(self.handleButtonClick)
            box.exec_()
        return super().close()
    
    def handleButtonClick(self, button):
        if button.text() == "Yes":
            self.save_file()
        elif button.text() == "No":
            pass
