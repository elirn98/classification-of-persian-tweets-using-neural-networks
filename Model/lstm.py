import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Dense, GlobalMaxPooling1D
from tensorflow.keras.layers import LSTM, Embedding
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
from dataset.loadDataset import DataSetLoader
from preprocessing.preprocessor import FormWords


class LSTMModel:
    def __init__(self):
        self.df = DataSetLoader.load()
        self.preProcess = FormWords()

    def buildLSTMModel(self):
        self.df['c_label'] = self.df['labels'].map(
            {'sport': 0, 'social': 1, 'politics': 2, 'cultural': 3, 'health': 4, 'economy': 5, 'scientific': 6})
        Y = self.df['c_label'].values
        xTrain, xTest, yTrain, yTest = train_test_split(self.df['tweet'], Y, test_size=0.33)
        xTrain = self.preProcess.normalize(xTrain)
        xTest = self.preProcess.normalize(xTest)
        train_sequence = self.preProcess.tokenize(xTrain)
        train_sequence = self.preProcess.stemmWords(train_sequence)
        train_sequence = self.preProcess.lemmatizeWords(train_sequence)
        test_sequence = self.preProcess.tokenize(xTest)
        test_sequence = self.preProcess.stemmWords(test_sequence)
        test_sequence = self.preProcess.lemmatizeWords(test_sequence)
        tokenizer = Tokenizer()
        word2idx = tokenizer.word_index
        V = len(word2idx)
        data_train = pad_sequences(train_sequence)
        data_test = pad_sequences(test_sequence)
        T = data_train.shape[1]
        D = 25
        M = 20
        i = Input(shape=(T,))
        x = Embedding(V + 1, D)(i)
        x = LSTM(M, return_sequences=True)(x)
        x = GlobalMaxPooling1D()(x)
        x = Dense(7, activation='relu')(x)
        model = Model(i, x)
        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        r = model.fit(data_train, yTrain, epoches=30, validation_data=(data_test, yTest))
        plt.plot(r.history['loss'], label='loss')
        plt.plot(r.history['val_loss'], label='val_loss')
        plt.legend()
        plt.plot(r.history['accuracy'], label='accuracy')
        plt.plot(r.history['val_accuracy'], label='val_accuracy')
        plt.legend()