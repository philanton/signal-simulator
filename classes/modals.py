import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt

from classes.basewidgets import BaseWidget, BaseLabel


class BaseModal(qtw.QDialog, BaseWidget):
    """Parent widget for all modal windows with sets of options"""
    def __init__(self, config):
        super().__init__()

        self.config = config

        self.setWindowTitle("Options: {}".format(self.config["name"]))
        self.init_gui()

    def init_gui(self):
        """"""
        self._init_sizing(width=400)

        self._init_buttons()
        form = self._init_options()
        self._init_layout(
            [
                BaseLabel(self.config["description"], self),
                form,
                self.buttonBox
            ],
            margins=(5, 5, 5, 5),
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#88D9E6") #"#C5FFFD"
        })

    def _form_by_type(self, option):
        return form_by_type[option["type"]](option)

    def _init_options(self):
        self.options = [
            self._form_by_type(option) for option in self.config["options"]
        ]

        form_layout = qtw.QFormLayout()
        for params in self.options:
            if params[0] == "radio":
                form_layout.addRow(params[1])
            elif params[0] == "num":
                form_layout.addRow(*params[1:])

        form_widget = qtw.QWidget()
        form_widget.setLayout(form_layout)
        return form_widget

    def _init_buttons(self):
        QBtn = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel
        self.buttonBox = qtw.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


form_by_type = {
    "radio": lambda a: radio_creator(a),
    "num": lambda a: num_creator(a)
}

def radio_creator(option):
    """"""
    button_group = qtw.QButtonGroup()
    radio_layout = qtw.QHBoxLayout()

    for index, radio in enumerate(option["variations"]):
        radio_button = qtw.QRadioButton(radio)
        radio_layout.addWidget(radio_button)
        button_group.addButton(radio_button)
        if index == option["value"]:
            radio_button.setChecked(True)

    return option["type"], radio_layout

def num_creator(option):
    return option["type"], option["label"], qtw.QSpinBox()
