import pandas as pd

def readCSVFile(fileName):

    column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter',
                   'localabsoluteJitter', 'rapJitter',
                   'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                   'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                   'meanIntensity', 'maxIntensity', 'minIntensity']
    data = []

    df = pd.read_csv(fileName)
    columns = df.columns
    for column in columns:
        data.append([])
    for i in range(len(df.index)):
        for variable in range(len(columns)):
            data[variable].append(df.loc[i][variable])

    return data
