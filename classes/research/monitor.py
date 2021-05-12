import PySide6.QtGui as qtg

from classes.basewidgets import BaseWidget


class Monitor(BaseWidget):
    """It's a monitor with plots of signals"""
    def __init__(self, notifier, parent=None):
        super().__init__(parent)
        self.element_state_notifier = notifier
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(height=200)

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#526760")
        })
