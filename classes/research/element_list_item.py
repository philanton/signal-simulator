import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt
import PySide6.QtGui as qtg

from classes.basewidget import BaseWidget


class ElementListRow(BaseWidget):
    """It's a list item with set of options for selected element"""
    def __init__(self, element=None, is_header=False, parent=None):
        super().__init__(parent)
        self.is_header = is_header
        self.element = element
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_layout(
            [
                self.get_index(),
                self.get_name(),
                self.get_colour(),
                self.get_show()
            ],
            is_vertical=False,
            margins=(1,1,1,1)
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor(
                "#8B8BAE" if self.is_header else "#C5FFFD"
            )
        })

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
