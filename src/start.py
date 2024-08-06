import os
import sys
import traceback

from PyQt5.QtWidgets import QMessageBox
from Application import Application


def excepthook(exctype, value, tb):
    print("Execption:")
    print("Execption Type:", exctype)
    print("Execption Value:", value)
    print("Execption Traceback:", tb)

    traceback.print_tb(tb)
    print(repr(exctype))
    response = QMessageBox.warning(Application.mainWindow, "Error", repr(value), QMessageBox.Ok | QMessageBox.Close)
    if response != QMessageBox.Ok:
        sys.exit(1)


sys.excepthook = excepthook


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = Application(sys.argv)
    sys.exit(app.exec())
