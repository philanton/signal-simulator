import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from classes.block_zone import BlockZone
from classes.discover_zone import DiscoverZone


class WorkingZone(qtw.QWidget):
    """It's a working zone"""

    def __init__(self, parent=None):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self.setSizePolicy(
            qtw.QSizePolicy.MinimumExpanding,
            qtw.QSizePolicy.MinimumExpanding
        )


        horizontal_layout = qtw.QHBoxLayout()

        block_zone = qtw.QScrollArea(self)
        block_zone.setWidget(BlockZone())
        horizontal_layout.addWidget(block_zone)
        
        horizontal_layout.addWidget(DiscoverZone(self))
        self.setLayout(horizontal_layout)


        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("black"))
        self.setPalette(palette)
