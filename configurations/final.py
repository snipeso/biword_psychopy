from debug import CONF # Can be: debug, fast, slow

CONF.update({
  "participant": "0023",
  "input_method": "network_long", # Can be: auto, manual, network_long, network_short
  "target_word": "respectfulness", # To be used for method "auto"
})
CONF['classifier']['acceptance_treshold'] = 0.2

for interval in CONF["trigger_timing"]:
    CONF["trigger_timing"][interval] =\
        CONF["trigger_timing"][interval] * CONF["triggers_per_second"]
