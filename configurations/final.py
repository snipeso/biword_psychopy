from whichever import CONFIG

CONFIG.update({
  "input_method": "manual",  # OPTIONS:
  "participant": "John Watson",
})

for interval in CONF["trigger_timing"]:
    CONF["trigger_timing"][interval] =\
        CONF["trigger_timing"][interval] * CONF["triggers_per_second"]
