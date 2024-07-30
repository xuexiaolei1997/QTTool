import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from UI_function.MainController import MainController


def excepthook(exctype, value, tb):
    print("自定义的异常处理逻辑")
    print("异常类型：", exctype)
    print("异常值：", value)
    print("异常追溯：", tb)

    import traceback
    traceback.print_tb(tb)
    print(repr(exctype))
    # response = QMessageBox.warning(Application.mainWindow, "Error", repr(value), QMessageBox.Ok | QMessageBox.Close)
    # if response != QMessageBox.Ok:
    #     sys.exit(1)

sys.excepthook = excepthook

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = MainController(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
