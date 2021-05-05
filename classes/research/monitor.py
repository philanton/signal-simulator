import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from classes.basewidget import BaseWidget


class Monitor(BaseWidget):
    """It's a monitor with plots of signals"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(height=200)

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#526760")
        })
