# ProsodicFeatureExtraction
To run full data set analysis:<br />
to run a full dataset provide a dataset directory containing subdirectories. Where each sub directory contains two audio files to be prosodically analysed.
python pythonScripts/runanalysis.py -dir \<datasetDirectory> -f1 \<nameOfFirstFile> -f2 \<nameOfSecondFile> -k \<k value>

To only extract file features:<br />
python pythonScripts/runanalysis.py -f1 \<nameOfFirstFile> 
  
To only run metrics analysis for 2 files:<br />
python pythonScripts/runanalysis.py -f1 \<nameOfFirstFile> -f2 \<nameOfSecondFile> -k \<k value>
