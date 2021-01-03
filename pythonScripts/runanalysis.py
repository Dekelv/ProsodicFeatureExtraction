import os

from pythonScripts.extract_features import Extract

dir = "experimentData"
experiments = os.listdir(dir)

for exp in experiments:
    if exp.__contains__("Human"):
        files = os.listdir(dir + "/" + "exp")
        Extract("Participant", "Participant_raw_features.csv")
        Extract("Computer", "Computer_raw_features.csv")

    if exp.__contains__("Furhat") or dir.__contains__("Robot"):
        files = os.listdir()
        pass
