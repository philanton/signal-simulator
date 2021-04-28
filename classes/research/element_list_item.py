import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt
import PySide6.QtGui as qtg


class ElementListItem(qtw.QWidget):
    """It's a list item with set of options for selected element"""

    def __init__(self, element=None, is_header=False, parent=None):
        super().__init__()
        self.is_header = is_header
        self.element = element
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""

        self.horizontal_layout = qtw.QHBoxLayout()
        self.horizontal_layout.setContentsMargins(1,1,1,1)
        self.horizontal_layout.addWidget(self.get_index())
        self.horizontal_layout.addWidget(self.get_name())
        self.horizontal_layout.addWidget(self.get_colour())
        self.horizontal_layout.addWidget(self.get_show())
        self.setLayout(self.horizontal_layout)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor("skyblue"))
        self.setPalette(palette)

    def get_index(self):
        index = qtw.QLabel()
        index.setText("№" if self.is_header else self.element["id"])
        return index

    def get_name(self):
        name = qtw.QLabel()
        name.setText("Name" if self.is_header else self.element["name"])
        return name

    def get_colour(self):
        colour = qtw.QLabel()
        colour.setText("Colour" if self.is_header else self.element["colour"])
        return colour

    def get_show(self):
        show = qtw.QLabel()
        show.setText("Show" if self.is_header else "No")
        return show
