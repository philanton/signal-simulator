from collections import Counter

import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt

from classes.basewidgets import BaseWidget, BlockLabel, BlockView
from config import blocks as block_configs
from modals import BaseModal
from states import BlockStore


class BlockZone(BaseWidget):
    """It's a zone, where we place and connect over blocks"""
    def __init__(self, notifier, parent=None):
        super().__init__(parent)
        self.block_state_notifier = notifier
        self.block_manager = BlockManager(parent=self)
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

    def dropEvent(self, e):
        """Create new block where mouse drops"""
        text = e.mimeData().text()
        if text in self.block_manager.index_rules.keys():
            self.block_manager.add_block(text)
        else:
            self.block_manager.reveal_block(self.block_pos)

        e.setDropAction(Qt.MoveAction)
        e.accept()

    def draw_block(self, block):
        self.hover_out()
        self.grid.addWidget(
            block,
            block.grid_pos[0] - 1,
            block.grid_pos[1] - 1,
            3,
            3
        )

    def hover_in(self, cell_pos):
        self.block_pos = self.index_hint(cell_pos)
        self.__hover()

    def hover_out(self):
        self.__hover(leaves=True)

    def __hover(self, leaves=False):
        """"""
        x_from, x_to = self.block_pos[0] - 1, self.block_pos[0] + 2
        y_from, y_to = self.block_pos[1] - 1, self.block_pos[1] + 2

        for x in range(x_from, x_to):
            for y in range(y_from, y_to):
                cell = self.grid.itemAtPosition(x, y).widget()
                cell.change_cell_colour(leaves=leaves)

    def index_hint(self, pos):
        x, y = pos
        max_x, max_y = self.grid_shape

        x = max_x - 1 if x >= max_x else x if x > 0 else 1
        y = max_y - 1 if y >= max_y else y if y > 0 else 1

        return x, y

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


class BlockManager():
    """"""
    def __init__(self, parent):
        """"""
        self.parent = parent
        self.index_rules = Counter([conf["abbr"] for conf in block_configs])
        self.blocks = set()
        self.cached_block = None

    def add_block(self, name):
        """"""
        config = [conf for conf in block_configs if conf["abbr"] == name][0]
        config = config.copy()
        abbr = config["abbr"]

        id = f"{abbr.lower()}_{self.index_rules.get(abbr)}"
        self.index_rules[abbr] += 1
        config.update({"id": id})

        block = GridBlockView(
            config["abbr-ua"],
            self.parent.block_pos,
            default_config=config,
            parent=self.parent
        )
        self.blocks.add(block)
        self.update_neighbors(block)

        self.parent.draw_block(block)

    def remove_block(self, block):
        """"""
        self.cached_block = block
        self.update_neighbors(block, leaves=True)
        self.cached_block.setParent(None)
        self.cached_block.grid_pos = (-10, -10)

    def reveal_block(self, pos):
        """"""
        block = self.cached_block
        block.grid_pos = pos
        self.update_neighbors(block)
        self.parent.draw_block(block)

    def update_neighbors(self, c_block, leaves=False):
        """"""
        if leaves:
            for block in c_block.neighbors[:]:
                block.allowed_neighbors.append(c_block.config["abbr"])
                block.neighbors.remove(c_block)

                c_block.allowed_neighbors.append(block.config["abbr"])
                c_block.neighbors.remove(block)
        else:
            neighbors, _ = self.check_neighbours(
                c_block.config["abbr"],
                c_block.grid_pos
            )

            for block in neighbors:
                block.allowed_neighbors.remove(c_block.config["abbr"])
                block.neighbors.append(c_block)

                c_block.allowed_neighbors.remove(block.config["abbr"])
                c_block.neighbors.append(block)

        c_block.update_state()

    def check_neighbours(self, name, pos):
        """"""
        c_x, c_y = self.parent.index_hint(pos)
        valid = []
        not_valid = []

        for block in self.blocks:
            x, y = block.grid_pos
            d = ((c_x - x) ** 2 + (c_y - y) ** 2) ** 0.5
            if d < 3:
                not_valid.append(block)
            elif d == 3:
                if name in block.allowed_neighbors:
                    valid.append(block)
                else:
                    not_valid.append(block)

        return valid, not_valid


class GridBlockView(BlockView):
    """View for block in Block Panel"""
    def __init__(self, name, grid_pos, default_config={}, parent=None):
        super().__init__(GridBlockLabel(name), parent)

        self.name = name
        self.grid_pos = grid_pos
        self.config = self.default_config = default_config
        self.neighbors = []
        self.allowed_neighbors = self.config["allowed"][:]

        self.store = BlockStore(
            self.config["id"],
            self.config["name"],
            False,
            []
        )
        self.parent().block_state_notifier.add_state(self.store)
        self.parent().block_state_notifier.notify_all()

        self.init_gui()
        tip = "{}: {}".format(self.config["name"], self.config["id"])
        self.setToolTip(tip)

    def mouseDoubleClickEvent(self, e):
        """Invoke modal window with set of options"""
        modal = self.config["modal"](self.config.copy())

        if modal.exec_():
            self.config.update({"values": modal.values})

    def mouseMoveEvent(self, e):
        """Event for dragging out block to the Block Zone"""
        if e.buttons() != Qt.LeftButton:
            return

        self.parent().block_manager.remove_block(self)

        mimeData = qtc.QMimeData()
        mimeData.setText(self.config["abbr"] + " " + self.config["id"])

        drag = qtg.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(qtg.QPixmap("img/block.png"))
        drag.exec_(Qt.MoveAction)

    def delete(self):
        self.parent().block_state_notifier.remove_state(self.store.id)
        self.parent().block_state_notifier.notify_all()
        self.parent().block_manager.remove_block(self)

    def notify_neighbors(self):
        """"""
        for block in self.neighbors:
            if self.config["abbr"] in block.config["depends"]:
                block.update_state()

    def update_state(self):
        """"""
        print(self.config["id"])
        self.notify_neighbors()


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
            self.parent().delete()

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

    def dragEnterEvent(self, e):
        """Accept creating new blocks"""
        pos = self.grid_pos
        manager = self.parent().block_manager
        abbr = e.mimeData().text().split(" ")[0]
        _, blocks = manager.check_neighbours(abbr, self.grid_pos)

        if blocks:
            pos = self.parent().block_pos

        self.parent().hover_in(pos)
        e.accept()

    def dragLeaveEvent(self, e):
        """Accept creating new blocks"""
        self.parent().hover_out()
        e.accept()

    def dropEvent(self, e):
        """Create new block where mouse drops"""
        self.parent().event(e)
