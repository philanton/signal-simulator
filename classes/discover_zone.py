import PySide6.QtGui as qtg

from classes.basewidgets import BaseWidget
from classes.research.element_list import ElementList
from classes.research.monitor import Monitor


class DiscoverZone(BaseWidget):
    """It's a zone, where we can monitor info"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(width=300)

        monitor = Monitor()
        element_list = ElementList()
        self._init_layout(
            [
                monitor,
                element_list
            ],
            margins=(5, 5, 5, 5),
            spacing=5
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#374B4A")
        })
