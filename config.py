from modals import (DataSourceModal,
                    InterferenceModal,
                    ConnectionLineModal,
                    CorrelatorModal,
                    ClockGenModal,
                    ReferenceDSModal,
                    PivotDSModal,
                    DecisionDeviceModal)

blocks = [
    {
        "name": "Джерело сигналу",
        "description": "Генерує масив даних відповідних вибраному типу сигналу"\
                       " довжиною рівною кількості відліків на символ "\
                       "(у випадку вибору типу \"Гармонічний сигнал\" добуток "\
                       "кількості відліків на період та "\
                       "кількості періодів на символ) помножену на кількість "\
                       "бітів записаних в полі \"Символи для передачі\".",
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
        "description": "З'єднує масиви даних відповідні переданому сигналу та"\
                       " заваді згідно до виставлених нижче коефіцієнтів."\
                       "Якщо на вході немає хоч одного з модулів ДС та Звд, то"\
                       " модуль на виході нічого не видає.",
        "abbr": "CL",
        "abbr-ua": "ЛЗ",
        "allowed": ["DS", "Infr", "Corr"],
        "modal": ConnectionLineModal,
        "values": {
            "infr_coef": 0.3,
            "signal_coef": 1,
            "counts_per_symbol": 50
        }
    },
    {
        "name": "Завада",
        "description": "Генерує масив даних згідно до вибраного типу завади та"\
                       " її амплітуди. Довжина масиву залежить від присутності"\
                       " цього модуля в одній системі з модулем ДС.",
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
        "description": "Генерує масив, що ілюструє взаємну кореляцію сигналів"\
                       " від модулів ДЕС та ЛЗ. Також для роботи є необхідним "\
                       "модуль ТГ.",
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
        "description": "Скидає в нуль значення корелятора при закінченні"\
                       "передачі кожного з символів.",
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
        "description": "Автоматично генерує сигнал, що є еталонним "\
                       "оригінальному. Якщо модуля ДС з таким оригінальним "\
                       "сигналом в системі немає, то на виході "\
                       "теж нічого немає.",
        "abbr": "RDS",
        "abbr-ua": "ДЕС",
        "allowed": ["Corr"],
        "modal": ReferenceDSModal,
        "values": {
            "id": "",
            "counts_per_symbol": 50
        }
    },
    {
        "name": "Джерело опорного сигналу",
        "description": "Контролює ймовірність допуску помилки модуля ППР.",
        "abbr": "PDS",
        "abbr-ua": "ДОС",
        "allowed": ["DD"],
        "modal": PivotDSModal,
        "values": {
            "pivot_signal_level": 70
        }
    },
    {
        "name": "Пристрій прийняття рішення",
        "description": "Аналізує масив даних переданий від модуля Корр "\
                       "та визначає кожен переданий символ. Якщо символ "\
                       "не вдалося розпізнати, то замінює його на '?'.",
        "abbr": "DD",
        "abbr-ua": "ППР",
        "allowed": ["Corr", "PDS"],
        "modal": DecisionDeviceModal,
        "values": {
            "received_message": ""
        }
    }
]
