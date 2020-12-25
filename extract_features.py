# Measure pitch of all wav files in directory
import glob
import numpy as np
import pandas as pd
import parselmouth

from parselmouth.praat import call
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pydub import AudioSegment

from pydub.silence import split_on_silence, detect_nonsilent


class Extract:
    # create lists to put the results
    interval_list = []
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
    mean_pitch = []
    max_pitch = []
    min_pitch = []
    mean_intensity = []
    max_intensity = []
    min_intensity = []

    def __init__(self, m4aFile):
        # Go through all the m4a files, convert to wav in the folder and measure pitch

        # To get this to work, add an m4a file and update the file path.
        # You may also need to install ffmpeg if you are experiencing problems.
        audio = AudioSegment.from_file(m4aFile + '.m4a')
        audio.export(m4aFile + ".wav", format="wav")
        self.non_silences = self.detect_nonsilences(m4aFile + ".wav")
        for wave_file in glob.glob(m4aFile + ".wav"):
            for interval in self.non_silences:
                try:
                    sound = self.cutAudioIntoSoundSegment(wave_file, interval[0], interval[1])
                    self.extractFeaturesForSoundSegment(sound, wave_file)
                    self.interval_list.append(str(interval[0]) + "_" + str(interval[1]))

                    pitch = sound.to_pitch()
                    pitch_values = pitch.selected_array['frequency']
                    pitch_values[pitch_values == 0] = np.nan

                    # Pitch mean
                    try:
                        self.mean_pitch.append(pitch_values[~np.isnan(pitch_values)].mean())
                    except Exception as e:
                        print(e)
                        print("An exception occurred: placing -1 as placeholder")
                        self.mean_pitch.append(-1)
                    # Pitch Max
                    try:
                        self.max_pitch.append(pitch_values[~np.isnan(pitch_values)].max())
                    except Exception as e:
                        print(e)
                        print("An exception occurred: placing -1 as placeholder")
                        self.max_pitch.append(-1)
                    # Pitch Min
                    try:
                        self.min_pitch.append(pitch_values[~np.isnan(pitch_values)].min())
                    except Exception as e:
                        print(e)
                        print("An exception occurred: placing -1 as placeholder")
                        self.min_pitch.append(-1)

                    # print("The intensities:")
                    try:
                        intensity = sound.to_intensity()
                        # Mean Intensity
                        try:
                            self.mean_intensity.append(intensity.values.T.mean())
                        except Exception as e:
                            print(e)
                            print("An exception occurred: placing -1 as placeholder")
                            self.mean_intensity.append(-1)
                        # Max Intensity
                        try:
                            self.max_intensity.append(intensity.values.T.max())
                        except Exception as e:
                            print(e)
                            print("An exception occurred: placing -1 as placeholder")
                            self.max_intensity.append(-1)
                        # Min Intensity
                        try:
                            self.min_intensity.append(intensity.values.T.min())
                        except Exception as e:
                            print(e)
                            print("An exception occurred: placing -1 as placeholder")
                            self.min_intensity.append(-1)
                    except Exception as e:
                        print(e)
                        print("could not extract intensities setting placeholders")
                        self.mean_intensity.append(-1)
                        self.max_intensity.append(-1)
                        self.min_intensity.append(-1)
                except Exception as e:
                    print(e)
                    print("could not extract pitch")


        lists = [self.interval_list, self.mean_F0_list, self.sd_F0_list, self.hnr_list, self.localJitter_list, self.localabsoluteJitter_list, self.rapJitter_list,
             self.ppq5Jitter_list, self.ddpJitter_list, self.localShimmer_list, self.localdbShimmer_list, self.apq3Shimmer_list,
             self.aqpq5Shimmer_list,
             self.apq11Shimmer_list, self.ddaShimmer_list, self.mean_pitch, self.max_pitch, self.min_pitch, self.mean_intensity, self.max_intensity, self.min_intensity]

        column_list = ['voiceID', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter', 'localabsoluteJitter', 'rapJitter',
                     'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                     'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                     'meanIntensity', 'maxIntensity', 'minIntensity']

        print("Extracted feature lists!!!")
        for i in range(len(lists)):
            print(column_list[i])
            print(lists[i])
            print(len(lists[i]))
        print("The columns")
        print(column_list)
        print(len(column_list))

        df = pd.DataFrame(np.column_stack(lists),
            columns=column_list)  # add these lists to pandas in the right order
        # pcaData = runPCA(df)
        # df = pd.concat([df, pcaData], axis=1)

        # Write out the updated dataframe
        df.to_csv("processed_results.csv", index=False)

    def detect_nonsilences(self, sound):
        snd = AudioSegment.from_wav(sound)
        dBFS = snd.dBFS
        non_silent = detect_nonsilent(snd, min_silence_len=1000, silence_thresh= dBFS - 16)
        #Convert to seconds
        non_silence = [((start / 1000), (stop / 1000)) for start, stop in non_silent]
        return non_silence

    def measurePitch(self, voiceID, f0min, f0max, unit):
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


    def runPCA(self, df):
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

    ##Extracts the features for a specific sound cut
    def extractFeaturesForSoundSegment(self, sound, wave_file):
        (meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer,
         localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = self.measurePitch(sound, 75, 500, "Hertz")
        self.mean_F0_list.append(meanF0)  # make a mean F0 list
        self.sd_F0_list.append(stdevF0)  # make a sd F0 list
        self.hnr_list.append(hnr)
        self.localJitter_list.append(localJitter)
        self.localabsoluteJitter_list.append(localabsoluteJitter)
        self.rapJitter_list.append(rapJitter)
        self.ppq5Jitter_list.append(ppq5Jitter)
        self.ddpJitter_list.append(ddpJitter)
        self.localShimmer_list.append(localShimmer)
        self.localdbShimmer_list.append(localdbShimmer)
        self.apq3Shimmer_list.append(apq3Shimmer)
        self.aqpq5Shimmer_list.append(aqpq5Shimmer)
        self.apq11Shimmer_list.append(apq11Shimmer)
        self.ddaShimmer_list.append(ddaShimmer)


    ## Once we figure out the times we can use this function to cut up the utterances without pauses to extract the features
    def cutAudioIntoSoundSegment(self, audio, start_Time, End_Time):
        return parselmouth.Sound(audio).extract_part(from_time=start_Time, to_time=End_Time)

    def knnRegression(self):
        pass

Extract("Participant")