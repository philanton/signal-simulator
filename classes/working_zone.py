import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from classes.basewidgets import BaseWidget
from classes.block_zone import BlockZone
from classes.discover_zone import DiscoverZone


class WorkingZone(BaseWidget):
    """It's a working zone"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(size_policy=(
            qtw.QSizePolicy.MinimumExpanding,
            qtw.QSizePolicy.MinimumExpanding
        ))

        block_zone = qtw.QScrollArea(self)
        block_zone.setWidget(BlockZone())
        discover_zone = DiscoverZone(self)
        self._init_layout(
            [
                block_zone,
                discover_zone
            ],
            is_vertical=False,
            margins=(5, 5, 5, 5),
            spacing=5
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#526760")
        })
