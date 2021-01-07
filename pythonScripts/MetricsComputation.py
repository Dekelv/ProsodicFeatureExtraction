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
        self.proximityConvergence = [[]]
        self.proximityConvergence.append([])
        for delta in self.deltaValues:
            self.delta_corrs.append([])

        p_data = readCSVFile(participantfile)
        c_data = readCSVFile(computerfile)
        ## compute correlations
        for deltaValue in range(len(self.deltaValues)):
            self.computeCorrelationsOnTheData(deltaValue, p_data, c_data)

        ## compute proximity
        for feature in range(4, len(self.column_list)):
            proxmity = self.determineProximity(p_data, c_data, feature)
            convergence = self.determineConvergence(p_data, c_data, proxmity, feature)
            self.proximityConvergence[0].append([proxmity])
            self.proximityConvergence[1].append([convergence])

        ## compute convergence


        outputrows = [self.column_list[4:]] + self.delta_corrs
        outputcolumns = ["features"] + self.deltaValues

        df = pd.DataFrame(np.column_stack(outputrows),
                          columns=outputcolumns)  # add these lists to pandas in the right order
        # Write out the updated dataframe
        df.to_csv(resultfile + "correlation.csv", index=False)

        outputrows2 = [self.column_list[4:]] + self.proximityConvergence
        outputcolumns2 = ["feature", "Proximity", "Convergence"]

        df2 = pd.DataFrame(np.column_stack(outputrows2),
                          columns=outputcolumns2)

        df2.to_csv(resultfile + "proximityConvergence.csv", index=False)

    def determineProximity(self, p_data, c_data, feature):
        size = 0
        if (len(p_data[1]) > len(c_data[1])):
            size = len(c_data[1])
        else:
            size = len(p_data[1])
        sum = 0

        for t in range(1,size):
            sum += abs(p_data[feature][t] - c_data[feature][t])
        return -sum / size

    def determineConvergence(self, p_data, c_data, proximity, feature):
        size = 0
        D_bar = -proximity
        if (len(p_data[1]) > len(p_data[1])):
            size = len(c_data[1])
        else:
            size = len(p_data[1])
        t_bar = size / 2
        sum_Numerator = 0
        sum_Denomerator_D = 0
        sum_Denomerator_t = 0
        for t in range(1,size):
            sum_Numerator += (-abs(p_data[feature][t] - c_data[feature][t]) - D_bar) * (t - t_bar)
            sum_Denomerator_D = (-abs(p_data[feature][t] - c_data[feature][t]))**2
            sum_Denomerator_t = (t - t_bar)**2
        convergence = sum_Numerator / (math.sqrt(sum_Denomerator_D * sum_Denomerator_t))
        return convergence



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

            while rowCount < len(p_data[variable]) and rowCount < len(c_data[variable]) and rowCount + self.deltaValues[deltaValue] < len(p_data[variable]) and rowCount + self.deltaValues[deltaValue] < len(
                    c_data[variable]):
                # print(rowCount)
                # print(self.deltaValues[deltaValue])
                # print(len(c_data[variable]))
                # print((rowCount + self.deltaValues[deltaValue]) < len(
                #     c_data[variable]))
                # print(len(p_data[variable])+ self.deltaValues[deltaValue])
                # print(len(c_data[variable])+ self.deltaValues[deltaValue])
                # print(rowCount + self.deltaValues[deltaValue])
                sumNumerator += (p_data[variable][rowCount + self.deltaValues[deltaValue]] - meanP) * (c_data[variable][rowCount] - meanC)
                sumDenominatorP += (p_data[variable][rowCount + self.deltaValues[deltaValue]] - meanP) * (p_data[variable][rowCount + self.deltaValues[deltaValue]] - meanP)
                sumDonominatorC += (c_data[variable][rowCount] - meanC) * (c_data[variable][rowCount] - meanC)
                rowCount += 1

            self.delta_corrs[deltaValue].append(sumNumerator / math.sqrt(sumDenominatorP * sumDonominatorC))





