import numpy as np

from PyQt5.QtWidgets import QMessageBox, QFileDialog, QWidget, QMdiSubWindow
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from UI.UI_MainWindow import Ui_MainWindow
from Components.FileBrowserDock import FileBrowserDock
from Components.TextFileEditor import TextFileEditor





class MainController(Ui_MainWindow):
    def __init__(self, MainWindow) -> None:
        super().__init__()

        self.MainWindow = MainWindow

        # >> Setup UI
        self.setupUi(MainWindow)

        # >> ThreadPool
        # self.t_pool = thread_pool.ThreadPool(4)

        # >> File
        # # New
        self.actionNew.triggered.connect(self.create_file)
        # # Open
        self.actionOpen.triggered.connect(self.open_file)
        # Open Folder
        self.actionOpen_Folder.triggered.connect(self.open_folder)

        # Save
        # Save as
        # Close
        self.actionClose.triggered.connect(self.close)


        # >> Edit
        
        # >> View

        # self.showDrawController = ShowDrawController(self)  # sub window for show
        # self.actionDraw.toggled['bool'].connect(self.showDrawController.open_close)

        # self.drawButton.clicked.connect(self.draw_method)

        # self.ThreadButton.clicked.connect(self.test_thread)

        # >> Help
        self.actionAbout.triggered.connect(self.show_about)
    
    def create_file(self):
        self.create_file_window(file_path="")
    
    def open_file(self):
        file_path, file_type = QFileDialog.getOpenFileName(self.MainWindow, "Select File", "./")
        if file_path == "":
            return
        self.create_file_window(file_path)

    def create_file_window(self, file_path=""):
        fileEditor = TextFileEditor(file_path)
        self.mdiArea.addSubWindow(fileEditor)
        fileEditor.show()
    
    def open_folder(self):
        directory = QFileDialog.getExistingDirectory(self.MainWindow, "Open Folder", "./")
        self.file_browser_dock = FileBrowserDock(self.dockWidget_Left, directory)
        self.file_browser_dock.fileSelected.connect(self.create_file_window)
    
    def close(self):
        self.MainWindow.close()

    def show_about(self):
        QMessageBox.information(None, "About", "This is About!", QMessageBox.StandardButton.Close)
    
    # def show_drawed_dialog(self, canvas):
    #     self.showDrawController.showDrawedWidget(canvas)
    #     self.actionDraw.setChecked(True)

    
    # def draw_method(self):
    #     data = np.random.rand(100)
    #     processed_data = data + 1

    #     canvas = FigureCanvas(plt.Figure())
    #     ax = canvas.figure.subplots()
    #     ax.clear()
    #     ax.plot(data, label='Original Data')
    #     ax.plot(processed_data, label='Processed Data')
    #     ax.legend()
    #     canvas.draw()
    #     self.show_drawed_dialog(canvas)
    
