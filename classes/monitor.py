from PySide6.QtCore import Qt
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
import pyqtgraph as pg

from classes.basewidgets import BaseWidget


class Monitor(BaseWidget):
    """It's a monitor with plots of signals"""
    def __init__(self, notifier, parent=None):
        super().__init__(parent)
        self.element_state_notifier = notifier
        self.element_state_notifier.add_observer(self.update_graph)
        self.plots = {}
        self.states = []
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_sizing(height=250)

        self.graph = self._init_graph_and_return()
        self._init_fullscreen_graph()
        self._init_layout([self.graph])

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#526760")
        })

    def _init_graph_and_return(self):
        """"""
        graph = pg.PlotWidget()
        graph.setBackground("#88D9E6")
        graph.setAxisItems({
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
        graph.showGrid(x=True, y=True)

        return graph

    def _init_fullscreen_graph(self):
        """"""
        graph = self._init_graph_and_return()

        layout = qtw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(graph)

        self.dialog = qtw.QWidget()
        self.dialog.graph = graph
        self.dialog.setWindowIcon(qtg.QIcon("img/app-block.png"))
        self.dialog.setWindowTitle("Розширений перегляд")
        self.dialog.setLayout(layout)

    def update_graph(self, *states, concrete=[]):
        """"""
        self.graph.clear()
        self.states = [state for state in states if state.show]
        for state in self.states:
            color = state.color
            color.setAlphaF(0.7)
            self.plots[state.id] = self.graph.plot(
                state.times,
                state.values,
                pen=pg.mkPen(color=color, width=3)
            )

    def mouseDoubleClickEvent(self, e):
        """"""
        if e.buttons() != Qt.LeftButton:
            return

        self.dialog.graph.clear()
        for state in self.states:
            color = state.color
            color.setAlphaF(0.7)
            self.dialog.graph.plot(
                state.times,
                state.values,
                pen=pg.mkPen(color=color, width=3)
            )

        self.dialog.show()
