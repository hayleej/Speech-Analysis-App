
import fileIO
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import soundfile as sf
import implementCharsiu as ic
from blume.table import table
import textwrap as tw


class Display:
    'Class for display figure containing signal graph, spectrogram, and phoneme segmentation of analysis of audio'

    def __init__(self, audioFile='', path_to_transcript=''):

        self.data = []
        self.samplerate = 0
        self.endTime = 0
        self.timeList = []
        self.phonemeList = []
        self.transcript = ''

        gskw = {'hspace': 0, 'right': 0.95}
        self.fig, self.axs = plt.subplots(3, 1, squeeze=True, gridspec_kw=gskw)
        self.segLines = []

        # produced by spectrogram later in code
        self.spec = [[]]
        self.specFreqs = []
        self.specTime = []

        if audioFile != '':
            self.data, self.samplerate = sf.read(audioFile)
            self.endTime = len(self.data)/self.samplerate

            # using Charsui to get forced alignment
            self.alignment = ic.implementTextless(audioFile)
            self.phonemeList, self.timeList = ic.alignmentIntoLists(
                self.alignment)
            self.transcript = fileIO.readTranscript(path_to_transcript)
            self.correctP = ic.implementCharsiu(audioFile, path_to_transcript)

        else:
            for ax in self.axs:
                ax.get_xaxis().set_visible(False)
                ax.get_yaxis().set_visible(False)
                ax.set_xticks([])
                ax.set_xlabel('')

    def getAmplitude(self, time):
        # -1 due to indexing starting at 0
        index = int(time * self.samplerate) - 1
        return self.data[index]

    def getPower(self, time, freq):
        col = np.where(self.specTime == time)
        print(col[0])
        row = np.where(self.specFreqs == freq)
        print(row[0])
        print(self.specFreqs[100])
        return self.spec[row[0][0]][col[0][0]]

    def getSpecPower(self, time, freq):
        col = self.getClosestIndex(time, self.specTime)
        row = self.getClosestIndex(freq, self.specFreqs)
        return self.spec[row][col]

    def getClosestIndex(self, value, array):
        # lowerI is the lower index and upperI is the upper index of the two values the value is between
        lowerIRange = (np.nonzero(array <= value))[0]
        lowerI = lowerIRange[-1]
        upperIRange = (np.nonzero(array > value))[0]
        upperI = upperIRange[0]
        midI = (array[lowerI] + array[upperI])/2

        if midI <= value:
            index = upperI
        else:  # midI > value
            index = lowerI

        return index

    # * Calculates width of each column in table of phoneme segmentations
    def _getColWidths(self):
        widths = []
        index = 0
        for r in self.timeList:
            widths.insert(index, (r[1]-r[0])/self.endTime)
            index = index + 1

        return widths

    # * creates the lines for the segmentations on the graph
    def createSegLines(self):
        index = 0
        for r in self.timeList:
            cur1 = self.axs[1].axvline(r[0], 0, 1, c='red')
            cur2 = self.axs[1].axvline(r[1], 0, 1, c='red')
            self.segLines.insert(index, [cur1, cur2])
            index = index + 1

    def showSegLines(self):
        for line in self.segLines:
            line[0].set(linestyle='solid')
            line[1].set(linestyle='solid')

    def hideSegLines(self):
        for line in self.segLines:
            line[0].set(linestyle='none')
            line[1].set(linestyle='none')

    def hidePhonemeTable(self):
        self.fig.delaxes(self.axs[2])
        self.axs[1].get_xaxis().set_visible(True)
        self.axs[1].set_xticks(np.arange(0, self.endTime, 0.2))
        self.axs[1].set_xlabel('Time (seconds)')
        self.fig.canvas.draw_idle()

    def showPhonemeTable(self):
        self.fig.add_subplot(self.axs[2])
        self.axs[2].set_visible(True)
        self.axs[1].get_xaxis().set_visible(False)
        self.fig.canvas.draw_idle()

    def showTranscript(self):
        yscale = 0.5/self.phoneTable[0, 0].get_height()
        print(self.phoneTable[0, 0].get_height())
        print(yscale)
        self.phoneTable.scale(1, yscale)
        self.transcriptTable.set_visible(True)
        #self.transcriptTable.scale(1, yscale)
        self.fig.canvas.draw_idle()

    def hideTranscript(self):
        yscale = 1/self.phoneTable[0, 0].get_height()
        print(self.phoneTable[0, 0].get_height())
        print(yscale)
        self.phoneTable.scale(1, yscale)
        self.transcriptTable.set_visible(False)
        self.fig.canvas.draw_idle()

    # * display graph1 - signal graph
    def signalGraph(self, time):
        # signal graph
        self.axs[0].plot(time, self.data, linewidth=1)
        self.axs[0].get_xaxis().set_visible(False)
        self.axs[0].set_ylabel('Amplitude')
        self.axs[0].set_xbound(lower=0, upper=self.endTime)

    # * display graph2 - spectrogram
    def spectrogram(self):
        # spectrogram graph
        self.axs[1].get_xaxis().set_visible(False)
        self.axs[1].set_ylabel('Frequency (Hz)')
        self.spec, self.specFreqs, self.specTime, self.specIm = self.axs[1].specgram(
            self.data, Fs=self.samplerate, mode='psd', cmap='viridis', interpolation='gaussian', NFFT=160, pad_to=324)

        self.axs[1].set_xbound(lower=0, upper=self.endTime)

    def createSpacesForWrapping(self):
        pCellText = [[]]
        i = 0
        widths = self._getColWidths()
        for phone in self.phonemeList:
            if widths[i] < 0.017:
                pCellText[0].append(tw.fill(phone, width=1))
            elif widths[i] < 0.034:
                pCellText[0].append(tw.fill(phone, width=2))
            elif widths[i] < 0.051:
                pCellText[0].append(tw.fill(phone, width=3))
            else:
                pCellText[0].append(tw.fill(phone, width=5))
            i = i + 1
        return pCellText

    # * display graph3 - phoneme tables
    def phonemeTable(self):
        # phoneme table
        self.axs[2].set_xbound(upper=self.endTime)

        widths = self._getColWidths()

        pCellText = self.createSpacesForWrapping()

        # Phoneme Table
        self.phoneTable = table(self.axs[2], cellText=pCellText, cellLoc='center',
                                colWidths=widths, loc='upper left')
        self.phoneTable.AXESPAD = 0
        self.phoneTable.auto_set_font_size(False)
        self.phoneTable.set_fontsize("medium")

        cells = [key for key in self.phoneTable._cells]
        print(cells)
        for cell in cells:
            if self.phoneTable._cells[cell]._width < 0.017:
                self.phoneTable._cells[cell].set_text_props(
                    wrap=True, fontsize='small')

        self.axs[2].set_xticks(np.arange(0, self.endTime, 0.2))
        self.axs[2].set_xlabel('Time (seconds)')
        self.axs[2].set_yticks([])
        self.axs[2].get_yaxis().set_visible(False)
        self.axs[2].set_xbound(lower=0, upper=self.endTime)

    def createTranscriptTable(self):
        self.transcriptTable = table(self.axs[2], cellText=[
                                     [self.transcript]], cellLoc='center', colWidths=[1], loc='lower left')
        self.transcriptTable.AXESPAD = 0
        self.transcriptTable.auto_set_font_size(False)
        self.transcriptTable[0, 0].set_text_props(fontsize='x-large')
        self.transcriptTable.scale(1, 0.5/self.phoneTable[0, 0].get_height())
        self.showTranscript()

    # * The matplotlib display part

    def graphDisplay(self):

        time = np.arange(self.endTime, step=1/self.samplerate)

        self.signalGraph(time)

        self.spectrogram()

        self.phonemeTable()

        self.createTranscriptTable()

        self.createSegLines()


if __name__ == "__main__":
    testDisplay = Display('testData/SA1.wav', 'testData/SA1.txt')
    testDisplay.graphDisplay()
    plt.show()
    plt.close('all')
