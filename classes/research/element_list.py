from random import randint

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from classes.basewidgets import BaseWidget, BaseLabel
from classes.states import ElementStore


class ElementList(BaseWidget):
    """It's a list, where we can set options about available elements"""
    def __init__(self, bl_notifier, el_notifier, parent=None):
        super().__init__(parent)

        self.block_state_notifier = bl_notifier
        self.block_states = {}
        self.block_state_notifier.add_observer(self.update_list)

        self.element_state_notifier = el_notifier
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(size_policy=(
            qtw.QSizePolicy.Preferred,
            qtw.QSizePolicy.MinimumExpanding
        ))

        header = ElementListRow(is_header=True)
        self._init_layout(
            [
                header,
                ""
            ],
            margins=(1, 1, 1, 1),
            spacing=1
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#88D9E6")
        })

    def update_list(self, *states):
        last_states = set(self.block_states.keys())
        states = set(states)

        deleted = last_states.difference(states)
        added = states.difference(last_states)

        for state in deleted:
            self.block_states.pop(state).setParent(None)

        for state in added:
            list_item = ElementListRow(state)
            self.block_states[state] = list_item
            self._layout.insertWidget(len(last_states) + 1, list_item)


class ElementListRow(BaseWidget):
    """It's a list item with set of options for selected element"""
    def __init__(self, block_state=None, is_header=False, parent=None):
        super().__init__(parent)
        self.is_header = is_header
        self.block_state = block_state
        if not is_header:
            self.element_state = ElementStore(
                block_state.id,
                qtg.QColor(*[randint(0,256) for a in [0] * 3]),
                False
            )
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        items = []
        if self.is_header:
            items.append(CellLabel(45, "ID", bgcolor="#8B8BAE"))
            items.append(CellLabel(110, "Ім'я'", bgcolor="#8B8BAE"))
            items.append(CellLabel(60, "Колір", bgcolor="#8B8BAE"))
            items.append(CellLabel(45, "Показ", bgcolor="#8B8BAE"))
        else:
            items.append(CellLabel(45, self.block_state.id))
            items.append(CellLabel(110, self.block_state.name))
            items.append(CellColourPicker(60, self.element_state))
            items.append(CellCheckBox(45, self.element_state))

        self._init_layout(
            items,
            is_vertical=False,
            margins=(1, 1, 1, 1),
            spacing=2
        )


class CellLabel(BaseLabel):
    """"""
    def __init__(self, width, text, bgcolor="#C5FFFD"):
        super().__init__(text, parent=None)
        self.width = width
        self.bgcolor = bgcolor
        self.init_gui()

    def init_gui(self):
        """"""
        super().init_gui()
        self.setFixedWidth(self.width)
        self.setMargin(3)

        self._init_font()
        self.setWordWrap(True);

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor(self.bgcolor),
            qtg.QPalette.WindowText: qtg.QColor("#88D9E6")
        })


class CellCheckBox(BaseWidget):
    """"""
    def __init__(self, width, state):
        super().__init__(parent=None)
        self.width = width
        self.state = state
        self.init_gui()

    def init_gui(self):
        self._init_sizing(width=self.width)

        check_box = qtw.QCheckBox()
        check_box.setChecked(self.state.show)
        check_box.stateChanged.connect(self.change_state)
        self._init_layout(
            ["", check_box, ""],
            is_vertical=False,
            margins=(3, 3, 3, 3)
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#C5FFFD")
        })

    def change_state(self, num):
        self.state.show = bool(num)


class CellColourPicker(BaseWidget):
    """"""
    def __init__(self, width, state):
        super().__init__(parent=None)
        self.width = width
        self.state = state
        self.init_gui()

    def init_gui(self):
        self._init_sizing(width=self.width)

        self._init_picker()
        self._init_layout(
            ["", self.picker, ""],
            is_vertical=False,
            margins=(2, 2, 2, 2)
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#C5FFFD")
        })

    def _init_picker(self):
        """"""
        self.picker = qtw.QPushButton()
        self.picker.setFixedSize(50, 15)

        self.picker.setAutoFillBackground(True)
        self.color_palette = self.picker.palette()
        self.color_palette.setColor(qtg.QPalette.Button, self.state.color)
        self.picker.setPalette(self.color_palette)

        self.picker.clicked.connect(self.change_state)

    def change_state(self):
        color = qtw.QColorDialog.getColor(self.state.color)

        self.color_palette.setColor(qtg.QPalette.Button, color)
        self.picker.setPalette(self.color_palette)

        self.state.color = color
