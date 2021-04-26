import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from classes.research.monitor import Monitor
from classes.research.element_list import ElementList


class DiscoverZone(qtw.QWidget):
    """It's a zone, where we can monitor info"""

    def __init__(self, parent=None):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""

        vertical_layout = qtw.QVBoxLayout()
        vertical_layout.addWidget(Monitor())
        vertical_layout.addWidget(ElementList())
        self.setLayout(vertical_layout)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("magenta"))
        self.setPalette(palette)
        self.setMinimumWidth(300)
