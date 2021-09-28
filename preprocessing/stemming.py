import re
from os import path

data_path = path.join(path.dirname(__file__), 'data')
default_words = path.join(data_path, 'words.dat')


class Stemer:
    def __init__(self):
        self.ends = ('ات', 'ان', 'ترین', 'تر','مان','مون','تان','تون','شون','شان','ند','ید','یم', 'م', 'ت', 'ش', 'یی', 'ی', 'های', 'ها', 'ٔ', '‌ا', '‌')
        self.words = default_words

    def stem(self, word):
        # if len(word) == 0:
        for i in range(0, 2):
            for e in self.ends:
                if word.endswith(e) and len(word) > len(e) + 1:
                    word = word[:-len(e)]
        return word
