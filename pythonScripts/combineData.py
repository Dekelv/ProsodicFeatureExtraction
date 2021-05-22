import pandas as pd

class combineData:
    def __init__(self, file1, file2,outputfile):
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        df3 = pd.merge(df1, df2, on="Experiment ID",how='inner')
        df3.to_csv(outputfile, index=False)
        print(df3)