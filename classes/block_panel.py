import PySide6.QtGui as qtg
from classes.blocks.basic_block import BasicBlock
from classes.basewidget import BaseWidget


class BlockPanel(BaseWidget):
    """Class for panel, which have all available blocks"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""

        self._init_layout(
            [BasicBlock(), ""],
            is_vertical=False,
            margins=(1,1,1,1),
            spacing=5
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("black")
        })
