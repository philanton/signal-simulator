from dataclasses import dataclass

from PySide6.QtGui import QColor


class StateNotifier():
    """"""
    def __init__(self):
        self._states = {}
        self._observers = []

    def add_state(self, state):
        """"""
        self._states[state.id] = state

    def remove_state(self, id):
        """"""
        return self._states.pop(id)

    def get_states(self):
        """"""
        return self._states.values()

    def get_state(self, id):
        """"""
        return self._states.get(id, None)

    def add_observer(self, func):
        """"""
        self._observers.append(func)

    def notify_all(self, concrete=[]):
        """"""
        for func in self._observers:
            func(*self._states.values(), concrete=concrete)


@dataclass
class BlockStore:
    id: str
    name: str
    done: bool
    values: list
    times: list

    def __hash__(self):
        return hash(self.id)


@dataclass
class ElementStore:
    id: str
    values: list
    times: list
    color: QColor
    show: bool

    def __hash__(self):
        return hash(self.id)
