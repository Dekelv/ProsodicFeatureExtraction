import myprosody as mp
from pydub import AudioSegment
p = ""
c = "SegmentsLesson1"
windowLength = 20000
currentWindow = 0
Audio = AudioSegment.from_wav("SSP frikandel Saar.wav")

cnt = 0
while currentWindow <= len(Audio):
    newAudio = Audio[currentWindow:currentWindow + windowLength]
    currentWindow += windowLength
    newAudio.export("dataset" + "/" + "audioFiles" + "/" + c + "/audioSeg-" + str(cnt) + ".wav", format="wav")
    cnt+=1

#mp.myprosody(newAudio)
#newAudio.export('newSong.wav', format="wav")