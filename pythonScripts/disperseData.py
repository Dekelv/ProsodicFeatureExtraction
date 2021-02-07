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
        startTime = int(df.loc[0][1])
        time = int(df.loc[0][1])
        print(time)
        dfIndex = 0
        dfsize = len(df.to_dict().get("voiceID"))
        while time < end_time:
            if time > df.loc[dfIndex][2]:
                dfIndex += 1
            # calculates the data to be put in
            if(time > df.loc[dfIndex][1]):
                self.data[0].append(str(time) + "-" + str(time + 1))
                self.data[1].append(time)
                self.data[2].append(time + 1)
                avgTime = time+0.005
                self.data[3].append(avgTime)

                for variable in range(4, len(columns)):
                    ## finds the knn nearest indices
                    Val = df.loc[dfIndex][columns[variable]]
                    self.data[variable].append(Val)

            if(time<df.loc[dfIndex][1]):
                self.data[0].append(str(time) + "-" + str(time + 1))
                self.data[1].append(time)
                self.data[2].append(time + 1)
                self.data[3].append(time+0.005)
                for variable in range(4, len(columns)):
                    ## finds the knn nearest indices
                    self.data[variable].append(float('nan'))

            time += 0.01

        dfnew = pd.DataFrame(np.column_stack(self.data),
                             columns=self.column_list)  # add these lists to pandas in the right order
        # Write out the updated dataframe
        dfnew.to_csv(outputfileName, index=False)


