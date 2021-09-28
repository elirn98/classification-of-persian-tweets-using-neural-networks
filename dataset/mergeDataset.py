import pandas as pd
import random

from pandas import DataFrame
import csv


class datasetMerger:
    def __init__(self):
        pass

    def load(self):
        df = pd.read_csv("E:/pythonProjects/ThesisProject/dataset/tweets.csv", encoding='utf-8')
        return df

    def merge(self):
        dataset = self.load()
        # 16011), 16009
        randomIndexes = random.sample(range(2, 15317), 15315)
        df = DataFrame({'number': [], 'tweet': [], 'label': []})
        f = open("datasethash.csv", 'a', encoding="utf-8")
        csvWriter = csv.writer(f, delimiter=',')
        csvWriter.writerow(['number', 'tweet', 'label'])
        for randInt in randomIndexes:
            csvWriter.writerow(dataset.iloc[randInt])
        f.close()


def main():
    dm = datasetMerger()
    dm.merge()


if __name__ == '__main__':
    main()