from base import CONF

CONF.update({
    "name": "debug",
    "trigger_timing": {
        "first_fixation": 1,
        "planning": 1,
        "thinking": 1,
        "resting": 1,
        "last_fixation": 1,
    },
})
