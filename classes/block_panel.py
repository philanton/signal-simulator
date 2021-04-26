import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt
from classes.blocks.basic_block import BasicBlock

class BlockPanel(qtw.QWidget):
    """Class for panel, which have all available blocks"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""

        horizontal_layout = qtw.QHBoxLayout()
        horizontal_layout.setContentsMargins(1, 1, 1, 1)
        horizontal_layout.setSpacing(5)

        # create and add blocks
        for value in ['Sender', 'Receiver', 'Middle', 'Other']:
            block = BasicBlock(self)
            block.setText(value)
            horizontal_layout.addWidget(block)
        horizontal_layout.addStretch(1)
        self.setLayout(horizontal_layout)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("black"))
        self.setPalette(palette)
