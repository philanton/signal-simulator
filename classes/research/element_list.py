import PySide6.QtWidgets as qtw
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

        header = ElementListRow(is_header=True)
        list_item_1 = ElementListRow({
            "id": "1",
            "name": "Sender",
            "colour": "red"
        })
        list_item_2 = ElementListRow({
            "id": "4",
            "name": "SenderSender",
            "colour": "red"
        })
        self._init_layout(
            [
                header,
                list_item_1,
                list_item_2,
                ""
            ],
            margins=(5, 5, 5, 5),
            spacing=5
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#88D9E6")
        })
