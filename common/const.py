OBJECT_NUMBERS = {
    'ships': 200,
    'weapons': 20,
    'hulls': 5,
    'engines': 6,
}

CONSTRAINTS = {
    'engines': {
        'power': {
            'min': 0,
            'max': 100,
        },
        'type': {
            'min': 1,
            'max': 20,
        },
    },
    'hulls': {
        'armor': {
            'min': 0,
            'max': 100,
        },
        'type': {
            'min': 1,
            'max': 10,
        },
        'capacity': {
            'min': 0,
            'max': 100,
        },
    },
    'weapons': {
        'reload_speed': {
            'min': 0,
            'max': 1000,
        },
        'rotational_speed': {
            'min': 0,
            'max': 1000,
        },
        'diameter': {
            'min': 0,
            'max': 30,
        },
        'power_volley': {
            'min': 0,
            'max': 30,
        },
        'count': {
            'min': 0,
            'max': 5,
        },
    },
}