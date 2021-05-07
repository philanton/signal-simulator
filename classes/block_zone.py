from collections import Counter

import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt

from classes.basewidgets import BaseWidget, BlockView
from classes.config import blocks
from classes.modals import BaseModal


class BlockZone(BaseWidget):
    """It's a zone, where we place and connect over blocks"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

        self.index_rules = Counter([block["abbr"] for block in blocks])

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

    def dropEvent(self, e):
        """Create new block where mouse drops"""
        text = e.mimeData().text()
        self.create_block(text)

        e.setDropAction(Qt.MoveAction)
        e.accept()

    def create_block(self, name=""):
        if (self.get_cleared_block() and
            self.get_cleared_block().config["id"] == name):
            block = self.cleared_block
            block.grid_pos = self.block_pos
        else:
            block_id = f"{name.lower()}_{self.index_rules.get(name)}"
            self.index_rules[name] += 1

            block_config = [conf for conf in blocks if conf["abbr"] == name][0]
            block_config = block_config.copy()
            block_config.update({ "id": block_id })

            block = GridBlockView(
                name,
                self.block_pos,
                default_config=block_config,
                parent=self
            )

        self.hover_out()
        self.grid.addWidget(
            block,
            self.block_pos[0] - 1,
            self.block_pos[1] - 1,
            3,
            3
        )

    def clear_block(self, block):
        """"""
        self.cleared_block = block
        self.cleared_block.setParent(None)

    def get_cleared_block(self):
        """"""
        try:
            return self.cleared_block
        except AttributeError:
            return None

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
    def __init__(self, name, grid_pos, default_config={}, parent=None):
        super().__init__(name, parent)
        self.name = name
        self.grid_pos = grid_pos
        self.config = self.default_config = default_config
        self.init_gui()

        tip = "{}: {}".format(self.config["name"], self.config["id"])
        self.setToolTip(tip)

        self.setFocusPolicy(Qt.ClickFocus)

    def mouseDoubleClickEvent(self, e):
        """Invoke modal window with set of options"""
        modal = BaseModal()
        if modal.exec_():
            print(modal.options)

    def mouseMoveEvent(self, e):
        """Event for dragging out block to the Block Zone"""
        if e.buttons() != Qt.LeftButton:
            return

        try:
            self.parent().clear_block(self)
        except AttributeError:
            pass

        mimeData = qtc.QMimeData()
        mimeData.setText(self.config["id"])

        drag = qtg.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(qtg.QPixmap("img/block.png"))
        drag.exec_(Qt.MoveAction)

    def focusOutEvent(self, e):
        """"""
        self.label.hover(leaves=True)

    def keyPressEvent(self, e):
        """"""
        if e.key() == Qt.Key_Delete:
            try:
                self.parent().clear_block(self)
            except AttributeError:
                pass


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
        text = e.mimeData().text()
        self.parent().create_block(text)

        e.setDropAction(Qt.MoveAction)
        e.accept()
