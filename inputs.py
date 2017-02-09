import sys
import time
import zmq
from psychopy import event


class Input:
    def __init__(self, CONF):
        self.CONF = CONF
        zmq_context = zmq.Context()
        self.socket = zmq_context.socket(zmq.PULL)
        self.socket.bind("tcp://*:5555")

    def _get_classifier_input(self, block=False):
        "Helper method, can be blocking or nonblocking"
        try:
            datapoint = self.socket.recv(flags=zmq.NOBLOCK if not block else False)
            return "before" if float(datapoint) < 0 else "after"
        except zmq.Again:
            return None

    def wait_for_input_short(self):
        "Blocks on classifier input"
        return self._get_classifier_input(block=True)

    def wait_for_input_long(self):
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
                direction = self._get_classifier_input(block=False)

            # waits 1/10 of a sec and checks again
            time.sleep(0.1)
        return direction

    def wait_triggers(self, trigger_count):
        "Waits a predefined number of triggers"
        trigger_timing = []
        while len(trigger_timing) < trigger_count:
            trigger_timing += event.waitKeys(keyList=["5"])
