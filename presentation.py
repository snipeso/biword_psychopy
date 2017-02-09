from psychopy import visual, core, event

class Screen:
    def __init__(self, CONF):
        self.CONF = CONF
        self.window = visual.Window(
            size=CONF["screen"]["size"],
            color=CONF["screen"]["color"],
            monitor=CONF["screen"]["monitor"],
            fullscr=False, units="norm")

        # Setup fixation cross
        self.fixation_cross = visual.TextStim(self.window, text="+")

        # Setup word and tasks
        self.word = visual.TextStim(self.window)
        self.task_before = visual.TextStim(self.window,
            text=CONF["tasks"]["instructions"]["before"],
            pos=[0-CONF["tasks"]["distance"], 0],
            height=CONF["tasks"]["height"])

        self.task_after = visual.TextStim(self.window,
            text=CONF["tasks"]["instructions"]["after"],
            pos=[CONF["tasks"]["distance"], 0],
            height=CONF["tasks"]["height"])

    def show_fixation_cross(self):
        self.fixation_cross.draw()
        self.window.flip()

    def show_planning(self, word):
        self.task_before.color = self.CONF["tasks"]["colors"]["planning"]
        self.task_before.draw()
        self.task_after.color = self.CONF["tasks"]["colors"]["planning"]
        self.task_after.draw()
        self.word.setText(word.upper())
        self.word.draw()
        self.window.flip()

    def show_thinking(self):
        self.task_before.color = self.CONF["tasks"]["colors"]["before"]
        self.task_before.draw()
        self.task_after.color = self.CONF["tasks"]["colors"]["after"]
        self.task_after.draw()
        self.word.draw()
        self.window.flip()

    def show_victory(self, word):
        self.word.setText(word.upper())
        self.word.draw()
        self.window.flip()
