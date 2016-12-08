import csv

def append_data(path, data):
    with open("{}.csv".format(path), "a+") as f:
        writer = csv.writer(f)
        writer.writerow(data)
