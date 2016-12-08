import json
import sys
import os
import datetime
from psychopy import visual, core, event
from dataset import Dataset
from utils import append_data

CONF_NAME = sys.argv[1]
CONF_PATH = os.path.join("configurations", "{}.json".format(CONF_NAME))
with open(CONF_PATH, "r") as f:
    CONF = json.load(f)

OUTPUT_FOLDER = "output"
OUTPUT_FILE_NAME = "{}_{}_{}".format(CONF["participant"], CONF_NAME,
    datetime.datetime.now())
output_file_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE_NAME)

with open("{}_conf.json".format(output_file_path), "w+") as f:
    f.write(json.dumps(CONF, indent=2))

HEADER = ["sequence", "word", "direction", "time_start_planning",
          "time_start_thinking", "time_answer"]
append_data(output_file_path, HEADER)

dataset = Dataset(CONF["dataset_name"])

window = visual.Window(CONF["screen_size"], monitor="testMonitor", units="norm")
FIXATION = core.StaticPeriod()
fixation_cross = visual.TextStim(window, text="+")
word = visual.TextStim(window)
TASK_DISTANCE = 0.66
task_before = visual.TextStim(window, text=CONF["tasks"]["before"], pos=[0-TASK_DISTANCE, 0])
task_after = visual.TextStim(window, text=CONF["tasks"]["after"], pos=[TASK_DISTANCE, 0])

fixation_cross.draw()
window.flip()

# gate
while CONF["keys"]["start"] not in event.waitKeys():
    pass
clock = core.Clock()
core.wait(CONF["timing"]["first_fixation"])

d_sequence = 0
while not dataset.is_finished():
    d_sequence += 1
    task_before.color = CONF["colors"]["planning"]
    task_after.color = CONF["colors"]["planning"]
    task_before.draw()
    task_after.draw()
    word.setText(dataset.middle_word())
    word.draw()
    window.flip()
    d_time_start_planning = clock.getTime()
    core.wait(CONF["timing"]["planning"])

    task_before.color = CONF["colors"]["before"]
    task_after.color = CONF["colors"]["after"]
    task_before.draw()
    task_after.draw()
    word.draw()
    window.flip()
    d_time_start_thinking = clock.getTime()

    core.wait(CONF["timing"]["thinking"])

    FIXATION.start(CONF["timing"]["resting"])
    fixation_cross.draw()
    window.flip()


    # TODO: add logic to ignore unwanted keys
    direction = None
    while not direction:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey in CONF["keys"]["before"]:
                direction = "before"
            elif thisKey in CONF["keys"]["after"]:
                direction = "after"

    d_time_answer = clock.getTime()

    FIXATION.complete()
    window.flip()
    append_data(output_file_path,
                [d_sequence, dataset.middle_word(), direction,
                 d_time_start_planning, d_time_start_thinking,
                 d_time_answer])

    dataset.split_dataset(direction)

print "Your word is:", dataset.middle_word()
