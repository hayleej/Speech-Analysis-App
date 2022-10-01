
import pandas as pd
from charsiu.src.Charsiu import charsiu_forced_aligner
from charsiu.src.Charsiu import charsiu_predictive_aligner

# initialize forced aligner model
charsiuForced = charsiu_forced_aligner(aligner='charsiu/en_w2v2_fc_10ms')

# initialize predictive aligner model
charsiuPredictive = charsiu_predictive_aligner(aligner='charsiu/en_w2v2_fc_10ms')


def implementCharsiu(path_to_audio_file, path_to_txt_file):
    print(5)
    charsiuForced.aligner.eval()
    # read in text file
    with open(path_to_txt_file) as f:
        text = f.read()

    # perform forced alignment
    print(6)
    alignment = charsiuForced.align(audio=path_to_audio_file, text=text)
    print(7)
    return alignment


def implementTextless(path_to_audio_file):
    'perform textless alignment'

    # align
    alignment = charsiuPredictive.align(audio=path_to_audio_file)

    return alignment


def alignmentIntoLists(alignment):
    phonemeList = []  # make phonemeList empty
    timeList = []  # make timeList empty
    i = 0
    for r in alignment:
        phonemeList.insert(i, r[2])
        timeList.insert(i, [r[0], r[1]])
        i = i+1

    return phonemeList, timeList


def convertToJson(alignment):
    jsonText = []
    i = 0
    #print(alignment)
    for r in alignment:
        jsonText.insert(i, {"phone": r[2], "start": r[0], "end": r[1]})
        i = i+1
    return jsonText


def getPhonesDataFrame(alignment):
    jsonText = convertToJson(alignment)
    return pd.DataFrame(jsonText)


if __name__ == "__main__":
    print("Starting\n")
    phonemeList, timeList = alignmentIntoLists(implementCharsiu('testData/SA1.wav','testData/SA1.txt')[0])
    print(phonemeList)
