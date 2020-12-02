import myprosody as mysp

p = "SegmentsLesson1/audioSeg-1"

#Insert your local directory address here to work with myprosody
c = ""


mysp.mysptotal(p,c)
mysp.myspf0mean(p,c)
mysp.myspf0sd(p,c)
mysp.myspf0med(p,c)
mysp.myspf0min(p,c)
mysp.myspf0max(p,c)
mysp.myspf0q25(p,c)
mysp.myspf0q75(p,c)