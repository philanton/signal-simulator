import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt


class BaseModal(qtw.QDialog):
    """Parent widget for all modal windows with sets of options"""
    def __init__(self):
        super().__init__()

        self.options = {"option": "value"}

        self.setWindowTitle("Base Modal")

        QBtn = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel

        self.buttonBox = qtw.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = qtw.QVBoxLayout()
        message = qtw.QLabel("Invoked modal Window")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
