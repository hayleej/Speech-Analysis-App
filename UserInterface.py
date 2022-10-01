
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from DisplayClass import Display

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import saveAndLoad
import fileIO
from Analysis import Analysis


class UIWindow:
    'Class for User Interface Window of program'

    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.parent = parent  # TODO don't know if i need this
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.mainframe = ttk.Frame(self.window, padding="2m")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        #self.createMenuBar()

        self.savedFilePath = None

        self.parent.withdraw()

    def createMenuBar(self):
        windowSystem = rt.tk.call('tk', 'windowingsystem')
        # creating menus below
        if windowSystem == 'x11':
            self.createX11MenuBar()
        elif windowSystem == 'win32':
            self.createWindowsMenuBar()
        elif windowSystem == 'aqua':
            self.createMacOSMenuBar()
        else:
            raise ValueError('window system is none of the correct types')
        
    def createX11MenuBar(self):
        pass

    def createWindowsMenuBar(self):
        pass

    def createMacOSMenuBar(self):

        self.parent.option_add('*tearOff', FALSE)
        # creating menubar
        self.menubar = Menu(self.window)

        # adding application menu
        appmenu = Menu(self.menubar, name='apple')
        self.menubar.add_cascade(menu=appmenu)
        appmenu.add_command(label='About My Application')
        appmenu.add_separator()

        # file menu
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')

        self.menu_file.add_command(label='New', command=self.newFile)

        self.menu_file.add_separator()

        self.menu_file.add_command(label='Open...', command=self.openFile)

        # recent files menu
        '''
        menu_recent = Menu(self.menu_file)
        self.menu_file.add_cascade(menu=menu_recent, label='Open Recent')
        for f in recent_files:
            menu_recent.add_command(label=os.path.basename(
                f), command=lambda f=f: self.openFile(f))
        '''
        #? could have the list of recent files saved in a folder (local or something?) that gets loaded up everytime the app is run
        self.menu_file.add_separator()

        self.menu_file.add_command(label='Save', command=self.save)
        self.menu_file.add_command(label='Save As...', command=self.saveAs)

        self.menu_file.add_separator()
        self.menu_file.add_command(label='Close', command=self.closeFile)
        self.menu_file.add_separator()

        # edit menu
        self.menu_edit = Menu(self.menubar)

        self.menubar.add_cascade(menu=self.menu_edit, label='Edit')
        self.menu_edit.add_command(
            label="Undo", command=lambda: self.parent.focus_get().event_generate("<<Undo>>"))
        self.menu_edit.entryconfigure('Undo', accelerator='Command+Z')
        self.menu_edit.add_command(
            label="Redo", command=lambda: self.parent.focus_get().event_generate("<<Redo>>"))
        self.menu_edit.entryconfigure('Redo', accelerator='Shift+Command+Z')
        self.menu_edit.add_separator()
        self.menu_edit.add_command(
            label="Copy", command=lambda: self.parent.focus_get().event_generate("<<Copy>>"))
        self.menu_edit.entryconfigure('Copy', accelerator='Command+C')
        self.menu_edit.add_command(
            label="Paste", command=lambda: self.parent.focus_get().event_generate("<<Paste>>"))
        self.menu_edit.entryconfigure('Paste', accelerator='Command+V')
        self.menu_edit.add_command(
            label="Cut", command=lambda: self.parent.focus_get().event_generate("<<Cut>>"))
        self.menu_edit.entryconfigure('Cut', accelerator='Command+X')
        self.menu_edit.add_command(
            label="Clear", command=lambda: self.parent.focus_get().event_generate("<<Clear>>"))

        # View menu
        self.menu_view = Menu(self.menubar)

        self.menubar.add_cascade(menu=self.menu_view, label='View')
        self.menu_view.add_command(label="Zoom...", command=self.zoom)
        self.menu_view.add_command(label="Zoom In", command=self.zoomIn)
        self.menu_view.add_command(label="Zoom Out", command=self.zoomOut)
        self.menu_view.add_command(label="Zoom to Selection",
                                   command=self.zoomToSelection)
        self.menu_view.add_command(label="Zoom Back", command=self.zoomBack)

        # Analyse menu
        self.menu_analyse = Menu(self.menubar)

        self.menubar.add_cascade(menu=self.menu_analyse, label='Analyse')
        self.menu_analyse.add_command(
            label="Open Analysis Window", command=self.openAnalysisWindow)
        self.menu_analyse.add_separator()
        self.menu_analyse.add_command(
            label="Editor Info", command=self.editorInfo)
        self.menu_analyse.add_command(
            label="Sound Info", command=self.soundInfo)
        self.menu_analyse.add_separator()
        self.menu_analyse.add_command(
            label="Get Summary", command=self.getSummary)
        self.menu_analyse.add_command(
            label="Get Phoneme Analysis", command=self.getPhonemeAnalysis)
        self.menu_analyse.add_command(
            label="Get At Cursor Analysis", command=self.getCursorAnalysis)

        # adding window menu
        self.windowmenu = Menu(self.menubar, name='window')
        self.menubar.add_cascade(menu=self.windowmenu, label='Window')

        # adding help menu
        self.helpmenu = Menu(self.menubar, name='help')
        self.menubar.add_cascade(menu=self.helpmenu, label='Help')
        self.parent.createcommand('tk::mac::ShowHelp', self.showHelp)
        self.parent.createcommand(
            'tk::mac::ShowPreferences', self.showMyPreferencesDialog)

        # attach menubar to window
        self.window['menu'] = self.menubar

    def showMyPreferencesDialog(self):
        pass

    def showHelp(self):
        pass

    #! below are temporary definitions for all the menu commands
    def newFile(self):
        dw = DisplayWindow(rt, '', emptyDisplay)

    def openFile(self):
        path_to_file = self._openFileScreen()
        if type(self) is not DisplayWindow:
            if len(path_to_file) != 0:
                dw = DisplayWindow(rt, path_to_file, emptyDisplay)
                dw._loadPlots(path_to_file)

    def save(self):
        # implemented in child classes
        pass

    def saveAs(self):
        # implemented in child classes
        pass
        

    def closeFile(self):
        #? need to do binding to exit button
        #? if only window that exists is closed then close app
        pass

    def zoom(self):
        pass

    def zoomIn(self):
        pass

    def zoomOut(self):
        pass

    def zoomToSelection(self):
        pass

    def zoomBack(self):
        pass

    def openAnalysisWindow(self):
        pass

    def editorInfo(self):
        pass

    def soundInfo(self):
        pass

    def getSummary(self):
        pass

    def getPhonemeAnalysis(self):
        pass

    def getCursorAnalysis(self):
        pass

    def _openFileScreen(self):
        path_to_file = filedialog.askopenfilename(filetypes=(
            ("Analysis file", "*.DAT"), ("Sound File", "*.wav")), title="Select File")
        return path_to_file


class DisplayWindow(UIWindow):
    def __init__(self, parent, path_to_file, dis):
        super().__init__(parent)
        self.analysisW = None
        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
        filePath = path_to_file.split('/')
        self.fileName = filePath[-1]

        self.window.title(self.fileName + " Display")

        self.dis = dis

        # frame adjustments
        self.mainframe.rowconfigure(2, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.columnconfigure(3, weight=1)
        self.mainframe.columnconfigure(4, weight=1)

        # checkbutton variables
        self.segBool = BooleanVar(value=True)
        self.transcriptBool = BooleanVar(value=True)
        self.tableBool = BooleanVar(value=True)

        self._createCheckboxes()

        # open file button
        self.openFileB = ttk.Button(self.mainframe, text='Open File',
                                    command=self._openFileScreen)
        self.openFileB.grid(column=4, row=1, sticky=(N, S, W, E))

        # embedding figures from matplotlib
        self.graphFrame = ttk.Frame(self.mainframe)
        self.graphFrame.grid(
            column=1, row=2, columnspan=4, sticky=(N, W, E, S))
        # makes canvas resizable
        self.graphFrame.rowconfigure(0, weight=1)
        self.graphFrame.columnconfigure(0, weight=1)
        # create canvas
        self.canvas = FigureCanvasTkAgg(
            self.dis.fig, master=self.graphFrame)
        self.canvas.get_tk_widget().grid(sticky=(N, W, E, S))
        self._createPlots()

        self.createMenuBar()

    def _createPlots(self):
        self.canvas.draw()

        toolbar = NavigationToolbar2Tk(
            self.canvas, self.graphFrame, pack_toolbar=False)
        toolbar.update()

        self.canvas.mpl_connect("key_press_event", lambda event: print(
            f"you pressed {event.key}"))
        self.canvas.mpl_connect("key_press_event", key_press_handler)

        toolbar.grid(column=0, row=1, sticky=(N, S, W, E))
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky=(N, S, W, E))

    def _createCheckboxes(self):
        # checkbuttons
        checkSeg = ttk.Checkbutton(
            self.mainframe, text='Show Segmentation Lines', command=self._segChange, variable=self.segBool, onvalue=True, offvalue=False)
        checkSeg.grid(column=1, row=1, sticky=(N, S, W, E))

        checkTranscript = ttk.Checkbutton(
            self.mainframe, text='Show Transcript', command=self._transcriptChange, variable=self.transcriptBool, onvalue=True, offvalue=False)
        checkTranscript.grid(column=2, row=1, sticky=(N, S, W, E))

        checkTable = ttk.Checkbutton(
            self.mainframe, text='Show Phoneme Table', command=self._tableChange, variable=self.tableBool, onvalue=True, offvalue=False)
        checkTable.grid(column=3, row=1, sticky=(N, S, W, E))

    def _segChange(self):
        if self.segBool.get() == True:
            self.dis.showSegLines()
        elif self.segBool.get() == False:
            self.dis.hideSegLines()
        self.canvas.draw()

    def _transcriptChange(self):
        if self.transcriptBool.get() == True:
            self.dis.showTranscript()
        elif self.transcriptBool.get() == False:
            self.dis.hideTranscript()

    def _tableChange(self):
        if self.tableBool.get() == True:
            self.dis.showPhonemeTable()
        elif self.tableBool.get() == False:
            self.dis.hidePhonemeTable()

    def _loadPlots(self, path_to_file):
        x = path_to_file.split(".")
        fileType = x[-1]

        if fileType == 'DAT':
            self.dis = saveAndLoad.loadProgram(path_to_file)
            self.dis.graphDisplay()
            # todo update canvas?
            self.graphFrame.rowconfigure(0, weight=1)
            self.graphFrame.columnconfigure(0, weight=1)
            self.canvas = FigureCanvasTkAgg(
                self.dis.fig, master=self.graphFrame)
            self.canvas.get_tk_widget().grid(sticky=(N, W, E, S))
            self._createPlots()
            # self.dis.fig.canvas.draw_idle()

        elif fileType == 'wav':
            path_to_transcript = fileIO.findTranscript(path_to_file)
            self.dis = Display(path_to_file, path_to_transcript)
            self.dis.graphDisplay()
            # todo update canvas?
            self.graphFrame.rowconfigure(0, weight=1)
            self.graphFrame.columnconfigure(0, weight=1)
            self.canvas = FigureCanvasTkAgg(
                self.dis.fig, master=self.graphFrame)
            self.canvas.get_tk_widget().grid(sticky=(N, W, E, S))
            self._createPlots()
            # self.dis.fig.canvas.draw_idle()

    def _openFileScreen(self):
        path_to_file = filedialog.askopenfilename(filetypes=(
            ("Analysis file", "*.DAT"), ("Sound File", "*.wav")), title="Select File")
        if len(path_to_file) != 0:
            # a file has been selected
            self._loadPlots(path_to_file)

    def createMacOSMenuBar(self):
        super().createMacOSMenuBar()
        self.menu_view.add_separator()
        menu_showDisplays = Menu(self.menu_view)
        self.menu_view.add_cascade(
            menu=menu_showDisplays, label='Show Displays')
        menu_showDisplays.add_checkbutton(
            label='Segmentation Lines', command=self._segChange, variable=self.segBool, onvalue=True, offvalue=False)
        menu_showDisplays.add_checkbutton(
            label='Phoneme Table', command=self._tableChange, variable=self.tableBool, onvalue=True, offvalue=False)
        menu_showDisplays.add_checkbutton(
            label='Transcript', command=self._transcriptChange, variable=self.transcriptBool, onvalue=True, offvalue=False)

    def openAnalysisWindow(self):
        super().openAnalysisWindow()
        # if analysis window exists move to top
        if self.analysisW != None:
            self.analysisW.window.lift()
        else:
            self.analysisW = AnalysisWindow(self.parent,self, self.dis, self.fileName)

    def editorInfo(self):
        self.openAnalysisWindow()
        self.analysisW.insertSummaryText()

    def soundInfo(self):
        self.openAnalysisWindow()
        self.analysisW.insertSummaryText()

    def getSummary(self):
        self.openAnalysisWindow()
        self.analysisW.insertSummaryText()

    def getPhonemeAnalysis(self):
        self.openAnalysisWindow()
        self.analysisW.insertAnalysisText()

    def getCursorAnalysis(self):
        self.openAnalysisWindow()
        self.analysisW.insertCursorText(0.1, 400)  # ! change later

    def saveAs(self):
        super().saveAs()
        path_to_file = filedialog.asksaveasfilename(confirmoverwrite=True, filetypes=(
            ("Analysis file", "*.DAT")), title="Save File")
        if path_to_file.split('.')[-1] == 'DAT':
            saveAndLoad.saveProgram(path_to_file, self.dis)
        self.savedFilePath = path_to_file
    
    def save(self):
        super().save()
        if self.savedFilePath != None:
            saveAndLoad.saveProgram(self.savedFilePath, self.dis)
        else:
            self.saveAs()

    def closeWindow(self):
        if self.analysisW != None:
            self.analysisW.window.destroy()
        self.window.destroy()


class AnalysisWindow(UIWindow):
    def __init__(self, parent, displayWindow, dis, fileName):
        super().__init__(parent)
        self.dis = dis
        self.fileName = fileName
        self.displayWindow = displayWindow

        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)

        self.analysis = Analysis(self.dis)

        self.window.title(self.fileName + " Analysis")
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.textBox = Text(self.mainframe, width=40, height=10, wrap='word')
        self.textBox.grid(column=0, row=0, sticky=(N, W, E, S))

        self.createMenuBar()

    def insertSummaryText(self):
        self.textBox.insert('1.0', 'Analysis of ' + self.fileName + "\n\n")
        self.textBox.insert('end', self.analysis.getSummaryText())

    def insertAnalysisText(self):
        self.textBox.insert(
            '1.0', 'Phoneme Analysis of ' + self.fileName + "\n\n")
        self.textBox.insert(
            'end', self.analysis.getAnalysisText())

    def insertCursorText(self, startT, freq, endT=0):
        self.textBox.insert('1.0', 'Analysis of ' + self.fileName + "\n\n")
        if endT == 0:
            self.textBox.insert(
                'end', self.analysis.getAtCursorText(startT=startT, freq=freq))
        else:
            self.textBox.insert('end', self.analysis.getAtCursorText(
                startT=startT, endT=endT, freq=freq))

    def createMacOSMenuBar(self):
        super().createMacOSMenuBar()
    
    def saveAs(self):
        super().saveAs()
        path_to_file = filedialog.asksaveasfilename(confirmoverwrite=True, filetypes=(
            ("Text file", "*.txt"), ("JSON (Phoneme Segmentation)", "*.json"), ("Markdown", "*.md")), title="Save File")
        if path_to_file.split('.')[-1] == 'txt' or path_to_file.split('.')[-1] == 'md':
            saveAndLoad.saveAnalysis(path_to_file, self.textBox.get('1.0','end'))
            self.savedFilePath = path_to_file
        elif path_to_file.split('.')[-1] == 'json':
            saveAndLoad.saveAnalysis(path_to_file, self.analysis.phones)
    
    def save(self):
        super().save()
        if self.savedFilePath != None and self.savedFilePath.split('.')[-1] != 'json':
            saveAndLoad.saveAnalysis(self.savedFilePath, self.textBox.get('1.0','end'))
        else:
            self.saveAs()
    
    def closeWindow(self):
        self.displayWindow.analysisW = None
        self.window.destroy()


rt = Tk()
emptyDisplay = Display()
DisplayWindow(rt, '', emptyDisplay)
rt.mainloop()
