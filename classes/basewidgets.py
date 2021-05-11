import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt


class BaseWidget(qtw.QWidget):
    """
    Parent widget for all widgets.
    """
    def __init__(self, parent):
        super().__init__(parent)

    def init_gui(self):
        """Separate function for GUI initialization"""
        pass

    def _init_layout(self, inner_widgets, is_vertical=True,
                     margins=(0, 0, 0, 0), spacing=0):
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
        def set_size_by_property_length(set_size=lambda: 0, property=()):
            if not property:
                return
            if type(property) is int:
                set_size(property, property)
            elif type(property) is tuple:
                set_size(property[0], property[1])

        set_size_by_property_length(lambda a, b: self.setSizePolicy(a, b),
                                    size_policy)
        set_size_by_property_length(lambda a, b: self._set_width(a, b),
                                    width)
        set_size_by_property_length(lambda a, b: self._set_height(a, b),
                                    height)

    def _set_width(self, min, max):
        self.setMinimumWidth(min)
        self.setMaximumWidth(max)

    def _set_height(self, min, max):
        self.setMinimumHeight(min)
        self.setMaximumHeight(max)


class BlockView(BaseWidget):
    """View for block"""
    def __init__(self, label, parent):
        super().__init__(parent)
        self.label = label

    def init_gui(self):
        """Separate function for GUI initialization"""
        self._init_layout(
            [self.label],
            margins=(3, 3, 3, 3)
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#88D9E6")
        })


class BaseLabel(qtw.QLabel):
    """
    Parent widget for custom labels
    """
    def __init__(self, text, parent):
        super().__init__(parent)
        self.text = text

    def init_gui(self):
        """Separate function for GUI initialization"""
        self.setText(self.text)

    def _init_palette(self, color_dict={}):
        """"""
        self.setAutoFillBackground(True)
        palette = self.palette()
        for place, color in color_dict.items():
            palette.setColor(place, color)
        self.setPalette(palette)

    def _init_font(self, family="Times", size=10,
                   is_bold=False, is_italic=False):
        font = qtg.QFont(family, size)
        font.setBold(is_bold)
        font.setItalic(is_italic)
        self.setFont(font)


class BlockLabel(BaseLabel):
    """
    Label class for blocks
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        super().init_gui()

        self.setAttribute(Qt.WA_Hover)

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#C5FFFD"),
            qtg.QPalette.WindowText: qtg.QColor("#88D9E6")
        })

        self._init_font("monospace", 13, is_bold=True)

        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def hover(self, leaves=False):
        """"""
        if self.hasFocus():
            return

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#C5FFFD" if leaves else "#8B8BAE")
        })

    def event(self, event):
        """Control Hover Event"""
        if event.type() == qtc.QEvent.HoverEnter:
            self.setCursor(Qt.OpenHandCursor)
            self.hover()
        elif event.type() == qtc.QEvent.HoverLeave:
            self.hover(leaves=True)

        return super().event(event)
