import json
import sys
from psychopy import visual, core, event
from dataset import Dataset

CONFIG_PATH = "./configurations/{}.json".format(sys.argv[1])
with open(CONFIG_PATH, "r") as f:
    CONF = json.load(f)

dataset = Dataset(CONF["dataset_name"])
window = visual.Window(CONF["screen_size"], monitor="testMonitor", units="deg")
fixation = visual.TextStim(window,text="+", alignHoriz="center", alignVert="center")
word = visual.TextStim(window, alignHoriz="center", alignVert="center")


fixation.draw()
window.flip()

# gate
while CONF["keys"]["start"] not in event.waitKeys():
    pass

core.wait(CONF["timing"]["first_fixation"])

while not dataset.is_finished():
    word.setText(dataset.middle_word())
    word.draw()
    window.flip()

    allKeys=event.waitKeys()
    for thisKey in allKeys:
        if thisKey in CONF["keys"]["before"]:
            dataset.split_dataset("before")
            break
        elif thisKey in CONF["keys"]["after"]:
            dataset.split_dataset("after")
            break


print "Your word is:", dataset.middle_word()
