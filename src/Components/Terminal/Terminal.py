import os
import re
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, QObject, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont, QTextCursor

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
    

class Terminal(Ui_Form_Terminal, QWidget):
    def __init__(self, parent: QWidget, current_dir="/") -> None:
        super().__init__(parent)

        self.setupUi(self)
        
        self.current_dir = current_dir
        self.label_current_dir.setText(f"{self.current_dir} : ")
        self.lineEdit_Command.setFocus()
        self.run_command_thread = QThread()

        # self.textEdit_Terminal = TerminalTextEdit(self, self.current_dir)

        qss_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qss', 'style.qss')
        if os.path.exists(qss_file_path):
            with open(qss_file_path, 'r', encoding='utf8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)

    def keyPressEvent(self, event):
        self.ensure_cursor_at_end()
        if event.key() == Qt.Key_Return:
            self.run_command()
        elif event.key() == Qt.Key_Tab:
            current_command = self.lineEdit_Command.text()
            if current_command == "":
                super().keyPressEvent(event)
            else:
                last_word = re.split('\s+', current_command)[-1]
                suggest = list(filter(lambda x: x.startswith(last_word), os.listdir(self.current_dir)))
                if suggest:
                    self.lineEdit_Command.setText(self.lineEdit_Command.text()[:-len(last_word)] + suggest[0])
                else:
                    return
        elif event.key() in (Qt.Key_Backspace, Qt.Key_Delete):
            super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def ensure_cursor_at_end(self):
        self.lineEdit_Command.setFocus()
        self.lineEdit_Command.setCursorPosition(len(self.lineEdit_Command.text()))
    
    def show_prompt(self):
        self.textBrowser_ResultView.append(f"{self.current_dir} : ")

    def run_command(self):
        command = self.lineEdit_Command.text().strip()
        if command:
            self.textBrowser_ResultView.append(f"<span style='color: green;'>{self.current_dir} : {command}</span>")
            self.worker = Worker(command, self.current_dir)
            
            self.worker.moveToThread(self.run_command_thread)

            def on_finished():
                if command.startswith("cd "):
                    entered_dir = re.search(r"^cd\s+(.*)$", command).group(1)
                    
                    entered_dir = os.path.abspath(os.path.join(self.current_dir, entered_dir))
                    if os.path.isdir(entered_dir):
                        self.current_dir = entered_dir
                    self.label_current_dir.setText(f"{self.current_dir} : ")
            
            def show_error(error):
                self.textBrowser_ResultView.append(f"<span style='color: red;'>{error}</span>")

            self.run_command_thread.started.connect(self.worker.run)
            self.worker.finished.connect(on_finished)
            self.worker.output.connect(self.textBrowser_ResultView.append)
            self.worker.error.connect(show_error)
            self.worker.finished.connect(self.run_command_thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)

            
            # self.run_command_thread.finished.connect(self.run_command_thread.deleteLater)

            self.run_command_thread.start()
        else:
            self.textBrowser_ResultView.append(f"{self.current_dir} : ")
        self.lineEdit_Command.clear()