from psychopy import visual, core, event

from dataset import Dataset

mainWindow = visual.Window([800, 600], monitor="testMonitor", units="deg")
fixation = visual.TextStim(mainWindow, text="+", alignHoriz="center", alignVert="center")
word = visual.TextStim(mainWindow, alignHoriz="center", alignVert="center")

dataset = Dataset("american-english")

KEYS = {
    "before": ["1", "left", "-"],
    "after": ["2", "right", "+"]
}


while not dataset.is_finished():
    word.setText(dataset.middle_word())
    word.draw()
    mainWindow.flip()

    allKeys=event.waitKeys()
    for thisKey in allKeys:
        if thisKey in KEYS["before"]:
            dataset.split_dataset("before")
            break
        elif thisKey in KEYS["after"]:
            dataset.split_dataset("after")
            break


print "Your word is:", dataset.middle_word()
