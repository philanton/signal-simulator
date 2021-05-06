import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt

from classes.basewidgets import BaseWidget, BlockView
from classes.modals import BaseModal


class BlockZone(BaseWidget):
    """It's a zone, where we place and connect over blocks"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(size_policy=(
            qtw.QSizePolicy.MinimumExpanding,
            qtw.QSizePolicy.MinimumExpanding
        ))

        self._init_grid_layout()

        self.setAcceptDrops(True)

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#8B8BAE")
        })

    def dragEnterEvent(self, e):
        """Accept creating new blocks"""
        e.accept()

    def create_block(self, name="", from_block=None):
        block = from_block if from_block else GridBlockView(name)
        self.grid.addWidget(
            block,
            self.block_pos[0] - 1,
            self.block_pos[1] - 1,
            3,
            3
        )

    def hover_in(self, cell_pos):
        self.__set_3x3_position(cell_pos)
        self.__hover()

    def hover_out(self):
        self.__hover(leaves=True)

    def __hover(self, leaves=False):
        x_from, x_to = self.block_pos[0] - 1, self.block_pos[0] + 2
        y_from, y_to = self.block_pos[1] - 1, self.block_pos[1] + 2

        for x in range(x_from, x_to):
            for y in range(y_from, y_to):
                current_cell = self.grid.itemAtPosition(x, y).widget()
                current_cell.change_cell_colour(leaves=leaves)

    def __set_3x3_position(self, position):
        x = self.block_index_hint["x"].get(position[0], position[0])
        y = self.block_index_hint["y"].get(position[1], position[1])

        self.block_pos = (x, y)

    def _init_grid_layout(self):
        """"""
        self.margins = (5, 5, 5, 5)
        self.spacing = 2
        self.grid_shape = (100, 100)
        self.block_index_hint = {
            "x": {
                0: 1,
                self.grid_shape[0] - 1: self.grid_shape[0] - 2
            },
            "y": {
                0: 1,
                self.grid_shape[1] - 1: self.grid_shape[1] - 2
            }
        }

        self.grid = qtw.QGridLayout()
        self.grid.setContentsMargins(*self.margins)
        self.grid.setVerticalSpacing(self.spacing)
        self.grid.setHorizontalSpacing(self.spacing)

        for i in range(self.grid_shape[1]):
            for j in range(self.grid_shape[0]):
                cell = GridCell((i, j))
                self.grid.addWidget(cell, i, j)

        self.setLayout(self.grid)


class GridBlockView(BlockView):
    """View for block in Block Panel"""
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.name = name
        self.init_gui()

    def mouseDoubleClickEvent(self, e):
        """Invoke modal window with set of options"""
        modal = BaseModal()
        if modal.exec_():
            print(modal.options)

    def _mouseMoveEvent(self, e):
        """Event for dragging out block to the Block Zone"""
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = qtc.QMimeData()
        mimeData.setText(self.text)

        drag = qtg.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(qtg.QPixmap("img/block-plus.png"))
        drag.exec_(Qt.MoveAction)


class GridCell(BaseWidget):
    """Class for every cell in the grid."""
    def __init__(self, grid_pos, parent=None):
        super().__init__(parent)
        self.grid_pos = grid_pos
        self.size = 15

        self.setAcceptDrops(True)

        self._init_sizing(width=self.size, height=self.size)
        self.change_cell_colour(leaves=True)

    def change_cell_colour(self, leaves=False):
        """"""
        colour = "#C5FFFD" if leaves else "#88D9E6"
        self._init_palette({
            qtg.QPalette.Window: qtg.QColor(colour)
        })

    def dragEnterEvent(self, e):
        """Accept creating new blocks"""
        self.parent().hover_in(self.grid_pos)
        e.accept()

    def dragLeaveEvent(self, e):
        """Accept creating new blocks"""
        self.parent().hover_out()
        e.accept()

    def dropEvent(self, e):
        """Create new block where mouse drops"""
        name = e.mimeData().text()
        self.parent().create_block(name)

        e.setDropAction(Qt.MoveAction)
        e.accept()
