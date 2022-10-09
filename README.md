# Speech-Analysis-App

## Table of Contents
- [Usage](README.md#Usage)
- [Features](README.md#Features)
- [Acknowledgements](README.md#Acknowledgements)
- [References](README.md#References)

## Usage

1. Download the program using the command 
```
$ git clone https://github.com/hayleej/Speech-Analysis-App/
```

2. Move to the project directory
```
$ cd Speech-Analysis-App/
```

3. Install requirements
```
$ pip3 install -r requirements.txt
```

4. Run the program
```
$ python3 UserInterface.py
```

The program will then run and can be used.  
**Note:** The program make take a while to load.

## Features
- Displays Signal Graph of audio
- Displays Spectrogram of audio
  - Lines on Spectrogram to show phoneme segmentation
- Phoneme Segmentation
- Transcript of Audio
- Hide and Show different displays
- Compare produced phonemes with the target phonemes
- Calculate Speech Sound Accuracy Scores to determine severity
  - Percentage of Consonants Correct (PCC)
  - Percentage of Vowels Correct (PVC)
  - Percentage of Phonemes Correct (PPC)
  - Phonological Mean Length of Utterance (PMLU)
  - Proportion of Whole Word Proximity (PWP)
- Save data to be loaded back up later
- Save analyis to a text file
- Save display as an image

## Acknowledgements
[Charsiu](https://github.com/lingjzhu/charsiu/) is used in the program for the forced alignment and phoneme segmentation of audio. It has been modified slightly for smoother connection to the rest of the program but everything contained in the [charsiu directory](charsiu/) is the work of Jian Zhu and Cong Zhang.

## References
[Charsiu](https://github.com/lingjzhu/charsiu/)
