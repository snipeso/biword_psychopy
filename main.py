import json
import logging
import os
from psychopy import core
from dataset import Dataset
from presentation import Screen
import inputs as input_modules
from output_writer import Logger

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s-%(levelname)s-%(message)s',
)


# Summon Configurations
from configurations.final import CONF
logging.info('Configuration loaded')

# Summon dataset with optional cleaning
dataset = Dataset(CONF["dataset"]["name"], CONF["dataset"]["to_clean"])
logging.info('Dataset loaded')

# Initialize screen, logger and inputs
screen = Screen(CONF)
logger = Logger(OUTPUT_FOLDER='output', CONF=CONF)
if CONF['input_method'] in ['manual', 'network_long']:
    inputs = input_modules.InputNetwork(CONF)
elif CONF['input_method'] == 'auto':
    inputs = input_modules.InputAuto(CONF, dataset)

logging.info('Initialization completed')


# Presents simple fixation
screen.show_fixation_cross()
logging.info('Waiting for first trigger')
inputs.wait_triggers(1)

# starts clock for timestamping events
clock = core.Clock()
logging.info('Starting experiment clock')

# waits for first n triggers with fixation, not counting the first
inputs.wait_triggers(CONF["trigger_timing"]["first_fixation"]-1)


# Main experiment loop
sequence_number = 0
while not dataset.is_finished():
    # Planning phase
    sequence_number += 1
    logging.info('Starting iteration #%s', sequence_number)
    logging.info('Starting planning phase')
    logger.data['sequence'] = sequence_number
    screen.show_planning(dataset.middle_word())
    logger.data['word'] = dataset.middle_word()
    logger.data['time_start_planning'] = clock.getTime()
    inputs.wait_triggers(CONF["trigger_timing"]["planning"])

    # Thinking phase
    logging.info('Starting thinking phase')
    screen.show_thinking()
    logger.data['time_start_thinking'] = clock.getTime()
    inputs.wait_triggers(CONF["trigger_timing"]["thinking"])

    # Resting period
    logging.info('Starting resting period')
    screen.show_fixation_cross()

    # Waits for answer to proceed to next word
    direction = inputs.wait_for_input()
    logging.info('A direction was obtained via %s : %s', CONF['input_method'], direction)


    logger.data['time_answer'] = clock.getTime()
    logger.data['direction'] = direction

    # Adds data to csv file
    logger.append_data()

    # splits dataset to start the next loop
    dataset.split_dataset(direction)

logging.info('Dictionary had len==1, iterations are ended')
logging.info('Showing the final word: %s', dataset.middle_word())
#shows final word for as long as the planning period
screen.show_victory("{}!".format(dataset.middle_word()))
inputs.wait_triggers(CONF["trigger_timing"]["planning"])

# Presents simple fixation until the end
logging.info('Showing fixation cross')
screen.show_fixation_cross()
inputs.wait_triggers(CONF["trigger_timing"]["last_fixation"])

logging.info('Quitting')
