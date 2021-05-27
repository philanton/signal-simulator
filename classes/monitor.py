import PySide6.QtGui as qtg

from classes.basewidgets import BaseWidget


class Monitor(BaseWidget):
    """It's a monitor with plots of signals"""
    def __init__(self, notifier, parent=None):
        super().__init__(parent)
        self.element_state_notifier = notifier
        self.element_state_notifier.add_observer(self.update_graph)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(height=200)

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#526760")
        })

    def update_graph(self, *states, concrete=[]):
        """"""
        if concrete:
            states = [state for state in states if state.id in concrete]
        for state in states:
            print(state.id, state.show, state.color)
