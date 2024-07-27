import os
import chardet
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget

class TextFileEditor(QWidget):
    def __init__(self, file_path="") -> None:
        super().__init__()
        self.setupUi(self)
        self.file_path = file_path
        self.file_content = ""
        
        self.textEdit_main_editor.textChanged.connect(self.change_text)
        self.Button_save.clicked.connect(self.save_file)

        self.open_file(file_path)
    
    def setupUi(self, FileEditor):
        FileEditor.setObjectName("FileEditor")
        FileEditor.resize(725, 554)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(FileEditor)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_file_path = QtWidgets.QLabel(FileEditor)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_file_path.setFont(font)
        self.label_file_path.setObjectName("label_file_path")
        self.verticalLayout.addWidget(self.label_file_path)
        self.textEdit_main_editor = QtWidgets.QTextEdit(FileEditor)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_main_editor.setFont(font)
        self.textEdit_main_editor.setObjectName("textEdit_main_editor")
        self.verticalLayout.addWidget(self.textEdit_main_editor)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Button_save = QtWidgets.QPushButton(FileEditor)
        self.Button_save.setObjectName("Button_save")
        self.horizontalLayout.addWidget(self.Button_save)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(FileEditor)
        QtCore.QMetaObject.connectSlotsByName(FileEditor)

    def retranslateUi(self, FileEditor):
        _translate = QtCore.QCoreApplication.translate
        FileEditor.setWindowTitle(_translate("FileEditor", "FileEditor"))
        self.label_file_path.setText(_translate("FileEditor", "file_path"))
        self.Button_save.setText(_translate("FileEditor", "Save"))

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
