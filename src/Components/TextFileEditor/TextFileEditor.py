import os
import re
import chardet
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from PyQt5.QtGui import *

from Components.TextFileEditor.UI_FileEditor import Ui_FileEditor


class TextFileEditor(Ui_FileEditor, QWidget):
    def __init__(self, file_path="") -> None:
        super().__init__()
        self.setupUi(self)

        # Current file path
        self.file_path = file_path
        self.file_content = ""
        self.now_content = ""

        # File size
        self.max_file_size = 4  # Unit: M

        # Action
        self.textEdit_main_editor.textChanged.connect(self.change_text)
        self.Button_save.clicked.connect(self.save_file)

        qss_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qss', 'style.qss')
        if os.path.exists(qss_file_path):
            with open(qss_file_path, 'r', encoding='utf8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        
        self.lineEdit_Search.textChanged.connect(self.SearchFromText)

        # Init open
        self.open_file(file_path)

        # Search & Replace
        self.search_text = ""
        self.search_result_index_list = []
        self.current_search_index = None

        self.pushButton_SearchPrevious.clicked.connect(self.SearchPrevious)
        self.pushButton_SearchNext.clicked.connect(self.SearchNext)
        self.pushButton_Replace.clicked.connect(self.replace)
        self.pushButton_ReplaceAll.clicked.connect(self.replaceAll)
    
    # Search & Replace Function
    def SearchFromText(self):
        self.search_text = self.lineEdit_Search.text()
        if not self.search_text:
            return

        self.search_result_index_list = [match.start() for match in re.finditer(re.escape(self.search_text), self.textEdit_main_editor.toPlainText())]
        if self.search_result_index_list:
            self.current_search_index = 0
            self.jump2loc()
        else:
            self.current_search_index = None
            self.label_SearchIndex.setText("No Result")

    def SearchPrevious(self):
        if self.current_search_index is not None and self.current_search_index > 0:
            self.current_search_index -= 1
            self.jump2loc()

    def SearchNext(self):
        if self.current_search_index is not None and self.current_search_index < len(self.search_result_index_list) - 1:
            self.current_search_index += 1
            self.jump2loc()

    def replace(self):
        replaced_text = self.lineEdit_Replace.text()
        if replaced_text and self.current_search_index is not None:
            cursor = self.textEdit_main_editor.textCursor()
            cursor.setPosition(self.search_result_index_list[self.current_search_index])
            cursor.movePosition(cursor.Right, cursor.KeepAnchor, len(self.search_text))
            cursor.insertText(replaced_text)
            self.textEdit_main_editor.setTextCursor(cursor)
            self.SearchFromText()  # Refresh search results after replacement
    
    def replaceAll(self):
        replaced_text = self.lineEdit_Replace.text()
        if replaced_text and self.search_result_index_list:
            for index in reversed(self.search_result_index_list):  # Replace from end to avoid messing up the indices
                cursor = self.textEdit_main_editor.textCursor()
                cursor.setPosition(index)
                cursor.movePosition(cursor.Right, cursor.KeepAnchor, len(self.search_text))
                cursor.insertText(replaced_text)
            self.SearchFromText()  # Refresh search results after replacement
    
    def jump2loc(self):
        if self.current_search_index is not None:
            self.label_SearchIndex.setText(f"Current Index: {self.current_search_index + 1}, Total: {len(self.search_result_index_list)}")
            cursor = self.textEdit_main_editor.textCursor()
            cursor.setPosition(self.search_result_index_list[self.current_search_index])
            cursor.movePosition(cursor.Right, cursor.KeepAnchor, len(self.search_text))
            self.textEdit_main_editor.setTextCursor(cursor)


    def update_file_info(self, file_path, title, file_content):
        self.file_path = file_path
        self.label_file_path.setText(title)
        self.file_content = file_content
        self.textEdit_main_editor.setText(self.file_content)

    def change_text(self):
        self.now_content = self.textEdit_main_editor.toPlainText()
        if self.now_content != self.file_content:
            self.label_Changed.setText("*")
        else:
            self.label_Changed.setText("")
    
    def open_file(self, file_path):
        if not file_path:
            if not self.file_path:  # New
                self.update_file_info(file_path, "Untitled", "")
            return
        
        if not os.path.isfile(file_path):
            QMessageBox.critical(self, "Error", f"Path: {file_path} does not contain a file!", QMessageBox.StandardButton.Close)
            return
        if not os.path.exists(file_path):
            QMessageBox.critical(self, "Error", f"File: {file_path} does not exist!", QMessageBox.StandardButton.Close)
            return

        # Check file size
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
        if file_size > self.max_file_size:
            QMessageBox.critical(self, "Error", f"Opened file should be smaller than {self.max_file_size} MB.", QMessageBox.StandardButton.Ok)
            return

        # Ensure encoding type
        try:
            with open(file_path, 'r', encoding="utf8") as f:
                file_content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'rb') as f:
                data = f.read()
                encoding = chardet.detect(data)['encoding']
            with open(file_path, 'r', encoding=encoding) as f:
                file_content = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read the file: {str(e)}", QMessageBox.StandardButton.Ok)
            return

        self.update_file_info(file_path, file_path, file_content)
    
    def save_file(self):
        if not self.file_path:
            self.file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "./", "All Files (*);;Text Files (*.txt)")
            if not self.file_path:
                return
        try:
            with open(self.file_path, 'w', encoding="utf8") as f:
                f.write(self.now_content)
            self.update_file_info(self.file_path, self.file_path, self.now_content)
            self.label_Changed.setText("")  # Clear Symbol: *
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save the file: {str(e)}", QMessageBox.StandardButton.Ok)

    def closeEvent(self, event):
        if self.now_content != self.file_content:
            reply = QMessageBox.question(self, "Save", "Save file?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        event.accept()
