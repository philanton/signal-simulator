import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg


class Monitor(qtw.QWidget):
    """It's a monitor with plots of signals"""

    def __init__(self, parent=None):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("red"))
        self.setPalette(palette)
        self.setMinimumHeight(200)
