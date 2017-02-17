from debug import CONF # Can be: debug, fast, slow

CONF.update({
  "participant": "001",
  "input_method": "manual", # Can be: auto, manual, network_long, network_short
  #"target_word": "respectfulness", # To be used for method is "auto"
})

for interval in CONF["trigger_timing"]:
    CONF["trigger_timing"][interval] =\
        CONF["trigger_timing"][interval] * CONF["triggers_per_second"]
