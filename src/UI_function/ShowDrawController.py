from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QDialog
from UI.UI_ShowDraw import Ui_Dialog


class ShowDrawController(Ui_Dialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(QDialog)

        self.canvas = FigureCanvas(plt.Figure())
        self.verticalLayout_for_draw.addWidget(self.canvas)