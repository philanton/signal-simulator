import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt

from classes.blocks.basic_block import BasicBlock


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

        self.setAcceptDrops(True)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("cyan"))
        self.setPalette(palette)

    def dragEnterEvent(self, e):
        """Accept creating new blocks"""
        e.accept()

    def dropEvent(self, e):
        """Create new block where mouse drops"""
        block = BasicBlock(self)
        block.setText("New Block")
        block.move(e.pos())
        block.show()

        e.setDropAction(Qt.MoveAction)
        e.accept()
