import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from classes.basewidgets import BaseLabel, BaseWidget


class BaseModal(qtw.QDialog, BaseWidget):
    """Parent widget for all modal windows with sets of options"""
    def __init__(self, config):
        super().__init__()

        self.name = config["name"]
        self.description = config["description"]
        self.values = config["values"].copy()
        self.options = []

        self._init_options()
        self.init_gui()

        self.setWindowIcon(qtg.QIcon("img/app-block.png"))
        self.setWindowTitle(
            "Настройка параметрів: {}".format(self.name)
        )

    def init_gui(self):
        """"""
        self._init_sizing(width=400)

        self._init_buttons()
        self.form = self._init_form()
        self._init_layout(
            [
                BaseLabel(self.description, self),
                self.form,
                self.buttonBox
            ],
            margins=(5, 5, 5, 5),
        )

        self._init_palette({
            qtg.QPalette.Window: qtg.QColor("#88D9E6")
        })

    def _init_options(self):
        pass

    def _init_form(self):
        """"""
        form_layout = qtw.QFormLayout()

        for params in self.options:
            form_layout.addRow(*params)

        form_widget = qtw.QWidget()
        form_widget.setLayout(form_layout)
        return form_widget

    def _init_buttons(self):
        buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel
        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


class DataSourceModal(BaseModal):
    """"""
    def __init__(self, config):
        super().__init__(config)

    def _init_options(self):
        """"""
        variations = ["Гармонічний сигнал", "Манчестерський код"]
        button_group = qtw.QButtonGroup()
        radio_layout = qtw.QHBoxLayout()
        for index, radio in enumerate(variations):
            radio_button = qtw.QRadioButton(radio)
            radio_button.clicked.connect(
                lambda a=True, i=index: self.__type_changed(i)
            )
            radio_layout.addWidget(radio_button)
            button_group.addButton(radio_button)
            if index == self.values["type"]:
                radio_button.setChecked(True)
        self.options.append([radio_layout])

        amplitude = qtw.QDoubleSpinBox()
        amplitude.setValue(self.values["amplitude"])
        amplitude.setRange(0.01, 10)
        amplitude.valueChanged.connect(
            lambda a: self.values.update({"amplitude": a})
        )
        self.options.append(["Амплітуда", amplitude])

        self.__init_form_analog()
        self.__init_form_discrete()
        self.options.append([self.inner_form_a])
        self.options.append([self.inner_form_b])
        if self.values["type"] == 1:
            self.inner_form_a.hide()
        else:
            self.inner_form_b.hide()

        bytes = qtw.QLineEdit()
        bytes.setText(self.values["bytes"])
        bytes.setInputMask("bbbbbbbb")
        bytes.textChanged.connect(
            lambda a: self.values.update({"bytes": a})
        )
        self.options.append(["Символи для передачі", bytes])

    def __type_changed(self, i):
        """"""
        if self.values["type"] == i:
            return

        if i == 0:
            cp = self.values["counts_per_period"]
            ps = self.values["periods_per_symbol"]
            self.values["counts_per_period"] = cp * ps
            self.inner_form_a.show()
            self.inner_form_b.hide()
        else:
            self.inner_form_a.hide()
            self.inner_form_b.show()
        self.adjustSize()

        self.values["type"] = i

    def __init_form_analog(self):
        """"""
        layout = qtw.QFormLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        phase = qtw.QCheckBox()
        phase.setChecked(self.values["phase"])
        phase.stateChanged.connect(
            lambda a: self.values.update({"phase": bool(a)})
        )
        layout.addRow("Зворотній", phase)

        frequency = qtw.QDoubleSpinBox()
        frequency.setValue(self.values["frequency"])
        frequency.setRange(0.01, 10)
        frequency.valueChanged.connect(
            lambda a: self.values.update({"frequency": a})
        )
        layout.addRow("Частота", frequency)

        periods_per_symbol = qtw.QSpinBox()
        periods_per_symbol.setValue(self.values["periods_per_symbol"])
        periods_per_symbol.setRange(1, 10)
        periods_per_symbol.valueChanged.connect(
            lambda a: self.values.update({
                "periods_per_symbol": a,
                "counts_per_symbol": a * self.values["counts_per_period"]
            })
        )
        layout.addRow("Періоди / Символ", periods_per_symbol)

        counts_per_period = qtw.QSpinBox()
        counts_per_period.setValue(self.values["counts_per_period"])
        counts_per_period.setRange(1, 50)
        counts_per_period.valueChanged.connect(
            lambda a: self.values.update({
                "counts_per_period": a,
                "counts_per_symbol": a * self.values["periods_per_symbol"]
            })
        )
        layout.addRow("Відліки / Період", counts_per_period)

        self.inner_form_a = qtw.QWidget()
        self.inner_form_a.setLayout(layout)

    def __init_form_discrete(self):
        """"""
        layout = qtw.QFormLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        counts_per_symbol = qtw.QSpinBox()
        counts_per_symbol.setValue(self.values["counts_per_symbol"])
        counts_per_symbol.setRange(1, 100)
        counts_per_symbol.valueChanged.connect(
            lambda a: self.values.update({"counts_per_symbol": a})
        )
        layout.addRow("Відліки / Символ  ", counts_per_symbol)

        self.inner_form_b = qtw.QWidget()
        self.inner_form_b.setLayout(layout)


class InterferenceModal(BaseModal):
    """"""
    def __init__(self, config):
        super().__init__(config)

    def _init_options(self):
        """"""
        variations = ["Білий шум", "Сірий шум", "Імпульсна завада"]
        combo_box = qtw.QComboBox()
        combo_box.addItems(variations)
        combo_box.setCurrentIndex(self.values["type"])
        combo_box.currentIndexChanged.connect(
            lambda a: self.values.update({"type": a})
        )
        self.options.append(["Тип", combo_box])

        amplitude = qtw.QDoubleSpinBox()
        amplitude.setValue(self.values["amplitude"])
        amplitude.setRange(0.01, 10)
        amplitude.valueChanged.connect(
            lambda a: self.values.update({"amplitude": a})
        )
        self.options.append(["Амплітуда", amplitude])


class ConnectionLineModal(BaseModal):
    """"""
    def __init__(self, config):
        super().__init__(config)

    def _init_options(self):
        """"""
        signal_coef = qtw.QDoubleSpinBox()
        signal_coef.setValue(self.values["signal_coef"])
        signal_coef.setRange(0, 5)
        signal_coef.setSingleStep(0.1)
        signal_coef.valueChanged.connect(
            lambda a: self.values.update({"signal_coef": a})
        )
        self.options.append(["Коефіцієнт для сигналу", signal_coef])

        infr_coef = qtw.QDoubleSpinBox()
        infr_coef.setValue(self.values["infr_coef"])
        infr_coef.setRange(0, 5)
        infr_coef.setSingleStep(0.1)
        infr_coef.valueChanged.connect(
            lambda a: self.values.update({"infr_coef": a})
        )
        self.options.append(["Коефіцієнт для завади", infr_coef])


class ReferenceDSModal(BaseModal):
    """"""
    def __init__(self, config):
        super().__init__(config)


class CorrelatorModal(BaseModal):
    """"""
    def __init__(self, config):
        super().__init__(config)


class ClockGenModal(BaseModal):
    """"""
    def __init__(self, config):
        super().__init__(config)


class DecisionDeviceModal(BaseModal):
    """"""
    def __init__(self, config):
        super().__init__(config)

    def _init_options(self):
        """"""
        received_message = qtw.QLineEdit()
        received_message.setText(self.values["received_message"])
        received_message.setReadOnly(True)
        self.options.append(["Прийняте повідомлення", received_message])


class PivotDSModal(BaseModal):
    """"""
    def __init__(self, config):
        super().__init__(config)

    def _init_options(self):
        """"""
        pivot_signal_level = qtw.QSpinBox()
        pivot_signal_level.setValue(self.values["pivot_signal_level"])
        pivot_signal_level.setRange(0, 100)
        pivot_signal_level.valueChanged.connect(
            lambda a: self.values.update({"pivot_signal_level": a})
        )
        self.options.append(["Величина опорного сигналу, %", pivot_signal_level])
