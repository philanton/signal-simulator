from collections import Counter

import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt

from classes.basewidgets import BaseWidget, BlockView, BlockLabel
from classes.config import blocks
from classes.modals import BaseModal


class BlockZone(BaseWidget):
    """It's a zone, where we place and connect over blocks"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

        self.index_rules = Counter([block["abbr"] for block in blocks])
        self.block_positions = {}

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

        self.block_positions.update({block.config["id"]: block.grid_pos})

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

        self.block_positions.update({block.config["id"]: (-10, -10)})

    def get_cleared_block(self):
        """"""
        try:
            return self.cleared_block
        except AttributeError:
            return None

    def hover_in(self, cell_pos):
        x = self.index_hint(cell_pos[0], max=self.grid_shape[0])
        y = self.index_hint(cell_pos[1], max=self.grid_shape[1])

        self.block_pos = (x, y)
        self.__hover()

    def hover_out(self):
        self.__hover(leaves=True)

    def __hover(self, leaves=False):
        x_from, x_to = self.block_pos[0] - 1, self.block_pos[0] + 2
        y_from, y_to = self.block_pos[1] - 1, self.block_pos[1] + 2

        for x in range(x_from, x_to):
            for y in range(y_from, y_to):
                current_cell = self.get_item_at_pos(x, y)
                current_cell.change_cell_colour(leaves=leaves)

    def get_item_at_pos(self, x, y):
        return self.grid.itemAtPosition(x, y).widget()

    def index_hint(self, c, min=0, max=100):
        return (max - 1  if c >= max
                else c if c > min
                else min + 1)

    def _init_grid_layout(self):
        """"""
        self.margins = (5, 5, 5, 5)
        self.spacing = 2
        self.grid_shape = (100, 100)

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
        super().__init__(GridBlockLabel(name), parent)
        self.name = name
        self.grid_pos = grid_pos
        self.config = self.default_config = default_config
        self.init_gui()

        tip = "{}: {}".format(self.config["name"], self.config["id"])
        self.setToolTip(tip)

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

    def delete(self):
        self.parent().clear_block(self)


class GridBlockLabel(BlockLabel):
    """"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.setFocusPolicy(Qt.ClickFocus)

    def focusOutEvent(self, e):
        """"""
        self.hover(leaves=True)

    def keyPressEvent(self, e):
        """"""
        if e.key() == Qt.Key_Delete:
            try:
                self.parent().delete()
            except AttributeError:
                pass

    def mouseMoveEvent(self, e):
        self.parent().event(e)


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

    def check_no_near_neighbours(self):
        pos = self.grid_pos
        pos = (
            self.parent().index_hint(pos[0], max=self.parent().grid_shape[0]),
            self.parent().index_hint(pos[1], max=self.parent().grid_shape[1])
        )

        for x, y in self.parent().block_positions.values():
            d_x = x - pos[0]
            d_y = y - pos[1]
            d = (d_x ** 2 + d_y ** 2) ** 0.5

            if d < 3: return False

        return True

    def dragEnterEvent(self, e):
        """Accept creating new blocks"""
        pos = self.grid_pos
        if not self.check_no_near_neighbours():
            pos = self.parent().block_pos

        self.parent().hover_in(pos)
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
