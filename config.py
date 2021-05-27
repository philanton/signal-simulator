from modals import (DataSourceModal,
                    InterferenceModal,
                    ConnectionLineModal,
                    CorrelatorModal,
                    ClockGenModal,
                    ReferenceDSModal)

blocks = [
    {
        "name": "Джерело сигналу",
        "description": "",
        "abbr": "DS",
        "abbr-ua": "ДС",
        "allowed": ["CL"],
        "modal": DataSourceModal,
        "values": {
            "type": 0,
            "amplitude": 5,
            "frequency": 2,
            "phase": 0,
            "periods_per_symbol": 5,
            "counts_per_period": 10,
            "counts_per_symbol": 50,
            "bytes": "10"
        }
    },
    {
        "name": "Лінія зв'язку",
        "description": "",
        "abbr": "CL",
        "abbr-ua": "ЛЗ",
        "allowed": ["DS", "Infr", "Corr"],
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
        "allowed": ["CL", "CG", "RDS", "DD"],
        "modal": CorrelatorModal,
        "values": {
            "counts_per_symbol": 50
        }
    },
    {
        "name": "Тактовий генератор",
        "description": "",
        "abbr": "CG",
        "abbr-ua": "ТГ",
        "allowed": ["Corr"],
        "modal": ClockGenModal,
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
        "values": {
            "pivot_signal_level": 4
        }
    }
]
