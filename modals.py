import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from classes.basewidgets import BaseLabel, BaseWidget


class BaseModal(qtw.QDialog, BaseWidget):
    """Parent widget for all modal windows with sets of options"""
    def __init__(self, config):
        super().__init__()

        self.config = config

        self.setWindowTitle(
            "Настройка параметрів: {}".format(self.config["name"])
        )

    def init_gui(self, options):
        """"""
        self._init_sizing(width=400)

        self._init_buttons()
        form = self._init_options(options)
        self._init_layout(
            [
                BaseLabel(self.config["description"], self),
                form,
                self.buttonBox
            ],
            margins=(5, 5, 5, 5),
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#88D9E6")
        })

    def _init_options(self):
        """"""
        form_layout = qtw.QFormLayout()

        for params in options:
            form_layout.addRow(*params)

        form_widget = qtw.QWidget()
        form_widget.setLayout(form_layout)
        return form_widget

    def _init_buttons(self):
        buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel
        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


# Here will be classes for modals


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
