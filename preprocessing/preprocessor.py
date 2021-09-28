from preprocessing.stemming import Stemer
from preprocessing.lemmatization import Lematizer
from preprocessing.tokenization import Tokenizer
from preprocessing.normalization import Normalizer
# from .sameWord import Samer
import numpy as np


class FormWords:
    def __init__(self):
        self.lemma = Lematizer()
        self.stem = Stemer()
        self.Normalizer = Normalizer()
        self.tokenizer = Tokenizer()
        # self.samer = Samer()

    def lemmatize(self, word):
        if word == '':
            return ''
        return self.lemma.lemmatize(word)

    def stemming(self, word):
        return self.stem.stem(word)

    def tokenize(self, sentences):
        tokenArray = []
        for sentence in sentences:
            tokenArray.append(self.tokenizer.word_tokenize(sentence))
        return tokenArray

    def normalize(self, sentences):
        normal = np.array([])
        for sentence in sentences:
            normal = np.append(normal, self.Normalizer.normaliz(sentence))
        return normal

    def stemmWords(self, words):
        stemmedTok = []
        #     i += 1
        for w in words:
            word = list(map(self.stemming, w))
            stemmedTok.append(word)
        return stemmedTok

    def lemmatizeWords(self, words):
        lemmatizedTok = []
        for w in words:
            word = list(map(self.lemmatize, w))
            lemmatizedTok.append(word)
        return lemmatizedTok

    # def uniform(self, tokens):
    #     token = map(self.samer.makeSame, tokens)
    #     return list(token)
