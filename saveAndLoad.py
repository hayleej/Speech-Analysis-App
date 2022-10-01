# * File contains methods to:
#       * Save and Load the program analysis to file
#       * save segmentation to a file
#       ? save spectrogram

import pickle
from DisplayClass import Display
import implementCharsiu as ic


# * save segmentation to a file
def writeSeg(path_to_file, phonemeList, timeList):
    file = open(path_to_file, "w")
    i = 0
    stringthing = "{'phone': '" + str(phonemeList[i]) + "', 'start': " + str(
        timeList[i][0]) + ", 'stop': " + str(timeList[i][1])

    # write the first [
    file.write('[')
    # write first phoneme info
    file.write(stringthing)

    while i < len(phonemeList):
        file.write("}, ")
        stringthing = "{'phone': '" + str(phonemeList[i]) + "', 'start': " + str(
            timeList[i][0]) + ", 'stop': " + str(timeList[i][1])
        file.write(stringthing)

        i = i + 1
    file.write("}]")
    file.close()


# * save program to file
# * program file needs to contain:
#       * data, samplerate
#       * phonemeList, timeList
#       * transcript
def saveProgram(path_to_file, display):
    print("Saving Object to File...")
    try:
        with open(path_to_file, "wb") as f:
            pickle.dump(display.data, f)
            pickle.dump(display.samplerate, f)
            pickle.dump(display.endTime, f)
            pickle.dump(display.timeList, f)
            pickle.dump(display.phonemeList, f)
            pickle.dump(display.transcript, f)
    except:
        print("Error: problem pickling objects!")

# * save analysis to file
def saveAnalysis(path_to_file, analysis):
    print("Saving Analysis to File...")
    try:
        with open(path_to_file, "w") as f:
            if path_to_file.split('.')[-1] != 'json':
                f.write(analysis)
            else:
                jsonString = ic.convertToJson(analysis)
                f.write(jsonString)
    except:
        print("Error: problem writing analysis!")

# load program file
def loadProgram(path_to_file):
    try:
        with open(path_to_file, "rb") as f:
            display = Display()
            display.data = pickle.load(f)
            display.samplerate = pickle.load(f)
            display.endTime = pickle.load(f)
            display.timeList = pickle.load(f)
            display.phonemeList = pickle.load(f)
            display.transcript = pickle.load(f)
            return display
    except:
        print("Error: Object file does not exist!")


if __name__ == "__main__":
    testDisplay = Display('testData/SA1.wav','testData/SA1.txt')
    saveProgram('z.DAT', testDisplay)
