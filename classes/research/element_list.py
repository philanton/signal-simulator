import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt
import PySide6.QtGui as qtg

from classes.basewidget import BaseWidget
from classes.research.element_list_item import ElementListRow


class ElementList(BaseWidget):
    """It's a list, where we can set options about available elements"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(size_policy=(
            qtw.QSizePolicy.Preferred,
            qtw.QSizePolicy.MinimumExpanding
        ))

        description = self.get_description()
        header = ElementListItem(is_header=True)
        list_item_1 = ElementListItem({
            "id": "1",
            "name": "Sender",
            "colour": "red"
        })
        list_item_2 = ElementListItem({
            "id": "4",
            "name": "SenderSender",
            "colour": "red"
        })
        self._init_layout(
            [
                description,
                header,
                list_item_1,
                list_item_2
            ],
            margins=(5,5,5,5),
            spacing=5
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#88D9E6")
        })

    def get_description(self):
        text = "Here will be list of current process elements."

        description_widget = qtw.QLabel()
        description_widget.setText(text)
        description_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        return description_widget
