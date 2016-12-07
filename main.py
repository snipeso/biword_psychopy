from psychopy import visual, core, event


DATASETS = {
    'american_english': './datasets/american-english',
}

def file_to_list(dataset_name):
    with open(DATASETS[dataset_name], 'r') as f:
        # Splits
        dataset = f.read().split('\n')

        # Removes words with apostrophes
        dataset = list(filter(lambda word: word.find("'") == -1, dataset))

        # Removes cases
        dataset = list(map(lambda word: word.lower(), dataset))
        # "set" makes this a collection of unique entries,
        # "list" makes it a list again, and "sorted" puts it in order
        dataset = sorted(list(set(dataset)))

    return dataset


def middle_word(dataset):
    middle = int(len(dataset) / 2)
    return dataset[middle], middle

def split_dataset(dataset, direction):
    assert direction in ["before", "after"], "Invalid direction"
    _, middle_pos = middle_word(dataset)

    if direction == "before":
        dataset = dataset[:middle_pos]
    else:
        dataset = dataset[middle_pos:]

    return dataset


mainWindow = visual.Window([800, 600], monitor="testMonitor", units="deg")
fixation = visual.TextStim(mainWindow, text="+", alignHoriz="center", alignVert="center")
word = visual.TextStim(mainWindow, alignHoriz="center", alignVert="center")


dataset = file_to_list("american_english")

while len(dataset) > 1:
    presented_word, _ = middle_word(dataset)
    word.setText(presented_word)
    word.draw()
    mainWindow.flip()

    allKeys=event.waitKeys()
    for thisKey in allKeys:
        if thisKey=="left":
            dataset = split_dataset(dataset, "before")
            break
        elif thisKey=="right":
            dataset = split_dataset(dataset, "after")
            break


print"Your word is:", dataset[0]
