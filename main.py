import json
import sys
from psychopy import visual, core, event
from dataset import Dataset

CONFIG_PATH = "./configurations/{}.json".format(sys.argv[1])
with open(CONFIG_PATH, "r") as f:
    CONF = json.load(f)

dataset = Dataset(CONF["dataset_name"])
window = visual.Window(CONF["screen_size"], monitor="testMonitor", units="norm")
fixation = visual.TextStim(window, text="+")
word = visual.TextStim(window)
TASK_DISTANCE = 0.66
task_before = visual.TextStim(window, text=CONF["tasks"]["before"], pos=[0-TASK_DISTANCE, 0])
task_after = visual.TextStim(window, text=CONF["tasks"]["after"], pos=[TASK_DISTANCE, 0])

fixation.draw()
window.flip()

# gate
while CONF["keys"]["start"] not in event.waitKeys():
    pass

core.wait(CONF["timing"]["first_fixation"])

while not dataset.is_finished():
    task_before.color = CONF["colors"]["thinking"]
    task_after.color = CONF["colors"]["thinking"]
    task_before.draw()
    task_after.draw()
    word.setText(dataset.middle_word())
    word.draw()
    window.flip()

    core.wait(CONF["timing"]["thinking"])
    task_before.color = CONF["colors"]["before"]
    task_after.color = CONF["colors"]["after"]
    task_before.draw()
    task_after.draw()
    word.draw()
    window.flip()

    # TODO: add logic to ignore unwanted keys
    allKeys=event.waitKeys()
    for thisKey in allKeys:
        if thisKey in CONF["keys"]["before"]:
            dataset.split_dataset("before")
            break
        elif thisKey in CONF["keys"]["after"]:
            dataset.split_dataset("after")
            break

    fixation.draw()
    window.flip()
    core.wait(CONF["timing"]["resting"])


print "Your word is:", dataset.middle_word()
