import pandas as pd
import numpy as np
import math
import statistics
from DisplayClass import Display
import implementCharsiu as ic

# ARPABET has 31 C and 19 V
CONSONANTS = {"NG", "F", "M", "R", "N", "V", "HH", "Z", "K", "CH", "W",
              "ZH", "T", "Y", "B", "P", "TH", "DH", "G", "L", "JH", "SH", "D", "S"}
VOWELS = {"AE", "UW", "IY", "AW", "UH", "OW", "AA",
          "ER", "EY", "EH", "AH", "AO", "OY", "AY", "IH"}
OTHER = {"[SIL]", "[UNK]", "[PAD]"}
NOTINCLUDED = {"C": {"DX", "EL", "EM", "EN", "NX", "Q", "WH"},
               "V": {"AX", "AXR", "IX", "UX"}, "O": {}}


class Analysis():

    def __init__(self, dis):
        self.dis = dis
        self.correctPhones = self.dis.correctP[0]
        self.wordNum = self.getNumOfWords(self.dis.transcript)
        self.phones = self.dis.alignment
        self.alignment = self.alignUsingMidPoint()
        # gets phonemes and times as pandas data frame

        # if self.dis.transcript != '':
        #    self.phoneDF = ic.getPhonesDataFrame(dis.alignment[0])
        # else:
        self.phoneDF = ic.getPhonesDataFrame(dis.alignment)
        self.correctDF = ic.getPhonesDataFrame(self.correctPhones)

    def _getMidPointList(self):
        # get list in format [[correctP, [midpointmatches]],...]
        # actual and correct in format [start,end,phone]
        midPointList = []
        for target in self.correctPhones:
            # find phones that actual is between correct boundaries
            midPointMatches = []
            for actual in self.phones:
                mid = (actual[1] + actual[0]) / 2
                # ! look at whether it should be <=, >= or <, >
                if mid >= target[0] and mid < target[1]:
                    midPointMatches.append(actual[2])
            midPointList.append([target[2], midPointMatches])
        return midPointList

    def alignUsingMidPoint(self):
        midPointList = self._getMidPointList()
        alignment = []
        for matches in midPointList:
            if len(matches[1]) == 0:
                # if midpointmatches length = 0 then blank match
                alignment.append([matches[0], "  "])
            elif len(matches[1]) == 1:
                # if midpointmatches length = 1 then match
                alignment.append([matches[0], matches[1][0]])
            elif matches[0] in matches[1]:
                # if correctP in midpointmatches then match that one and have others empty matches
                for m in matches[1]:
                    if m == matches[0]:
                        alignment.append([matches[0], m])
                    else:
                        alignment.append(["  ", m])
            else:
                # if not in midpointmatches then match to first in list
                for m in matches[1]:
                    if m == matches[1][0]:
                        alignment.append([matches[0], m])
                    else:
                        alignment.append(["  ", m])
        return alignment

    def calcPercentCorrectWrapper(self):
        cc, cv, other = self._calcPercentCorrect(0, 0, 0, 0)
        consonantNum, vowelNum, otherNum = self._calcTotalInCorrect()
        PCC = (cc/consonantNum)*100
        PVC = (cv/vowelNum)*100
        PPC = ((cc+cv+other)/(consonantNum+vowelNum+otherNum))*100
        return PCC, PVC, PPC

    def _calcTotalInCorrect(self):
        consonantNum = 0
        vowelNum = 0
        otherNum = 0

        for phone in self.correctPhones:
            if phone[2] in CONSONANTS:
                consonantNum += 1
            elif phone[2] in VOWELS:
                vowelNum += 1
            elif phone[2] in OTHER and phone[2] != "  ":
                otherNum += 1

        return consonantNum, vowelNum, otherNum

    def _calcPercentCorrect(self, cur, cc, cv, other):
        if cur < len(self.alignment):
            if self.alignment[cur][1] in CONSONANTS:
                if self.alignment[cur][0] == self.alignment[cur][1]:
                    cc += 1
            elif self.alignment[cur][1] in VOWELS:
                if self.alignment[cur][0] == self.alignment[cur][1]:
                    cv += 1
            elif self.alignment[cur][1] in OTHER and self.alignment[cur][1] != "  ":
                if self.alignment[cur][0] == self.alignment[cur][1]:
                    other += 1
            cc, cv, other = self._calcPercentCorrect(cur+1, cc, cv, other)
        return cc, cv, other

    def getNumOfWords(self, transcript):
        words = transcript.split(' ')
        return len(words)

    def _calcPMLU(self):
        cc = self._calcPercentCorrect(0, 0, 0, 0)
        if len(self.phones) < len(self.correctPhones):
            points = len(self.phones)
        else:
            points = len(self.correctPhones)
        return (points + cc[0])/self.wordNum

    def _calcTargetPMLU(self):
        points = len(self.correctPhones)
        for r in self.correctPhones:
            if r[2] in CONSONANTS:
                points += 1
        return points/self.wordNum

    def _calcPWP(self):
        "Calculates the Proportion of Whole Word Proximity. Child's PMLU / Target PMLU"
        return self._calcPMLU()/self._calcTargetPMLU()

    def calcPMLUandPWP(self):
        'returns the child PMLU and PWP'
        PMLU = self._calcPMLU()
        PWP = self._calcPWP()
        return PMLU, PWP

    def _calcRMS(self, ar):
        squareArray = np.multiply(ar, ar)
        av = np.sum(squareArray)
        x = (1/len(ar)) * av
        rms = math.sqrt(x)
        return "{:.4f}".format(rms)

    def _getTranscriptString(self):
        transcript = "Transcript:\n\t" + self.dis.transcript + "\n\n"
        return str(transcript)

    def _getTimeSummaryString(self):
        timeSummary = "\tStart Time = " + str(self.dis.timeList[0][0]) + " seconds \n\tEnd Time = " + str(self.dis.endTime) + \
            " seconds \n\tTotal Duration = " + str(self.dis.endTime - self.dis.timeList[0][0]) + \
            " seconds \n\tSamplerate = " + str(self.dis.samplerate) + "\n\n"
        return str(timeSummary)

    def _getAmpSummaryString(self):
        amplitudeSummary = '\tMinimum Amplitude = ' + "{:.3f}".format(min(self.dis.data)) + ' dB \n\tMaximum Amplitude = ' + \
            "{:.3f}".format(max(self.dis.data)) + ' dB \n\tMean Amplitude = ' + "{:.7f}".format(statistics.mean(self.dis.data)) + \
            ' dB \n\tRMS Amplitude = ' + \
            self._calcRMS(self.dis.data) + ' dB \n\n'
        return str(amplitudeSummary)

    def _getFreqSummaryString(self):
        freqSummary = '\tMinimum Frequency = ' + \
            "{:.2f}".format(self.dis.specFreqs[0]) + ' Hz \n\tMaximum Frequency = ' + \
            "{:.2f}".format(self.dis.specFreqs[-1]) + ' Hz \n\n'
        return freqSummary

    def _getPhonemeSummaryString(self):
        phonemeSummary = 'Phonemes:\n' + self.phoneDF.to_string() + '\n\n'
        return str(phonemeSummary)

    def _getPhonemeSummaryString1(self):
        phonemeSummary = 'Phonemes:\n' + self.correctDF.to_string() + '\n\n'
        return str(phonemeSummary)

    def getSummaryText(self):
        summaryString = self._getTranscriptString()+'General:\n'+self._getTimeSummaryString() + \
            self._getAmpSummaryString() + self._getFreqSummaryString() + \
            self._getPhonemeSummaryString() + "Correct " + self._getPhonemeSummaryString1()
        return str(summaryString)

    def getAnalysisText(self):

        list1 = ''
        list2 = ''
        for r in self.alignment:
            list1 = list1 + str(r[0]) + ' '

        for r in self.alignment:
            list2 = list2 + r[1] + ' '

        PCC, PVC, PPC = self.calcPercentCorrectWrapper()
        PMLU, PWP = self.calcPMLUandPWP()

        analysisString = self._getTranscriptString() + 'Correct Phonemes:\t\t\t' + \
            list1 + '\nPhoneme List:\t\t\t' + list2 + '\n\n' + 'Speech Accuracy Scoring:' + '\n\tPCC = ' + "{:.2f}".format(PCC) + '\n\tPVC = ' + "{:.2f}".format(
                PVC) + '\n\tPPC = ' + "{:.2f}".format(PPC) + '\n\tPMLU = ' + "{:.2f}".format(PMLU) + '\n\tPWP = ' + "{:.2f}".format(PWP) + '\n\n'

        return str(analysisString)

    def _getAnalysisText(self):

        list1 = ''
        list2 = ''
        for r in self.phoneDF['phone']:
            list1 = list1 + str(r) + ' '

        for r in self.correctDF['phone']:
            list2 = list2 + r + ' '

        PCC, PVC, PPC = self.calcPercentCorrectWrapper()
        PMLU, PWP = self.calcPMLUandPWP()
        analysisString = self._getTranscriptString() + 'Phoneme List:\t\t' + \
            list1 + '\nCorrect Phonemes:\t' + list2 + '\n\n' + 'Speech Accuracy Scoring:' + '\n\tPCC = ' + \
            PCC + '\n\tPVC = ' + PVC + '\n\tPPC = ' + PPC + \
            '\n\tPMLU = ' + PMLU + '\n\tPWP = ' + PWP + '\n\n'

        return str(analysisString)

    def _getPowerString(self, isSelection, cursor):
        minCol = self.dis.getClosestIndex(cursor['startT'], self.dis.specTime)
        row = self.dis.getClosestIndex(cursor['freq'], self.dis.specFreqs)
        if isSelection:
            maxCol = self.dis.getClosestIndex(
                cursor['endT'], self.dis.specTime)
            minP = min(self.dis.spec[row][minCol:(maxCol+1)])
            maxP = max(self.dis.spec[row][minCol:(maxCol+1)])
            meanP = statistics.mean(self.dis.spec[row][minCol:(maxCol+1)])
            powerString = '\tMinimum Power: ' + "{:.2f}".format(minP) + ' dB/Hz (at time=' + "{:.2f}".format(self.dis.specTime[self.dis.spec[row] == minP]) + ')\n\tMaximum Power: ' + \
                "{:.2f}".format(maxP) + ' dB/Hz (at time=' + \
                "{:.2f}".format(self.dis.specTime[self.dis.spec[row] == maxP]) + \
                ')\n\tMean Power: ' + "{:.3f}".format(meanP) + ' dB/Hz\n'
        else:
            powerString = '\tPower: ' + \
                "{:.2f}".format(self.dis.spec[row][minCol]) + ' dB/Hz\n'
        return str(powerString)

    # todo Write getPhonemeAtTime()
    def getPhonemeAtTime(self, startTime, endTime=0):
        # Three cases for phones
        #   * 1. only one time (endTime=0)
        #   * 2. startTime and endTime are both between the same start and end boundary for one phone
        #   * 3. time selection crosses over multiple phones
        phones = []
        if endTime == 0:
            # find phone that startTime is between
            for index, cur in self.phoneDF.iterrows():
                if startTime >= cur['end']:
                    # time == current end, don't include current phone, include next phone that has time == start
                    # go to next row
                    continue
                elif startTime >= cur['start']:
                    # get phone
                    # time == start, include this phone
                    phones.append(cur['phone'])
                    break
                else:
                    # time < start
                    raise ValueError("Iterated too far?: Time at cursor is less than start time of row " +
                                     index + " of dataframe. But was greater than previous row's end time.")
        else:
            # selection if times
            for index, cur in self.phoneDF.iterrows():
                if startTime > cur['end']:
                    # next row
                    continue
                elif startTime >= cur['start']:
                    # get phone
                    phones.append(cur['phone'])
                    break

    def _getPhonesForSelection(self, startTime, endTime):
        phones = []
        for index, cur in self.phoneDF.iterrows():

            if startTime >= cur['end']:
                # have not found start phone
                # continue to next row
                continue
            elif endTime > cur['end']:
                # cur['start'] <= startTime
                # phone in selection time, not the last phone
                phones.append(cur['phone'])
                continue
            elif endTime == 0 or endTime > cur['start']:
                # cur['start'] < endTime <= cur['end']
                # last phone in selection
                phones.append(cur['phone'])
                break
            else:
                # (endTime != 0 and endTime <= cur['start']) or startTime < cur['start']:
                raise ValueError("Iterated too far?: start or end time of selection is less than start time of row " +
                                 index + " of dataframe. But was greater than previous row's end time.")
        return phones

    def _getPhonemeString(self, startTime, endTime=0):
        phonemeString = ''
        phones = self._getPhonesForSelection(startTime, endTime)
        for phone in phones:
            phonemeString += phone + ' '
        return str(phonemeString)

    def getAtCursorText(self, **cursor):
        '''cursor is a dictionary of: startT, endT and freq of the cursor when method is called. '''
        cursorText = 'At Cursor:\n\t'

        # dealing with ranges in x-pos (time)
        if 'endT' not in cursor.keys():
            cursorText += 'Time: ' + \
                str(cursor['startT']) + ' seconds\n\tAmplitude: ' + \
                "{:.3f}".format(self.dis.getAmplitude(cursor['startT'])) + ' dB\n\tFrequency: ' + \
                "{:.2f}".format(cursor['freq']) + ' Hz\n' + \
                self._getPowerString(False, cursor) + '\tPhoneme: ' + \
                self._getPhonemeString(cursor['startT']) + '\n\n'
        else:
            startIndex = int(cursor['startT'] * self.dis.samplerate - 1)
            endIndex = int(cursor['endT'] * self.dis.samplerate)

            cursorText += 'Start Time: ' + str(cursor['startT']) + ' seconds\n\t' + 'End Time: ' + str(cursor['endT']) + \
                ' seconds\n\t' + 'Minimum Amplitude = ' + "{:.3f}".format(min(self.dis.data[startIndex:endIndex])) + ' dB\n\t' + \
                '\n\tMaximum Amplitude = ' + "{:.3f}".format(max(self.dis.data[startIndex:endIndex])) + ' dB\n\t' + '\n\tMean Amplitude = ' + \
                "{:.7f}".format(statistics.mean(self.dis.data[startIndex:endIndex])) + ' dB\n\t' +  \
                '\n\tRMS Amplitude = ' + \
                self._calcRMS(self.dis.data[startIndex:endIndex]) + \
                ' dB\n\tFrequency: ' + str(cursor['freq']) + ' Hz\n' + \
                self._getPowerString(True, cursor) + '\tPhoneme: ' + \
                self._getPhonemeString(
                    cursor['startT'], cursor['endT']) + '\n\n'
        return str(cursorText)


if __name__ == "__main__":
    testDis = Display('testData/SA1.wav', 'testData/SA1.txt')
    testDis.graphDisplay()
    testAnalysis = Analysis(testDis)
    print(testAnalysis.getSummaryText())
    print(testAnalysis.getAnalysisText())
