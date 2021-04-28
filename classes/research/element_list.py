import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt
import PySide6.QtGui as qtg

from classes.research.element_list_item import ElementListItem


class ElementList(qtw.QWidget):
    """It's a list, where we can set options about available elements"""

    def __init__(self, parent=None):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""

        self.setSizePolicy(
            qtw.QSizePolicy.Preferred,
            qtw.QSizePolicy.MinimumExpanding
        )

        self.vertical_layout = qtw.QVBoxLayout()
        self.vertical_layout.addWidget(self.get_description(
            "Here will be list of current process elements."
        ))
        self.vertical_layout.addWidget(ElementListItem(is_header=True))
        self.vertical_layout.addWidget(ElementListItem({
            "id": "1",
            "name": "Sender",
            "colour": "red"
        }))
        self.vertical_layout.addWidget(ElementListItem({
            "id": "2",
            "name": "Sender",
            "colour": "red"
        }))
        self.vertical_layout.addWidget(ElementListItem({
            "id": "3",
            "name": "Sender",
            "colour": "redddddd"
        }))
        self.vertical_layout.addWidget(ElementListItem({
            "id": "4",
            "name": "SenderSender",
            "colour": "red"
        }))
        self.setLayout(self.vertical_layout)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("blue"))
        self.setPalette(palette)

    def get_description(self, text):
        description_widget = qtw.QLabel()
        description_widget.setText(text)
        description_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        return description_widget
