# * File contains methods to:
#       * read transcript file

from os.path import exists

# * read transcript file
def readTranscript(path_to_file):
    with open(path_to_file, "r") as f:
        text = f.read()
    return text

def findTranscript(path_to_audio):
    filePath = path_to_audio.split('.')
    fileName = filePath[0]
    fileName = fileName + ".txt"

    if not exists(fileName):
        fileName = ''
    return fileName
