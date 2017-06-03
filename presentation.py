from psychopy import visual, core, event

class Screen:
    def __init__(self, CONF):
        self.CONF = CONF
        self.window = visual.Window(
            size=CONF["screen"]["size"],
            color=CONF["screen"]["color"],
            monitor=CONF["screen"]["monitor"],
            fullscr=True, units="norm")

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

        self._create_alphabet()


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
        self._show_alphabet()
        self.window.flip()

    def show_thinking(self):
        self.task_before.color = self.CONF["tasks"]["colors"]["before"]
        self.task_before.draw()
        self.task_after.color = self.CONF["tasks"]["colors"]["after"]
        self.task_after.draw()
        self.word.draw()
        self._show_alphabet()
        self.window.flip()

    def show_victory(self, word):
        self.word.setText(word.upper())
        self.word.draw()
        self.window.flip()

    def _create_alphabet(self):
        self.alphabet = []
        spacing = self.CONF["alphabet"]["length"]*2/(len(self.CONF["alphabet"]["letters"])-1)
        for i, letter in enumerate(self.CONF["alphabet"]["letters"]):
            self.alphabet.append(
                visual.TextStim(self.window,
                    text=letter,
                    pos=[
                        0-self.CONF["alphabet"]["length"]+spacing*i,
                        self.CONF["alphabet"]["y_position"]
                    ],
                    height=self.CONF["alphabet"]["height"])
            )
            #
            # #setup alphabet
            # self.alphabet = visual.TextStim(self.window,
            #     text=(" "*CONF["alphabet"]["spacing"]).join(CONF["alphabet"]["letters"]),
            #     pos=[0, CONF["alphabet"]["distance"]],
            #     height=CONF["alphabet"]["height"])            letter.draw()

    def _show_alphabet(self):
        for letter in self.alphabet:
            letter.draw()
