import os
import csv
import pandas as pd
import math
import numpy as np
import scipy

from pythonScripts.readCSVData import readCSVFile
import sys
class getMetrics:
    deltaValues = [-15,-10,-5,0,5,10,15]
    delayWindows = [-3,-2,-1,0,1,2,3]
    windowSize = 40
    shift = 20


    column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter',
                   'localabsoluteJitter', 'rapJitter',
                   'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                   'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                   'meanIntensity', 'maxIntensity', 'minIntensity']

    def __init__(self, expName, participantfile, computerfile, resultfile):
        self.delta_corrs = []
        self.delta_windowed_corrs = []
        self.proximityConvergence = [[]]
        self.proximityConvergence.append([])
        self.proximityConvergence.append([])
        self.nameColumn = [expName for x in range(len(self.column_list[4:]))]


        for delta in self.deltaValues:
            self.delta_corrs.append([])

        for delta in self.delayWindows:
            self.delta_windowed_corrs.append([])

        p_data = readCSVFile(participantfile)
        c_data = readCSVFile(computerfile)
        # ## compute correlations
        # for deltaValue in range(len(self.deltaValues)):
        #     self.computeCorrelationsOnTheData(deltaValue, p_data, c_data)

        # for deltaValue in range(len(self.delayWindows)):
        #     self.windowedCorrelation(deltaValue, p_data, c_data, self.windowSize, self.shift)

        ## compute proximity
        for feature in range(4, len(self.column_list)):
            proxmity = self.determineProximity(p_data, c_data, feature)
            convergence = self.determineConvergence(p_data, c_data, feature)
            self.proximityConvergence[0].append([proxmity])
            self.proximityConvergence[1].append([convergence[0]])
            self.proximityConvergence[2].append([convergence[1]])

        ## compute convergence


        # outputrows = [self.column_list[4:]] + self.delta_corrs
        # outputcolumns = ["features"] + self.deltaValues
        #
        # df = pd.DataFrame(np.column_stack(outputrows),
        #                   columns=outputcolumns)  # add these lists to pandas in the right order
        # # Write out the updated dataframe
        # df.to_csv(resultfile + "correlation.csv", index=False)

        outputrows2 = [self.nameColumn] + [self.column_list[4:]] + self.proximityConvergence
        outputcolumns2 = ["Experiment ID" , "feature", "Proximity", "Convergence", "convergence_pvalue"]
        df2 = pd.DataFrame(np.column_stack(outputrows2),
                          columns=outputcolumns2)

        df2.to_csv(resultfile + "proximityConvergence.csv", index=False)

        # outputrows3 = [self.column_list[4:]] + self.delta_windowed_corrs
        # outputcolumns3 = ["features"] + self.delayWindows
        #
        # df3 = pd.DataFrame(np.column_stack(outputrows3),
        #                   columns=outputcolumns3)  # add these lists to pandas in the right order
        # # Write out the updated dataframe
        # df3.to_csv(resultfile + "Windowedcorrelation.csv", index=False)

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

    def determineConvergence(self, p_data, c_data, feature):
        if (len(p_data[1]) > len(c_data[1])):
            size = len(c_data[1])
        else:
            size = len(p_data[1])
        return scipy.stats.pearsonr(p_data[feature][:size],c_data[feature][:size])

    def computeCorrelationsOnTheData(self, deltaValue, p_data, c_data):
        rowCount = 0
        columnNumber = len(p_data) - 1

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
                if(self.deltaValues[deltaValue] + rowCount < 0):
                    rowCount += 1
                    continue

                sumNumerator += (p_data[variable][rowCount + self.deltaValues[deltaValue]] - meanP) * (c_data[variable][rowCount] - meanC)
                sumDenominatorP += (p_data[variable][rowCount + self.deltaValues[deltaValue]] - meanP) * (p_data[variable][rowCount + self.deltaValues[deltaValue]] - meanP)
                sumDonominatorC += (c_data[variable][rowCount] - meanC) * (c_data[variable][rowCount] - meanC)
                rowCount += 1
            self.delta_corrs[deltaValue].append(sumNumerator / math.sqrt(sumDenominatorP * sumDonominatorC))

    def windowedCorrelation(self, deltaValue, p_data, c_data, windowSize, shift):
        rowCount = 0
        columnNumber = len(p_data) - 1

        for variable in range(4, columnNumber + 1):
            meanC = 0
            meanP = 0
            while ((len(p_data[columnNumber]) < len(c_data[columnNumber]) and rowCount < len(p_data[columnNumber])) or
                   (len(p_data[columnNumber]) > len(c_data[columnNumber]) and rowCount < len(c_data[columnNumber]))):
                rowCount += 1
                meanP += p_data[variable][rowCount - 1]
                meanC += c_data[variable][rowCount - 1]

            meanP = meanP / rowCount
            meanC = meanC / rowCount

            rowCount = 0
            sumNumerator = 0
            sumDenominatorP = 0
            sumDonominatorC = 0

            while rowCount + windowSize < len(p_data[variable]) and rowCount + windowSize < len(c_data[variable]) and rowCount + self.delayWindows[deltaValue] * windowSize \
                    < len(p_data[variable]) and rowCount + windowSize * self.delayWindows[deltaValue] < len(
                    c_data[variable]):
                if(rowCount + (windowSize * self.delayWindows[deltaValue]) < 0):
                    rowCount += shift
                    continue

                windowValueC = 0
                windowValueP = 0

                for r in range(rowCount + (windowSize * self.delayWindows[deltaValue]), rowCount + windowSize + (windowSize * self.delayWindows[deltaValue])):
                    windowValueP += p_data[variable][r]
                windowValueP = windowValueP/windowSize

                for r in range(rowCount, rowCount + windowSize):
                    windowValueC += c_data[variable][r]
                windowValueC = windowValueC/windowSize

                sumNumerator += (windowValueP - meanP) * (
                            windowValueC - meanC)
                sumDenominatorP += windowValueP**2
                sumDonominatorC += windowValueC**2
                rowCount += shift
            self.delta_windowed_corrs[deltaValue].append(sumNumerator / math.sqrt(sumDenominatorP * sumDonominatorC))



