import csv

import pandas as pd
from pandas import DataFrame


class DataSetLoader:
    def __init__(self):
        pass

    def load(self):
        df = pd.read_csv("E:/pythonProjects/ThesisProject/dataset/test.csv", encoding='utf-8')
        return df

    def faln(self):
        clusterNames = ['sport', 'social', 'politics', 'cultural', 'health', 'economy', 'scientific', 'religious',
                        'university']
        dataset = self.load()
        df = DataFrame({'number': [], 'tweet': [], 'label': []})
        f = open("testans.csv", 'a', encoding="utf-8")
        csvWriter = csv.writer(f, delimiter=',')
        csvWriter.writerow(['number', 'tweet', 'label'])
        dataset["label"].replace({"sport": "politics", "social": "cultural", "politics": "health", "cultural": "economy", "health": "scientific", "economy": "religious", "scientific": "university"}, inplace=True)
        for i in range(len(dataset)):
            csvWriter.writerow(dataset.iloc[i])
            # print(dataset.iloc[i])
            # if dataset.iloc[i]['label'] == clusterNames[0]:
            #     dataset.iloc[i]['label'] = clusterNames[2]
            #     print(dataset.iloc[i])
            #     csvWriter.writerow(dataset.iloc[i])
            # if dataset.iloc[i]['label'] == clusterNames[1]:
            #     dataset.iloc[i]['label'] = clusterNames[3]
            #     csvWriter.writerow(dataset.iloc[i])
            # if dataset.iloc[i]['label'] == clusterNames[2]:
            #     dataset.iloc[i]['label'] = clusterNames[4]
            #     csvWriter.writerow(dataset.iloc[i])
            # if dataset.iloc[i]['label'] == clusterNames[3]:
            #     dataset.iloc[i]['label'] = clusterNames[5]
            #     csvWriter.writerow(dataset.iloc[i])
            # if dataset.iloc[i]['label'] == clusterNames[4]:
            #     dataset.iloc[i]['label'] = clusterNames[6]
            #     csvWriter.writerow(dataset.iloc[i])
            # if dataset.iloc[i]['label'] == clusterNames[5]:
            #     dataset.iloc[i]['label'] = clusterNames[7]
            #     csvWriter.writerow(dataset.iloc[i])
            # if dataset.iloc[i]['label'] == clusterNames[6]:
            #     dataset.iloc[i]['label'] = clusterNames[8]
            #     csvWriter.writerow(dataset.iloc[i])
        f.close()
dl = DataSetLoader()
dl.faln()