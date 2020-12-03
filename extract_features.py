#mysp = __import__("my-voice-analysis")
import myprosody as mysp
import pickle

p = "audioSeg-"

#Insert your local directory address here to work with myprosody
c = "/home/dekel/Documents/myprosody/myprosody/dataset/audioFiles/"
import os

list = os.listdir(c) # dir is your directory path
number_files = len(list)

for i in range(number_files):
    mysp.mysptotal(p + str(i),c)
    mysp.myspf0mean(p + str(i),c)
    mysp.myspf0sd(p + str(i),c)
    mysp.myspf0med(p + str(i),c)
    mysp.myspf0min(p + str(i),c)
    mysp.myspf0max(p + str(i),c)
    mysp.myspf0q25(p + str(i),c)
    mysp.myspf0q75(p + str(i),c)