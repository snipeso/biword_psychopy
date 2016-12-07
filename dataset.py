class Dataset:
    def __init__(self, dataset_name, to_clean=True):
        self._load_dataset(dataset_name)
        if to_clean:
            self._clean_dataset()

    def _load_dataset(self, dataset_name):
        path = './datasets/{}'.format(dataset_name)
        with open(path, 'r') as f:
            self.dataset = f.read().split('\n')

    def _clean_dataset(self):
        self.dataset = list(filter(lambda word: "'" not in word, self.dataset))
        self.dataset = list(map(lambda word: word.lower(), self.dataset))
        self.dataset = list(set(self.dataset))
        self.dataset = sorted(self.dataset)

    def _middle_word_position(self):
        return int(len(self.dataset)/2)

    def middle_word(self):
        return self.dataset[self._middle_word_position()]

    def split_dataset(self, direction):
        if direction == "before":
            self.dataset = self.dataset[:self._middle_word_position()]
        else:
            self.dataset = self.dataset[self._middle_word_position():]

    def is_finished(self):
        return len(self.dataset) == 1
