import sys

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from classes.block_panel import BlockPanel
from classes.working_zone import WorkingZone

class MainWindow(qtw.QMainWindow):
    """It's a main page of app"""

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        central_widget = qtw.QWidget(self)
        vertical_layout = qtw.QVBoxLayout(central_widget)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(BlockPanel(central_widget))
        vertical_layout.addWidget(WorkingZone(central_widget))
        central_widget.setLayout(vertical_layout)
        self.setCentralWidget(central_widget)

        central_widget.setAutoFillBackground(True)
        palette = central_widget.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("green"))
        central_widget.setPalette(palette)

        self.setMinimumSize(720, 480)
        self.show()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    app.exec_()
