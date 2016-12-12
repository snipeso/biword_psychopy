import json
import sys
import os
import datetime
from psychopy import visual, core, event
from dataset import Dataset
from utils import append_data

# Summon Configurations
#CONF_NAME = sys.argv[1] #select configuration file from terminal when running script.
CONF_NAME = "debug"
CONF_PATH = os.path.join("configurations", "{}.json".format(CONF_NAME))
with open(CONF_PATH, "r") as f:
    CONF = json.load(f)
CONF["participant"] = "001"


# Create new file for the run
OUTPUT_FOLDER = "output"
OUTPUT_FILE_NAME = "{}_{}_{}".format(CONF["participant"], CONF_NAME,
    datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
output_file_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE_NAME)

with open("{}_conf.json".format(output_file_path), "w+") as f:
    f.write(json.dumps(CONF, indent=2))

HEADER = ["sequence", "word", "direction", "time_start_planning",
          "time_start_thinking", "time_answer"]
append_data(output_file_path, HEADER)


# Summon dataset with optional cleaning
dataset = Dataset(CONF["dataset"]["name"], CONF["dataset"]["to_clean"])


# Psychopy variables, based on configurations file
window = visual.Window(size=CONF["screen"]["size"],
                       color=CONF["screen"]["color"],
                       fullscr=True,
                       monitor=CONF["screen"]["monitor"],
                       units="norm")
FIXATION = core.StaticPeriod()
fixation_cross = visual.TextStim(window, text="+")
word = visual.TextStim(window)
task_before = visual.TextStim(window, text=CONF["tasks"]["instructions"]["before"],
                              pos=[0-CONF["tasks"]["distance"], 0], height=CONF["tasks"]["height"])
task_after = visual.TextStim(window, text=CONF["tasks"]["instructions"]["after"],
                             pos=[CONF["tasks"]["distance"], 0], height=CONF["tasks"]["height"])





# Presents simple fixation
fixation_cross.draw()
window.flip()


# Starts experiment with first input from scanner
while CONF["keys"]["start"] not in event.waitKeys():
    pass
clock = core.Clock()
core.wait(CONF["timing"]["first_fixation"])

# Main experiment loop
d_sequence = 0
while not dataset.is_finished():
    # Planning phase
    d_sequence += 1
    task_before.color = CONF["tasks"]["colors"]["planning"]
    task_after.color = CONF["tasks"]["colors"]["planning"]
    task_before.draw()
    task_after.draw()
    d_middle_word = dataset.middle_word()
    word.setText(d_middle_word.upper())
    word.draw()
    window.flip()
    d_time_start_planning = clock.getTime()
    core.wait(CONF["timing"]["planning"])

    # Thinking phase
    task_before.color = CONF["tasks"]["colors"]["before"]
    task_after.color = CONF["tasks"]["colors"]["after"]
    task_before.draw()
    task_after.draw()
    word.draw()
    window.flip()
    d_time_start_thinking = clock.getTime()
    core.wait(CONF["timing"]["thinking"])

    # Resting period
    FIXATION.start(CONF["timing"]["resting"])
    fixation_cross.draw()
    window.flip()


    # Waits for answer to proceed to next word
    direction = None
    while not direction:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey in CONF["keys"]["before"]:
                direction = "before"
            elif thisKey in CONF["keys"]["after"]:
                direction = "after"
            elif thisKey == "escape":
                sys.exit(1)
    d_time_answer = clock.getTime()

    # Waits for remaing time (if any) before presenting next stimulus
    FIXATION.complete()
    window.flip()

    # Adds data to csv file
    append_data(output_file_path,
                [d_sequence, d_middle_word, direction,
                 d_time_start_planning, d_time_start_thinking,
                 d_time_answer])

    # splits dataset to start the next loop
    dataset.split_dataset(direction)

print "Your word is:", dataset.middle_word()
