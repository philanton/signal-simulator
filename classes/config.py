blocks = [
    {
        "name": "Data Source",
        "description": "",
        "abbr": "DS",
        "options": [
            {
                "label": "Type",
                "type": "radio",
                "variations": ["analog", "discrete"],
                "value": 0
            },
            {
                "label": "Amplitude",
                "type": "num",
                "value": 1
            },
            {
                "label": "Frequency",
                "type": "num",
                "value": 50
            },
            {
                "label": "Periods per symbol",
                "attached": {"to": "Type", "value": 0},
                "type": "num",
                "value": 2
            },
            {
                "label": "Counts per period",
                "attached": {"to": "Type", "value": 0},
                "type": "num",
                "value": 2
            },
            {
                "label": "Counts per symbol",
                "attached": {"to": "Type", "value": 1},
                "type": "num",
                "value": 4
            },
            {
                "label": "Length",
                "type": "num",
                "value": 1
            }
        ]
    },
    {
        "name": "Communication Line",
        "description": "",
        "abbr": "CL",
        "options": [
            {
                "label": "",
                "type": "",
                "value": 0
            }
        ]
    },
    {
        "name": "Interference",
        "description": "",
        "abbr": "Infr",
        "options": [
            {
                "label": "Type",
                "type": "radio",
                "value": 0
            },
            {
                "label": "Amplitude",
                "type": "num",
                "value": 1
            },
            {
                "label": "Counts per Symbol",
                "type": "num",
                "value": 3
            }
        ]
    },
    {
        "name": "Correlator",
        "description": "",
        "abbr": "Corr",
        "options": {}
    },
    {
        "name": "Reference Data Source",
        "description": "",
        "abbr": "RDS",
        "options": {}
    }
]
