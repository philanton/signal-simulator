import PySide6.QtGui as qtg
import pyqtgraph as pg

from classes.basewidgets import BaseWidget


class Monitor(BaseWidget):
    """It's a monitor with plots of signals"""
    def __init__(self, notifier, parent=None):
        super().__init__(parent)
        self.element_state_notifier = notifier
        self.element_state_notifier.add_observer(self.update_graph)
        self.plots = {}
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(height=250)

        self._init_graph()
        self._init_layout([self.graph])

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#526760")
        })

    def _init_graph(self):
        """"""
        self.graph = pg.PlotWidget()
        self.graph.setBackground("#88D9E6")
        self.graph.setAxisItems({
            'left': pg.AxisItem(
                'left',
                pen=pg.mkPen(color="#374B4A", width=2),
                textPen="#374B4A"
            ),
            'bottom': pg.AxisItem(
                'bottom',
                pen=pg.mkPen(color="#374B4A", width=2),
                textPen="#374B4A"
            )
        })
        self.graph.showGrid(x=True, y=True)

    def update_graph(self, *states, concrete=[]):
        """"""
        self.graph.clear()
        states = [state for state in states if state.show]
        for state in states:
            color = state.color
            color.setAlphaF(0.7)
            self.plots[state.id] = self.graph.plot(
                state.times,
                state.values,
                pen=pg.mkPen(color=color, width=3)
            )
