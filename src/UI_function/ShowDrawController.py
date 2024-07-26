from PyQt5.QtGui import QCloseEvent
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QDialog, QWidget
from UI.UI_ShowDraw import Ui_DrawPaint
from UI.UI_MainWindow import Ui_MainWindow


class ShowDrawController(Ui_DrawPaint, QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.setupUi(self)
        self.showedWidget = None
        self.parent = parent
    
    def clear_layout(self):
        """
        Clear content in Layout
        """
        if self.showedWidget:
            self.showedWidget.setParent(None)
            self.verticalLayout_Draw.removeWidget(self.showedWidget)
    
    def open_close(self, open_status: bool):
        """
        Toggle this Diaglog
        """
        self.show() if open_status else self.close()
    
    def showDrawedWidget(self, showedWidget):
        """
        Show 
        """
        self.clear_layout()
        self.showedWidget = showedWidget
        self.verticalLayout_Draw.addWidget(self.showedWidget)
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.clear_layout()
        self.parent.actionDraw.setChecked(False)
        return super().closeEvent(a0)