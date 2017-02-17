import json
import os
from psychopy import core
from dataset import Dataset
from presentation import Screen
from inputs import Input
from output_writer import Logger

# Summon Configurations
from configurations.final import CONF

# Initialize screen, logger and inputs
screen = Screen(CONF)
logger = Logger(OUTPUT_FOLDER='output', CONF=CONF)
inputs = Input(CONF)

# Summon dataset with optional cleaning
dataset = Dataset(CONF["dataset"]["name"], CONF["dataset"]["to_clean"])

# Presents simple fixation
screen.show_fixation_cross()
inputs.wait_triggers(1)

# starts clock for timestamping events
clock = core.Clock()

# waits for first n triggers with fixation, not counting the first
inputs.wait_triggers(CONF["trigger_timing"]["first_fixation"]-1)



# Main experiment loop
sequence_number = 0
while not dataset.is_finished():
    # Planning phase
    sequence_number += 1
    logger.data['sequence'] = sequence_number
    screen.show_planning(dataset.middle_word())
    logger.data['word'] = dataset.middle_word()
    logger.data['time_start_planning'] = clock.getTime()
    inputs.wait_triggers(CONF["trigger_timing"]["planning"])

    # Thinking phase
    screen.show_thinking()
    logger.data['time_start_thinking'] = clock.getTime()
    inputs.wait_triggers(CONF["trigger_timing"]["thinking"])

    # Resting period
    screen.show_fixation_cross()

    # Waits for answer to proceed to next word
    if CONF['input_method'] == 'manual':
        direction = inputs.wait_for_input_long()
    elif CONF['input_method'] == 'network_short':
        direction = inputs.wait_for_input_short()
    elif CONF['input_method'] == 'network_long':
        direction = inputs.wait_for_input_long()
    elif CONF['input_method'] == 'auto':
        direction = inputs.wait_for_input_auto(dataset.middle_word())


    logger.data['time_answer'] = clock.getTime()
    logger.data['direction'] = direction

    # Adds data to csv file
    logger.append_data()

    # splits dataset to start the next loop
    dataset.split_dataset(direction)

#shows final word for as long as the planning period
screen.show_victory("{}!".format(dataset.middle_word()))
inputs.wait_triggers(CONF["trigger_timing"]["planning"])

# Presents simple fixation until the end
screen.show_fixation_cross()
inputs.wait_triggers(CONF["trigger_timing"]["last_fixation"])
