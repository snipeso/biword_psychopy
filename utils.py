import csv
from psychopy import event

def append_data(path, data):
    with open("{}.csv".format(path), "a+") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def wait_trigger(trigger_count):
    trigger_timing = []
    while len(trigger_timing) < trigger_count:
        trigger_timing += event.waitKeys(keyList=["5"])
