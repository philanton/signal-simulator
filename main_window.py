import sys

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from classes.basewidgets import BaseWidget
from classes.block_panel import BlockPanel
from classes.working_zone import WorkingZone


class MainWindow(qtw.QMainWindow):
    """It's a main page of app"""
    def __init__(self):
        super().__init__()
        self.central_widget = MainWidget(self)
        self.setCentralWidget(self.central_widget)

        self.setMinimumSize(720, 480)
        self.show()


class MainWidget(BaseWidget):
    """Inner main widget for main window."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        block_panel = BlockPanel(self)
        working_zone = WorkingZone(self)
        self._init_layout(
            [
                block_panel,
                working_zone
            ],
            margins=(5, 5, 5, 5),
            spacing=5
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#374B4A")
        })


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    app.setStyle('Fusion')
    app.exec_()
