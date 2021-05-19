from modals import (DataSourceModal,
                    InterferenceModal,
                    ConnectionLineModal,
                    CorrelatorModal,
                    ReferenceDSModal)

blocks = [
    {
        "name": "Джерело сигналу",
        "description": "",
        "abbr": "DS",
        "abbr-ua": "ДС",
        "allowed": ["CL"],
        "depends": [],
        "modal": DataSourceModal,
        "values": {
            "type": 0,
            "amplitude": 5,
            "frequency": 2,
            "phase": 0,
            "periods_per_symbol": 5,
            "counts_per_period": 10,
            "counts_per_symbol": 50,
            "length": 2
        }
    },
    {
        "name": "Лінія зв'язку",
        "description": "",
        "abbr": "CL",
        "abbr-ua": "ЛЗ",
        "allowed": ["DS", "Infr", "Corr"],
        "depends": ["DS", "Infr"],
        "modal": ConnectionLineModal,
        "values": {
            "infr_coef": 0.3,
            "signal_coef": 0.7,
            "counts_per_symbol": 50
        }
    },
    {
        "name": "Завада",
        "description": "",
        "abbr": "Infr",
        "abbr-ua": "Звд",
        "allowed": ["CL"],
        "depends": [],
        "modal": InterferenceModal,
        "values": {
            "type": 0,
            "amplitude": 5,
            "counts_per_symbol": 50
        }
    },
    {
        "name": "Коррелятор",
        "description": "",
        "abbr": "Corr",
        "abbr-ua": "Корр",
        "allowed": ["CL", "RDS", "DD"],
        "depends": ["CL", "RDS"],
        "modal": CorrelatorModal,
        "values": {
            "counts_per_symbol": 50
        }
    },
    {
        "name": "Джерело еталонного сигналу",
        "description": "",
        "abbr": "RDS",
        "abbr-ua": "ДЕС",
        "allowed": ["Corr"],
        "depends": [],
        "modal": ReferenceDSModal,
        "values": {
            "id": ""
        }
    },
    {
        "name": "Джерело опорного сигналу",
        "description": "",
        "abbr": "PDS",
        "abbr-ua": "ДОС",
        "allowed": ["DD"],
        "depends": [],
        "values": {
            "pivot_signal_level": 4
        }
    },
    {
        "name": "Пристрій прийняття рішення",
        "description": "",
        "abbr": "DD",
        "abbr-ua": "ППР",
        "allowed": ["Corr", "PDS"],
        "depends": ["Corr", "PDS"],
        "values": {
            "pivot_signal_level": 4
        }
    }
]
