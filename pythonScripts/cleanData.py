import pandas as pd
import math
from pythonScripts import readCSVData
import numpy as np

class CleanData:
    column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter',
                   'localabsoluteJitter', 'rapJitter',
                   'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                   'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                   'meanIntensity', 'maxIntensity', 'minIntensity']


    def __init__(self, inputfile,  outputfileName):
        self.data = readCSVData.readCSVFile(inputfile)
        self.means = []
        self.SDs = []

        for variable in range(4, len(self.column_list)):
            self.means.append(sum(self.data[variable])/len(self.data[variable]))
            self.SDs.append(np.std(self.data[variable]))
        print("means")
        print(self.means)
        print("SDs")
        print(self.SDs)

        for variable in range(4, len(self.column_list)):
            for row in range(len(self.data[variable])):
                if self.data[variable][row] > self.means[variable-4] + 4 * self.SDs[variable-4] \
                    or self.data[variable][row] < self.means[variable-4] - 4 * self.SDs[variable-4]:
                    self.data[variable][row] = float("NaN")

        dfnew = pd.DataFrame(np.column_stack(self.data),
                             columns=self.column_list)  # add these lists to pandas in the right order
        # Write out the updated dataframe
        dfnew.to_csv(outputfileName, index=False)