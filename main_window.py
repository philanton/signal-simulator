import sys

import PySide6.QtWidgets as qtw

from classes.block_panel import BlockPanel

class MainWindow(qtw.QMainWindow):
    """It's a main page of app"""

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        central_widget = qtw.QWidget(self)
        vertical_layout = qtw.QVBoxLayout(central_widget)
        self.block_panel = BlockPanel(self)
        vertical_layout.addWidget(self.block_panel)
        central_widget.setLayout(vertical_layout)
        self.setCentralWidget(central_widget)

        self.show()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    app.exec_()
