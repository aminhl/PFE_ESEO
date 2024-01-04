import sys
import random

from PySide6.QtWidgets import QWidget, QVBoxLayout


from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

class Charts(QWidget):
    def __init__(self, parent=None):
        super(Charts, self).__init__(parent)

        self.resize(600, 490)
        self.title = 'The Window Title'
        self.setWindowTitle(self.title)

        self.createCharts()

    def createCharts(self):
        if not hasattr(self, 'charts_added') or not self.charts_added:
            x1 = [1, 2, 8, 3, 6]
            y1 = [9, 3, 1, 6, 3]
            labels = ['Category 1', 'Category 2']
            sizes = [15, 30]

            canvas = self.createMatplotlibCanvas(x1, y1, labels, sizes)

            layout = QVBoxLayout()
            layout.addWidget(canvas)
            self.setLayout(layout)

            self.charts_added = True

    def createMatplotlibCanvas(self, x_data, y_data, labels, sizes, dpi=100):
        fig = Figure()
        fig.set_facecolor('#c9c5c5')

        ax1 = fig.add_subplot(121)
        ax1.plot(x_data, y_data)
        ax1.set_title('Line Chart')
        ax1.set_xlabel('X-axis')
        ax1.set_ylabel('Y-axis')

        ax2 = fig.add_subplot(122)
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%',
                startangle=90, wedgeprops=dict(width=0.4))
        ax2.set_title('Donut Chart')
        
        canvas = FigureCanvas(fig)
        return canvas
