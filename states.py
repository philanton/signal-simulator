from dataclasses import dataclass

from PySide6.QtGui import QColor


class StateNotifier():
    """"""
    def __init__(self):
        self._states = []
        self._observers = []

    def add_state(self, state):
        self._states.append(state)

    def remove_state(self, id):
        i = [i for i, state in enumerate(self._states) if state.id == id][0]
        self._states.pop(i)

    def get_states(self):
        return self._states[:]

    def get_state(self, id):
        return [state for state in self._states if state.id == id][0]

    def add_observer(self, func):
        self._observers.append(func)

    def notify_all(self):
        for func in self._observers:
            func(*self._states)


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
    done: bool
    values: list
    times: list
    color: QColor
    show: bool

    def __hash__(self):
        return hash(self.id)
