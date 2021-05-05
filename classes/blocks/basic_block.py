import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt


class BasicBlock(qtw.QLabel):
    """Parent Class for all available blocks"""

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self.setText(self.text)
        self.setStyleSheet("""
            border: 3px solid #88D9E6;
            background-color: #C5FFFD;
            color: #88D9E6;
            border-radius: 3px;
            font-family: monospace;
            font-size: 16px;
        """)
        self.setFixedSize(50, 40)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.LeftButton:
            return

        mimeData = qtc.QMimeData()
        mimeData.setText(self.text)

        drag = qtg.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(qtg.QPixmap("img/block-plus.png"))

        dropAction = drag.exec_(Qt.MoveAction)
