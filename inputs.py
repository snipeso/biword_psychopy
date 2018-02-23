import sys
import time
import zmq
import re
from psychopy import event

class Input:
    def wait_triggers(self, trigger_count):
        "Waits a predefined number of triggers"
        trigger_timing = []
        while len(trigger_timing) < trigger_count:
            trigger_timing += event.waitKeys(keyList=["5", "escape"])
            if "escape" in trigger_timing:
                sys.exit(1)


class InputAuto(Input):
    def __init__(self, CONF, dataset):
        self.CONF = CONF
        self.dataset = dataset
    def wait_for_input(self):
        middle_word = self.dataset.middle_word()
        self.wait_triggers(self.CONF["trigger_timing"]["resting"])
        return "before" if self.CONF["target_word"] < middle_word else "after"


class InputNetwork(Input):
    def __init__(self, CONF):
        self.CONF = CONF
        zmq_context = zmq.Context()
        self.socket = zmq_context.socket(zmq.PULL)
        self.socket.bind("tcp://*:5555")

    def _get_classifier_input(self, block=False):
        "Checks for prediction from the classifier, can be blocking or nonblocking"
        try:
            return self.socket.recv(flags=zmq.NOBLOCK if not block else False)
            # return self.CONF["classifier_directions"][prediction]
        except zmq.Again:
            return None


    def wait_for_input(self):
        direction = None
        trigger_count = 0

        while not direction or trigger_count < self.CONF["trigger_timing"]["resting"]:
            # Checks keyboard input
            for thisKey in event.getKeys():
                if thisKey in self.CONF["keys"]["before"]:
                    direction = "before"
                elif thisKey in self.CONF["keys"]["after"]:
                    direction = "after"
                elif thisKey == "escape":
                    sys.exit(1)
                elif thisKey == "5":
                    trigger_count += 1

            # If no keyboard input, checks network input
            if not direction:
                prediction = self._get_classifier_input(block=False)
                if prediction:
                    prediction = float(prediction)
                    if abs(prediction) <= self.CONF['classifier']['acceptance_treshold']:
                        return 'prediction_below_treshold'
                    return 'before' if prediction < 0 else 'after'


            # waits 1/100 of a sec and checks again
            time.sleep(0.01)
        return direction


    # def wait_for_input_short(self):
    #     "Blocks on classifier input"
    #     return self._get_classifier_input(block=True)