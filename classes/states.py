from collections import namedtuple


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


BlockStore = namedtuple("BlockStore", "id name")
ElementStore = namedtuple("ElementStore", "id colour")
