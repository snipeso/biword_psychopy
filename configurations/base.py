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
    "classifier_directions":{
        "1": "before",
        "2": "after",
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
        "spacing": 1,
        "color": "white",
        "distance": 0.9,
        "height": 0.04,
        "length": 0.8, #percent of screen size
    }
}
