from base import CONF

CONF.update({
    "name": "fast",
    "trigger_timing": {
        "first_fixation": 20,
        "planning": 5,
        "thinking": 10,
        "resting": 5,
        "last_fixation": 20,
    },
})
