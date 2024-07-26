import numpy as np

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from UI.UI_MainWindow import Ui_MainWindow
from UI_function.ShowDrawController import ShowDrawController
from common import thread_pool
from common.FileBrowserDock import FileBrowserDock




class MainController(Ui_MainWindow):
    def __init__(self, MainWindow) -> None:
        super().__init__()

        self.MainWindow = MainWindow

        # >> Setup UI
        self.setupUi(MainWindow)

        # >> ThreadPool
        self.t_pool = thread_pool.ThreadPool(4)

        # >> File
        # # new
        # # open
        # Open Folder
        self.actionOpen_Folder.triggered.connect(self.open_folder)

        # >> Edit
        
        # >> View
        self.showDrawController = ShowDrawController(self)  # sub window for show
        self.actionDraw.toggled['bool'].connect(self.showDrawController.open_close)

        self.drawButton.clicked.connect(self.draw_method)

        self.ThreadButton.clicked.connect(self.test_thread)

        # >> Help
        self.actionAbout.triggered.connect(self.show_about)

        # self.dockWidget_Left.closeEvent(self.actionResource.setChecked(False))
    
    def open_folder(self):
        directory = QFileDialog.getExistingDirectory(self.MainWindow, "Open Folder", "/")
        FileBrowserDock(self.dockWidget_Left, directory)

    def show_about(self):
        QMessageBox.information(None, "About", "This is About!", QMessageBox.StandardButton.Close)
    
    def show_drawed_dialog(self, canvas):
        self.showDrawController.showDrawedWidget(canvas)
        self.actionDraw.setChecked(True)

    
    def draw_method(self):
        data = np.random.rand(100)
        processed_data = data + 1

        canvas = FigureCanvas(plt.Figure())
        ax = canvas.figure.subplots()
        ax.clear()
        ax.plot(data, label='Original Data')
        ax.plot(processed_data, label='Processed Data')
        ax.legend()
        canvas.draw()
        self.show_drawed_dialog(canvas)
        
    def test_thread(self):

        def _sub_thread():

            print("789456")
        
        self.t_pool.enqueue(_sub_thread)
        print("finished")
