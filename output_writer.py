import datetime
import json
import collections
import os
import csv

class Logger:
    def __init__(self, OUTPUT_FOLDER, CONF):
        "Initialize Logger"

        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        # Determines name for output fole
        OUTPUT_FILE_NAME = "{}_{}_{}_{}".format(
            CONF["participant"],
            CONF["name"],
            CONF["input_method"],
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
        self.path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE_NAME)

        # TODO: auto create output folder

        self.CONF = CONF
        self.save_conf()

        # Initialize container for data and writes header to CSV file
        self.data = collections.OrderedDict([
            ["sequence", None],
            ["word", None],
            ["direction", None],
            ["time_start_planning", None],
            ["time_start_thinking", None],
            ["time_answer", None],
        ])
        self.append_row(self.data.keys())

    def save_conf(self):
        "Writes CONF used for current run to a file, for future reference"
        with open("{}_conf.json".format(self.path), "w+") as f:
            f.write(json.dumps(self.CONF, indent=2))

    def append_row(self, data):
        "Writes a generic row to the csv file (could be data or HEADER)"
        with open("{}.csv".format(self.path), "a+") as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def append_data(self):
        "Writes accumulated data row to disk and clear the dictionary"
        self.append_row(self.data.values())
        for k in self.data:
            self.data[k] = None
