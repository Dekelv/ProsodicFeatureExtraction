import pandas as pd
import numpy as np
from scipy import stats

exp_perception = pd.read_csv("Metrics/experiment_perception.csv")
exp_columns = exp_perception.columns

input = pd.read_csv("Metrics/TTest input data.csv")
input_columns = input.columns
# features

# variance
for feature in input_columns[10:len(input_columns)-1]:
    data1_M = input[(input['GENDER'] == 'Male') & (input['CONDITION'] == 1)][feature].values
    data2_M = input[(input['GENDER'] == 'Male') & (input['CONDITION'] == 2)][feature].values
    p_value_male = stats.levene(data1_M, data2_M)[1]
    if p_value_male < 0.05:
        print(feature + "Male. P value = " + str(p_value_male))

    data1_F = input[(input['GENDER'] == 'Female') & (input['CONDITION'] == 1)][feature].values
    data2_F = input[(input['GENDER'] == 'Female') & (input['CONDITION'] == 2)][feature].values
    p_value_female = stats.levene(data1_F, data2_F)[1]
    if p_value_female < 0.05:
        print(feature + "Female. P value = " + str(p_value_female))
print(input_columns)

