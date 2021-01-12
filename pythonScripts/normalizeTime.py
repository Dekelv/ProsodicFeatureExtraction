import pandas as pd
import math
import numpy as np

class disperseData:
    column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter',
                   'localabsoluteJitter', 'rapJitter',
                   'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                   'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                   'meanIntensity', 'maxIntensity', 'minIntensity']

    def __init__(self, filename, outputfileName):
        df = pd.read_csv(filename)
        columns = df.columns

        self.data = []

        for column in columns:
            self.data.append([])

        end_time = math.floor(df.to_dict()["endTime"][len(df.to_dict()["endTime"]) - 1])
        time = 0
        dfIndex = 0
        dfsize = len(df.to_dict().get("voiceID"))
        while time < end_time:
            time += 1
            if time > df.loc[dfIndex][2]:
                dfIndex += 1
            # calculates the data to be put in
            if(time > df.loc[dfIndex][1]):
                self.data[0].append(str(time - 1) + "-" + str(time))
                self.data[1].append(time - 1)
                self.data[2].append(time)
                avgTime = ((time - 1) + time) / 2
                self.data[3].append(avgTime)

                for variable in range(4, len(columns)):
                    ## finds the knn nearest indices
                    Val = df.loc[dfIndex][columns[variable]]
                    self.data[variable].append(Val)

        dfnew = pd.DataFrame(np.column_stack(self.data),
                             columns=self.column_list)  # add these lists to pandas in the right order
        # Write out the updated dataframe
        dfnew.to_csv(outputfileName, index=False)


