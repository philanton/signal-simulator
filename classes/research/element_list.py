import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
import snoop

from classes.basewidgets import BaseWidget
from classes.research.element_list_item import ElementListRow


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
                "",
                header
            ],
            margins=(5, 5, 5, 5),
            spacing=5
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
            list_item = ElementListRow({
                "id": state.id,
                "name": state.name,
                "colour": "red"
            })

            self.block_states[state] = list_item
            self._layout.addWidget(list_item)

        print(self.block_states)
