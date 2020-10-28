from tika import parser
import re
from datetime import date, timedelta, datetime
import os
import pandas as pd
import matplotlib.pyplot as plt 

def mapDataForFile(file):
    raw = parser.from_file('data\{filename}'.format(filename=file))
    lastParagraph = raw['content'].replace('\n', '').rsplit('Δείγματα που έχουν ελεγχθεί')[-1]
    secondParagraph = raw['content'].replace('\n', '').split('Ο συνολικός αριθμός των κρουσμάτων ανέρχεται')[0].split('Τα νέα εργαστηριακά επιβεβαιωμένα κρούσματα')[1]
    lastParagraphsNumbers = re.findall(r'[0-9]+', lastParagraph, re.M|re.I)
    secondParagraphsNumbers = re.findall(r'[0-9]+', secondParagraph, re.M|re.I)
    cases = int(secondParagraphsNumbers[0])
    clinic = int(lastParagraphsNumbers[3])
    rapid = int(lastParagraphsNumbers[4])
    totalTestsPerformed = clinic + rapid
    date = file.split(".")[-2].split("-")[-1]
    return [date, cases, clinic, rapid, totalTestsPerformed, 0]

def getAndSaveDataOff():
    listOfFiles = os.listdir('./data/')
    dataset = list(map(mapDataForFile, listOfFiles))

    for i in range(len(dataset)-2, -1, -1):
        dataset[i+1][2] = dataset[i+1][2] - dataset[i][2]
        dataset[i+1][3] = dataset[i+1][3] - dataset[i][3]
        dataset[i+1][4] = dataset[i+1][4] - dataset[i][4]
        dataset[i+1][5] = dataset[i+1][1] / dataset[i+1][4]

    dataset.pop(0)

    import csv
    with open('dataset.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['date', 'newCases', 'newClinicTests', 'newRapidTests', 'totalNewTests', 'percentage'])
        for day in dataset:
            spamwriter.writerow(day)

getAndSaveDataOff()

def loadCsvDataSet():
    return pd.read_csv('dataset.csv')

dataset = loadCsvDataSet()

def showScatterPlot(dataset):
    dateSet = list(map(lambda item: datetime.strptime(str(item), '%Y%m%d'), dataset.date))

    figure, axYleft = plt.subplots()
    plt.figure(1, figsize=(12,7))
    color = 'tab:red'
    axYleft.set_xlabel('date')
    axYleft.set_ylabel('percentage of infected')
    axYleft.plot(dateSet, dataset.percentage, color=color)
    axYleft.tick_params(axis='y', labelcolor=color)

    axYright = axYleft.twinx()

    color = 'tab:blue'
    axYright.set_ylabel('new cases')
    axYright.plot(dateSet, dataset.newCases, color=color)
    axYright.tick_params(axis='y', labelcolor=color)
    figure.tight_layout()
    plt.title('Percentage of infected in Greece(new cases/total new tests) per day') 

    plt.figure(2, figsize=(12,7))
    plt.plot(dateSet, dataset.totalNewTests, color='tab:orange')
    plt.ylabel('total new cases')
    plt.xlabel('date')
    plt.title('Total new tests over time(daily)')
    # function to show the plot 
    plt.show()


showScatterPlot(dataset)