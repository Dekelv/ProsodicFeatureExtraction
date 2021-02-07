import matplotlib.pyplot as plt
import numpy as np

class plotsMaker:

    Data = []
    plot = plt.plot()


    def __init__(self):
        pass

    def giveData(self, data):
        self.Data.append(data)

    def setLabels(self, xLabel, yLabel, title):
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)

    def setLegend(self, labels):
        plt.legend(labels)

    def scatter(self,dataIndex, xAxis, yAxis, marker, color, shift):
        plt.scatter([x+shift for x in self.Data[dataIndex][xAxis][1:]], self.Data[dataIndex][yAxis][1:], marker=marker,color=color)

    def plot(self,dataIndex, xAxis, yAxis, marker, color, shift):
        plt.plot([x + shift for x in self.Data[dataIndex][xAxis][1:]], self.Data[dataIndex][yAxis][1:], marker=marker, color=color)

    def readDataFromFile(self,fileName, column_names):
        data = np.genfromtxt(fileName, delimiter=',', dtype=float, names=column_names)
        data = np.array(np.asarray(data.tolist())).transpose()
        self.Data.append(data)

    def show(self):
        plt.show()