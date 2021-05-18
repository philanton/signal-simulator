import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt

from classes.basewidgets import BaseWidget, BlockView, BlockLabel
from classes.config import blocks as block_configs


class BlockPanel(BaseWidget):
    """Class for panel, which have all available blocks"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        block_widgets = [
            PanelBlockView(
                conf["abbr-ua"],
                conf["abbr"]
            ) for conf in block_configs
        ]
        self._init_layout(
            block_widgets + [""],
            is_vertical=False,
            margins=(5, 5, 5, 5),
            spacing=5
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#526760")
        })


class PanelBlockView(BlockView):
    """View for block in Block Panel"""
    def __init__(self, name, id, parent=None):
        super().__init__(BlockLabel(name), parent)
        self.name = name
        self.id = id
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        super().init_gui()

        self._init_sizing(width=60, height=40)

    def mouseMoveEvent(self, e):
        """Event for dragging out block to the Block Zone"""
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = qtc.QMimeData()
        mimeData.setText(self.id)

        drag = qtg.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(qtg.QPixmap("img/block-plus.png"))
        drag.exec_(Qt.MoveAction)
