import pandas as pd
from scipy import stats
import numpy as np
import math
class standardizeData:
    column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter',
                   'localabsoluteJitter', 'rapJitter',
                   'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                   'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                   'meanIntensity', 'maxIntensity', 'minIntensity']

    def __init__(self, filename, outputfileName):
        df = pd.read_csv(filename)
        columns = df.columns
        zscore = stats.zscore(df[columns[4:len(columns)]],nan_policy="omit")
        df2 = pd.DataFrame(zscore, columns= columns[4:len(columns)])
        frames = [df[columns[0:4]], df2]
        final = pd.concat(frames, axis=1)
        final.to_csv(outputfileName, index= False, na_rep=np.nan)
