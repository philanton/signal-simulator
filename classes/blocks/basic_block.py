import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt

class BasicBlock(qtw.QLabel):
    """Parent Class for all available blocks"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""

        self.setStyleSheet("""
            border: 3px solid blue;
            background-color: yellow;
            color: blue;
            border-radius: 3px;
            font-family: monospace;
            font-size: 16px;
        """)
        self.setFixedSize(80, 60)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
