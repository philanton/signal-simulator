blocks = [
    {
        "name": "Джерело сигналу",
        "description": "",
        "abbr": "DS",
        "abbr-ua": "ДС",
        "options": [
            {
                "label": "Тип",
                "type": "radio",
                "variations": ["аналоговий", "дискретний"],
                "value": 0
            },
            {
                "label": "Амплітуда",
                "type": "num",
                "value": 1
            },
            {
                "label": "Частота",
                "type": "num",
                "value": 50
            },
            {
                "label": "Кількість періодів на логічний символ алфавіту",
                "attached": {"to": 0, "value": 0},
                "type": "num",
                "value": 2
            },
            {
                "label": "Кількість відліків на період",
                "attached": {"to": 0, "value": 0},
                "type": "num",
                "value": 2
            },
            {
                "label": "Кількість відліків на символ алфавіту",
                "attached": {"to": 0, "value": 1},
                "type": "num",
                "value": 4
            },
            {
                "label": "Кількість передаваємих символів",
                "type": "num",
                "value": 1
            }
        ]
    },
    {
        "name": "Лінія зв'язку'",
        "description": "",
        "abbr": "CL",
        "abbr-ua": "ЛЗ",
        "options": [
            {
                "label": "",
                "type": "",
                "value": 0
            }
        ]
    },
    {
        "name": "Завада",
        "description": "",
        "abbr": "Infr",
        "abbr-ua": "Звд",
        "options": [
            {
                "label": "Тип",
                "type": "radio",
                "variations": ["білий шум"],
                "value": 0
            },
            {
                "label": "Амплітуда",
                "type": "num",
                "value": 1
            },
            {
                "label": "Кількість відліків на символ алфавіту",
                "type": "num",
                "value": 3
            }
        ]
    },
    {
        "name": "Коррелятор",
        "description": "",
        "abbr": "Corr",
        "abbr-ua": "Корр",
        "options": {}
    },
    {
        "name": "Джерело еталонного сигналу",
        "description": "",
        "abbr": "RDS",
        "abbr-ua": "ДЕС",
        "options": {}
    },
    {
        "name": "Джерело опорного сигналу",
        "description": "",
        "abbr": "PDS",
        "abbr-ua": "ДОС",
        "options": {}
    },
    {
        "name": "Пристрій прийняття рішення",
        "description": "",
        "abbr": "DD",
        "abbr-ua": "ППР",
        "options": {}
    }
]
