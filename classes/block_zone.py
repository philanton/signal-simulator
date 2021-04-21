import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg


class BlockZone(qtw.QWidget):
    """It's a zone, where we place and connect over blocks"""

    def __init__(self, parent=None):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self.setSizePolicy(
            qtw.QSizePolicy.MinimumExpanding,
            qtw.QSizePolicy.MinimumExpanding
        )

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("cyan"))
        self.setPalette(palette)
