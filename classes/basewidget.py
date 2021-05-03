import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt
import PySide6.QtGui as qtg


class BaseWidget(qtw.QWidget):
    """
    Parent widget for all widgets.
    """
    def __init__(self, parent):
        super().__init__(parent)

    def _init_layout(self, inner_widgets, is_vertical=True,
                     margins=(0,0,0,0), spacing=0):
        """"""
        self._layout = qtw.QVBoxLayout() if is_vertical else qtw.QHBoxLayout()
        self._layout.setContentsMargins(*margins)
        self._layout.setSpacing(spacing)

        for widget in inner_widgets:
            if widget:
                self._layout.addWidget(widget)
            else:
                self._layout.addStretch(1)

        self.setLayout(self._layout)

    def _init_palette(self, color_dict={}):
        """"""
        self.setAutoFillBackground(True)
        palette = self.palette()
        for place, color in color_dict.items():
            palette.setColor(place, color)
        self.setPalette(palette)

    def _init_sizing(self, size_policy=(), width=(), height=()):
        """"""
        def set_size_by_property_length(set_size=lambda: pass, property):
            if len(property) == 0:
                pass
            elif len(property) == 1:
                set_size(property[0], property[0])
            else:
                set_size(property[0], property[1])

        set_size_by_property_length(lambda a, b: self.setSizePolicy(a, b),
                                    size_policy)
        set_size_by_property_length(lambda a, b: self._set_width(a, b),
                                    width)
        set_size_by_property_length(lambda a, b: self._set_height(a, b),
                                    height)

    def _set_width(min, max):
        self.setMinimumWidth(min)
        self.setMaximumWidth(max)

    def _set_height(min, max):
        self.setMinimumHeight(min)
        self.setMaximumHeight(max)
