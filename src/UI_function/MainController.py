import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from UI.UI_MainWindow import Ui_MainWindow
from common import thread_pool

class MainController(Ui_MainWindow):
    def __init__(self, MainWindow) -> None:
        super().__init__()

        self.setupUi(MainWindow)

        self.t_pool = thread_pool.ThreadPool(4)

        self.canvas = FigureCanvas(plt.Figure())
        self.drawVerticalLayout.addWidget(self.canvas)

        self.drawButton.clicked.connect(self.draw_method)
        self.ThreadButton.clicked.connect(self.test_thread)
    
    def draw_method(self):
        data = np.random.rand(100)
        processed_data = data + 1
        ax = self.canvas.figure.subplots()
        ax.clear()
        ax.plot(data, label='Original Data')
        ax.plot(processed_data, label='Processed Data')
        ax.legend()
        self.canvas.draw()

    def test_thread(self):

        def _sub_thread():

            print("789456")
        
        self.t_pool.enqueue(_sub_thread)
        print("finished")
