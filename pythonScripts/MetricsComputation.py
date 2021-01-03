import os
import csv
import pandas as pd
import math
import numpy as np

from pythonScripts.readCSVData import readCSVFile
class getMetrics:
    deltaValues = [-15,-10,-5,0,5,10,15]

    column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter',
                   'localabsoluteJitter', 'rapJitter',
                   'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                   'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                   'meanIntensity', 'maxIntensity', 'minIntensity']

    def __init__(self, participantfile, computerfile, resultfile):
        self.delta_corrs = []

        for delta in self.deltaValues:
            self.delta_corrs.append([])

        p_data = readCSVFile(participantfile)
        c_data = readCSVFile(computerfile)
        print("p_data shape: " + str(len(p_data[0])))
        print("c_data shape: " + str(len(c_data[0])))

        for deltaValue in range(len(self.deltaValues)):
            self.computeCorrelationsOnTheData(deltaValue, p_data, c_data)
        outputrows = [self.column_list[4:]] + self.delta_corrs
        outputcolumns = ["features"] + self.deltaValues
        df = pd.DataFrame(np.column_stack(outputrows),
                          columns=outputcolumns)  # add these lists to pandas in the right order
        # Write out the updated dataframe
        df.to_csv(resultfile, index=False)

    def computeCorrelationsOnTheData(self, deltaValue, p_data, c_data):
        rowCount = 0
        columnNumber = len(p_data) - 1
        # print("pdata len")
        # print(len(p_data[0]))
        # print("cdata len")
        # print(len(c_data[0]))
        # print("row counts")
        # for variable in range(4, columnNumber + 1):
        #     print("c_data")
        #     print(len(c_data[variable]))
        #     print("p_data")
        #     print(len(p_data[variable]))
        # print("end row counts")

        for variable in range(4,columnNumber + 1):
            meanC = 0
            meanP = 0
            while((len(p_data[columnNumber]) < len(c_data[columnNumber]) and rowCount < len(p_data[columnNumber])) or
                  (len(p_data[columnNumber]) > len(c_data[columnNumber]) and rowCount < len(c_data[columnNumber]))):
                rowCount += 1
                meanP += p_data[variable][rowCount-1]
                meanC += c_data[variable][rowCount-1]

            meanP = meanP / rowCount
            meanC = meanC / rowCount

            rowCount = 0
            sumNumerator = 0
            sumDenominatorP = 0
            sumDonominatorC = 0

            while ((len(p_data[columnNumber]) < len(c_data[columnNumber]) and rowCount < len(p_data[columnNumber])) or (
                    len(p_data[columnNumber]) > len(c_data[columnNumber]) and rowCount < len(
                    c_data[columnNumber]))):

                sumNumerator += (p_data[variable][rowCount + self.deltaValues[deltaValue]] - meanP) * (c_data[variable][rowCount] - meanC)
                sumDenominatorP += (p_data[variable][rowCount + self.deltaValues[deltaValue]] - meanP) * (p_data[variable][rowCount + self.deltaValues[deltaValue]] - meanP)
                sumDonominatorC += (c_data[variable][rowCount] - meanC) * (c_data[variable][rowCount] - meanC)
                rowCount += 1

            self.delta_corrs[deltaValue].append(sumNumerator / math.sqrt(sumDenominatorP * sumDonominatorC))





