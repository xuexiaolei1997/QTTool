import os
import re
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, QObject, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont

from .UI_Terminal import Ui_Form_Terminal


class Worker(QObject):
    finished = pyqtSignal()
    output = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, command, current_dir):
        super().__init__()
        self.command = command
        self.current_dir = current_dir

    def run(self):
        try:
            process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.current_dir, text=True)
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    self.output.emit(output.strip())
            stderr = process.communicate()[1]
            if stderr:
                self.error.emit(stderr.strip())
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

class TerminalTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_ = parent

        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.setFont(font)
        self.setObjectName("textEdit_Terminal")
        self.setAcceptRichText(True)
        self.setReadOnly(False)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.parent_.run_command()  # 执行自定义操作
        else:
            super().keyPressEvent(event)  # 调用父类方法，确保其他按键正常处理
    

class Terminal(Ui_Form_Terminal, QWidget):
    def __init__(self, parent: QWidget, current_dir="/") -> None:
        super().__init__(parent)
        
        self.current_dir = current_dir
        self.run_command_thread = QThread()

        self.textEdit_Terminal = TerminalTextEdit(self)

        qss_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qss', 'style.qss')
        if os.path.exists(qss_file_path):
            with open(qss_file_path, 'r', encoding='utf8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        
        self.setupUi(self)
        self.show_prompt(self.current_dir)
    
    def setupUi(self, Form_Terminal):
        Form_Terminal.setObjectName("Form_Terminal")
        Form_Terminal.resize(616, 439)
        self.verticalLayout = QVBoxLayout(Form_Terminal)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.textEdit_Terminal)

        self.retranslateUi(Form_Terminal)
        QMetaObject.connectSlotsByName(Form_Terminal)

    def retranslateUi(self, Form_Terminal):
        _translate = QCoreApplication.translate
        Form_Terminal.setWindowTitle(_translate("Form_Terminal", "Form"))

    def show_prompt(self, current_dir):
        self.textEdit_Terminal.append(f"{current_dir} > ")

    def catch_command(self, command):
        match = re.search(r"^.*?>\s+(.*)$", command)
        if match:
            return match.group(1)
        return ""

    def run_command(self):
        text = self.textEdit_Terminal.toPlainText()
        command_line = text.split('\n')[-1]  # Get the last line as the command line
        command = self.catch_command(command_line)  # Get the command part

        if command:
            self.textEdit_Terminal.append("")  # Add a new line for output

            if command.startswith("cd "):
                new_dir = re.search(r"^cd\s+(.*)$", command).group(1)
                new_dir = os.path.abspath(new_dir)
                if os.path.isdir(new_dir):
                    self.current_dir = new_dir
                self.show_prompt(self.current_dir)
                return

            self.worker = Worker(command, self.current_dir)
            self.worker.moveToThread(self.run_command_thread)

            self.run_command_thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.on_finished)
            self.worker.output.connect(self.show_output)
            self.worker.error.connect(self.show_error)
            self.worker.finished.connect(self.run_command_thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            # self.run_command_thread.finished.connect(self.run_command_thread.deleteLater)

            self.run_command_thread.start()
        else:
            self.show_prompt(self.current_dir)

    def show_output(self, output):
        self.textEdit_Terminal.append(output)

    def show_error(self, error):
        self.textEdit_Terminal.append(f"<span style='color: red;'>{error}</span>")

    def on_finished(self):
        self.textEdit_Terminal.append("Command finished.")
        self.show_prompt(self.current_dir)