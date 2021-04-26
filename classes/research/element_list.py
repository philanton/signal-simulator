import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg


class ElementList(qtw.QWidget):
    """It's a list, where we can set options about available elements"""

    def __init__(self, parent=None):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""

        self.setSizePolicy(
            qtw.QSizePolicy.Preferred,
            qtw.QSizePolicy.MinimumExpanding
        )

        self.grid = qtw.QGridLayout()
        self.setLayout(self.grid)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("blue"))
        self.setPalette(palette)
