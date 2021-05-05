import PySide6.QtGui as qtg
from classes.blocks.basic_block import BasicBlock
from classes.basewidget import BaseWidget
from classes.blocks.config import blocks


class BlockPanel(BaseWidget):
    """Class for panel, which have all available blocks"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        block_names = [block["abbr"] for block in blocks]
        block_widgets = [BasicBlock(name) for name in block_names]
        self._init_layout(
            block_widgets + [""],
            is_vertical=False,
            margins=(5, 5, 5, 5),
            spacing=5
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#526760")
        })
