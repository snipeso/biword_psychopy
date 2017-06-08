from base import CONF

CONF.update({
    "name": "slow",
    "trigger_timing": {
        "first_fixation": 25,
        "planning": 5,
        "thinking": 10,
        "resting": 25,
        "last_fixation": 30,
    },
})
