# Measure pitch of all wav files in directory
import glob
import numpy as np
import pandas as pd
import parselmouth

from parselmouth.praat import call
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pydub import AudioSegment


# This is the function to measure voice pitch
def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID)  # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)  # create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit)  # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0, 0, unit)  # get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer = call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer = call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer


def runPCA(df):
    # Z-score the Jitter and Shimmer measurements
    features = ['localJitter', 'localabsoluteJitter', 'rapJitter', 'ppq5Jitter', 'ddpJitter',
                'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer', 'apq11Shimmer', 'ddaShimmer']
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    # y = df.loc[:,['target']].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)
    # PCA
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=principalComponents, columns=['JitterPCA', 'ShimmerPCA'])
    principalDf
    return principalDf


# create lists to put the results
file_list = []
mean_F0_list = []
sd_F0_list = []
hnr_list = []
localJitter_list = []
localabsoluteJitter_list = []
rapJitter_list = []
ppq5Jitter_list = []
ddpJitter_list = []
localShimmer_list = []
localdbShimmer_list = []
apq3Shimmer_list = []
aqpq5Shimmer_list = []
apq11Shimmer_list = []
ddaShimmer_list = []


##Extracts the features for a specific sound cut
def extractFeaturesForSoundSegment(sound):
    (meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer,
     localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = measurePitch(sound, 75, 500, "Hertz")
    file_list.append(wave_file)  # make an ID list
    mean_F0_list.append(meanF0)  # make a mean F0 list
    sd_F0_list.append(stdevF0)  # make a sd F0 list
    hnr_list.append(hnr)
    localJitter_list.append(localJitter)
    localabsoluteJitter_list.append(localabsoluteJitter)
    rapJitter_list.append(rapJitter)
    ppq5Jitter_list.append(ppq5Jitter)
    ddpJitter_list.append(ddpJitter)
    localShimmer_list.append(localShimmer)
    localdbShimmer_list.append(localdbShimmer)
    apq3Shimmer_list.append(apq3Shimmer)
    aqpq5Shimmer_list.append(aqpq5Shimmer)
    apq11Shimmer_list.append(apq11Shimmer)
    ddaShimmer_list.append(ddaShimmer)


## Once we figure out the times we can use this function to cut up the utterances without pauses to extract the features
def cutAudioIntoSoundSegment(audio, start_Time, End_Time):
    return parselmouth.Sound(audio).extract_part(from_time=start_Time, to_time=End_Time)


# Go through all the m4a files, convert to wav in the folder and measure pitch

# To get this to work, add an m4a file and update the file path.
# You may also need to install ffmpeg if you are experiencing problems.
audio = AudioSegment.from_file('dataset/audioFiles/m4aFiles/audio_only.m4a')
audio.export("dataset/audioFiles/m4aFiles/audio_only.wav", format="wav")
for wave_file in glob.glob("dataset/audioFiles/m4aFiles/audio_only.wav"):
    print(wave_file)
    sound = cutAudioIntoSoundSegment(wave_file, 0, 5)
    print(sound)
    extractFeaturesForSoundSegment(sound)

    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values == 0] = np.nan

    print(pitch_values)
    # Pitch mean
    print(pitch_values[~np.isnan(pitch_values)].mean())
    # Pitch Max
    print(pitch_values[~np.isnan(pitch_values)].max())
    # Pitch Min
    print(pitch_values[~np.isnan(pitch_values)].min())

    intensity = sound.to_intensity()
    print(intensity.values.T)
    # Mean Intensity
    print(intensity.values.T.mean())
    # Max Intensity
    print(intensity.values.T.max())
    # Min Intensity
    print(intensity.values.T.min())


df = pd.DataFrame(np.column_stack(
    [file_list, mean_F0_list, sd_F0_list, hnr_list, localJitter_list, localabsoluteJitter_list, rapJitter_list,
     ppq5Jitter_list, ddpJitter_list, localShimmer_list, localdbShimmer_list, apq3Shimmer_list, aqpq5Shimmer_list,
     apq11Shimmer_list, ddaShimmer_list]),
    columns=['voiceID', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter', 'localabsoluteJitter', 'rapJitter',
             'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
             'apq11Shimmer', 'ddaShimmer'])  # add these lists to pandas in the right order
# pcaData = runPCA(df)
# df = pd.concat([df, pcaData], axis=1)

# Write out the updated dataframe
df.to_csv("processed_results.csv", index=False)
