class Dataset:
    "This class handles all of the datset manipulation."
    def __init__(self, dataset_name, to_clean=True):
        """
        When you create an instance of Dataset, this automatically loads the
        dataset, and unless you specify to_clean=False, it cleans the dataset.
        """
        self._load_dataset(dataset_name)
        if to_clean:
            self._clean_dataset()

    def _load_dataset(self, dataset_name):
        """
        This is used internally to load the dataset from the datsets folder,
        and makes the string into a list of words.
        """
        path = './datasets/{}'.format(dataset_name)
        with open(path, 'r') as f:
            self.dataset = f.read().split('\n')

    def _clean_dataset(self):
        """
        This is used internally to remove words with apostrophes, make uppercase
        words lowercase, and remove doubles. Happens automatically unless
        specified otherwise.
        """
        self.dataset = list(filter(lambda word: "'" not in word, self.dataset))
        self.dataset = list(map(lambda word: word.lower(), self.dataset))
        self.dataset = list(set(self.dataset))
        self.dataset = sorted(self.dataset)

    def _middle_word_position(self):
        "Internally used to get the position of the middle word."
        return int(len(self.dataset)/2)

    def middle_word(self):
        "Internally used to get the middle word of the dataset."
        return self.dataset[self._middle_word_position()]

    def split_dataset(self, direction):
        "Splits the dataset based on answer key."
        if direction == "before":
            self.dataset = self.dataset[:self._middle_word_position()]
        elif direction == "after":
            self.dataset = self.dataset[self._middle_word_position():]

    def is_finished(self):
        "Checks for the end of the process, when there is only 1 word left."
        return len(self.dataset) == 1
