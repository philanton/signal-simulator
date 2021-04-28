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

        self.initialize_grid()

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

    def initialize_grid(self):

        self.grid = qtw.QGridLayout()
        self.grid.setContentsMargins(2, 2, 2, 2)
        self.grid.setVerticalSpacing(2)
        self.grid.setHorizontalSpacing(2)

        cell_s = 15

        for i in range(100):
            for j in range(100):
                cell = qtw.QWidget()
                cell.setFixedSize(cell_s, cell_s)
                cell.setAutoFillBackground(True)
                palette = cell.palette()
                palette.setColor(qtg.QPalette.Window, qtg.QColor("white"))
                cell.setPalette(palette)
                self.grid.addWidget(cell, i, j)

        self.setLayout(self.grid)
