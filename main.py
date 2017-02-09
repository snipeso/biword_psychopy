import json
import sys
import os
import datetime
import zmq
from psychopy import visual, core, event
from dataset import Dataset
from utils import append_data, wait_trigger

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



zmq_context = zmq.Context()
socket = zmq_context.socket(zmq.PULL)
socket.bind("tcp://*:5555")


# Presents simple fixation
fixation_cross.draw()
window.flip()


wait_trigger(1)
# starts clock for timestamping events
clock = core.Clock()
# waits for first n triggers with fixation, not counting the first
wait_trigger(CONF["trigger_timing"]["first_fixation"]-1)



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
    wait_trigger(CONF["trigger_timing"]["planning"])


    # Thinking phase
    task_before.color = CONF["tasks"]["colors"]["before"]
    task_after.color = CONF["tasks"]["colors"]["after"]
    task_before.draw()
    task_after.draw()
    word.draw()
    window.flip()
    d_time_start_thinking = clock.getTime()
    wait_trigger(CONF["trigger_timing"]["thinking"])


    # Resting period
    fixation_cross.draw()
    window.flip()


    # Waits for answer to proceed to next word
    direction = None
    trigger_count = 0

    if CONF["input_method"] == "network":
        classifier_datapoint = float(socket.recv())
        direction = "before" if classifier_datapoint < 0 else "after"

    else if CONF["input_method"] == "manual":
        while not direction or trigger_count < CONF["trigger_timing"]["resting"]:
            for thisKey in event.waitKeys():
                if thisKey in CONF["keys"]["before"]:
                    direction = "before"
                elif thisKey in CONF["keys"]["after"]:
                    direction = "after"
                elif thisKey == "escape":
                    sys.exit(1)
                elif thisKey == "5":
                    trigger_count += 1
    d_time_answer = clock.getTime()

    window.flip()

    # Adds data to csv file
    append_data(output_file_path,
                [d_sequence, d_middle_word, direction,
                 d_time_start_planning, d_time_start_thinking,
                 d_time_answer])

    # splits dataset to start the next loop
    dataset.split_dataset(direction)

word.setText("{}!".format(dataset.middle_word()))
word.draw()
window.flip()
wait_trigger(2)
