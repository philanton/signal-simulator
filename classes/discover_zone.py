import PySide6.QtGui as qtg

from classes.basewidgets import BaseWidget
from classes.states import StateNotifier
from classes.research.element_list import ElementList
from classes.research.monitor import Monitor


class DiscoverZone(BaseWidget):
    """It's a zone, where we can monitor info"""
    def __init__(self, notifier, parent=None):
        super().__init__(parent)
        self.block_state_notifier = notifier
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(width=300)

        element_state_notifier = StateNotifier()
        monitor = Monitor(element_state_notifier)
        element_list = ElementList(
            self.block_state_notifier,
            element_state_notifier
        )
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
