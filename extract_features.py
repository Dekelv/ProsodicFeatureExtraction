import parselmouth

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set() # Use seaborn's default style to make attractive graphs

# Plot nice figures using Python's "standard" matplotlib library
snd = parselmouth.Sound("dataset/audioFiles/SegmentsLesson1/audioSeg-1.wav")
plt.figure()
plt.plot(snd.xs(), snd.values.T)
plt.xlim([snd.xmin, snd.xmax])
plt.xlabel("time [s]")
plt.ylabel("amplitude")
plt.show()

print("Amplitude")
print(snd.values.T)

pitch = snd.to_pitch()
pitch_values = pitch.selected_array['frequency']
pitch_values[pitch_values==0] = np.nan
plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
plt.grid(False)
plt.ylim(0, pitch.ceiling)
plt.ylabel("fundamental frequency [Hz]")
plt.show()
print("Pitch")
print(pitch_values)