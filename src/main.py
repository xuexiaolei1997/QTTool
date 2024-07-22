import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import data_processing

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Processing and Visualization')
        self.setGeometry(100, 100, 800, 600)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)

        self.button = QPushButton('Process and Visualize Data')
        self.button.clicked.connect(self.process_and_visualize_data)
        layout.addWidget(self.button)

    def process_and_visualize_data(self):
        data = np.random.rand(100).tolist()
        processed_data = data_processing.process_data(data)

        ax = self.canvas.figure.subplots()
        ax.clear()
        ax.plot(data, label='Original Data')
        ax.plot(processed_data, label='Processed Data')
        ax.legend()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
