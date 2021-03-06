import string

CONF = {
    "name": "base",
    "dataset": {
        "name": "american-english",
        "to_clean": True,
    },
    "triggers_per_second": 3,
    "keys": {
        "before": ["1", "left", "minus"],
        "after": ["2", "right", "plus"],
        "start": "5",
    },
    "screen": {
        "size": [800, 600],
        "color": "black",
        "monitor": "testMonitor",
    },
    "tasks": {
    "instructions": {
        "before": "TALK",
        "after": "DRAW",
    },
    "colors": {
        "before": "green",
        "after": "red",
        "planning": "white",
    },
    "distance": 0.58,
    "height": 0.07,
    },
    "alphabet": {
        "letters" : string.ascii_uppercase,
        "length": 0.53, #percent of screen size
        "y_position": 0.8,
        "height": 0.07,
    },
    "classifier": {
        "acceptance_treshold": 0.2,
        "directions":{
            -1: "before",
             1: "after",
        },
    }
}
