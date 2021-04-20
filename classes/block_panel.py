import PySide6.QtWidgets as qtw

class BlockPanel(qtw.QWidget):
    """Class for panel, which have all available blocks"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        """Separate function for GUI initialization"""
        horizontal_layout = qtw.QHBoxLayout()

        # create and add blocks
        for value in ['Sender', 'Receiver', 'Middle', 'Other']:
            label = qtw.QLabel(self)
            label.setText(value)
            horizontal_layout.addWidget(label)
        self.setLayout(horizontal_layout)
