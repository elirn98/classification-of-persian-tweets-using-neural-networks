import pickle
import re

from preprocessing import preprocessor
from preprocessing import constances
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model


class Predict():
    def __init__(self):

        self.preProcess = preprocessor.FormWords()
        self.constant = constances.ConstantVars()
        self.model7 = load_model('E:/pythonProjects/ThesisProject/LSTMClassifier7.h5')
        self.model9 = load_model('E:/pythonProjects/ThesisProject/LSTMClassifier9.h5')
        self.dic = {0: 'ورزشی', 1: 'اجتماعی', 2: 'سیاسی', 3: 'فرهنگی', 4: 'سلامت', 5: 'اقتصادی', 6: 'علمی و تکنولوژی', 7:'مذهبی', 8:'دانشگاهی'}

    def loadDictionary(self, name):
        with open('E:/pythonProjects/ThesisProject/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def cleanContent(self, raw):
        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags=re.UNICODE)
        cleanText = re.sub(r'((https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b)|(@[_A-Za-z0-9]+)', '', raw)
        cleanText = regrex_pattern.sub(r'', cleanText)
        return cleanText

    # a function for removing stopwords
    def Filter(self, strings, substr):
        filtered = []
        for string in strings:
            filter = [str for str in string if not any(sub == str for sub in substr)]
            filtered.append(filter)
        return filtered

    def predictClass(self, tweet, classNum):
        a = self.cleanContent(tweet)
        a = self.preProcess.normalize([a])
        b = self.preProcess.tokenize(a)
        c = self.preProcess.stemmWords(b)
        d = self.preProcess.lemmatizeWords(c)
        d = self.Filter(d, self.constant.punctuations() + ['\"', '\"', '!', '', '\n'] + self.constant.StopWords())
        word2idx = self.loadDictionary('LSTMdic'+classNum)
        if classNum == '7':
            current_idx = 21079
        elif classNum == '9':
            current_idx = 21724
        sequence = [[y for y in x] for x in d]
        i = -1
        for words in d:
            i += 1
            j = 0
            for word in words:
                if word in word2idx:
                    sequence[i][j] = float(word2idx[word])
                else:
                    sequence[i][j] = current_idx
                j += 1
        for i in range(len(sequence)):
            sequence[i] = np.array(sequence[i], dtype="float32")
        data = pad_sequences(sequence, maxlen=68)
        if classNum == '7':
            p = self.model7.predict(data).argmax(axis=1)
        else:
            p = self.model9.predict(data).argmax(axis=1)
        return self.dic[p[0]]