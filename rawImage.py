from __future__ import print_function, division
import WalabotAPI as wlbt
try: # for Python 2
    import Tkinter as tk
except ImportError: # for Python 3
    import tkinter as tk
try: # for Python 2
    range = xrange
except NameError:
    pass

COLORS = ["000083", "000087", "00008B", "00008F", "000093", "000097", "00009B",
    "00009F", "0000A3", "0000A7", "0000AB", "0000AF", "0000B3", "0000B7",
    "0000BB", "0000BF", "0000C3", "0000C7", "0000CB", "0000CF", "0000D3",
    "0000D7", "0000DB", "0000DF", "0000E3", "0000E7", "0000EB", "0000EF",
    "0000F3", "0000F7", "0000FB", "0000FF", "0003FF", "0007FF", "000BFF",
    "000FFF", "0013FF", "0017FF", "001BFF", "001FFF", "0023FF", "0027FF",
    "002BFF", "002FFF", "0033FF", "0037FF", "003BFF", "003FFF", "0043FF",
    "0047FF", "004BFF", "004FFF", "0053FF", "0057FF", "005BFF", "005FFF",
    "0063FF", "0067FF", "006BFF", "006FFF", "0073FF", "0077FF", "007BFF",
    "007FFF", "0083FF", "0087FF", "008BFF", "008FFF", "0093FF", "0097FF",
    "009BFF", "009FFF", "00A3FF", "00A7FF", "00ABFF", "00AFFF", "00B3FF",
    "00B7FF", "00BBFF", "00BFFF", "00C3FF", "00C7FF", "00CBFF", "00CFFF",
    "00D3FF", "00D7FF", "00DBFF", "00DFFF", "00E3FF", "00E7FF", "00EBFF",
    "00EFFF", "00F3FF", "00F7FF", "00FBFF", "00FFFF", "03FFFB", "07FFF7",
    "0BFFF3", "0FFFEF", "13FFEB", "17FFE7", "1BFFE3", "1FFFDF", "23FFDB",
    "27FFD7", "2BFFD3", "2FFFCF", "33FFCB", "37FFC7", "3BFFC3", "3FFFBF",
    "43FFBB", "47FFB7", "4BFFB3", "4FFFAF", "53FFAB", "57FFA7", "5BFFA3",
    "5FFF9F", "63FF9B", "67FF97", "6BFF93", "6FFF8F", "73FF8B", "77FF87",
    "7BFF83", "7FFF7F", "83FF7B", "87FF77", "8BFF73", "8FFF6F", "93FF6B",
    "97FF67", "9BFF63", "9FFF5F", "A3FF5B", "A7FF57", "ABFF53", "AFFF4F",
    "B3FF4B", "B7FF47", "BBFF43", "BFFF3F", "C3FF3B", "C7FF37", "CBFF33",
    "CFFF2F", "D3FF2B", "D7FF27", "DBFF23", "DFFF1F", "E3FF1B", "E7FF17",
    "EBFF13", "EFFF0F", "F3FF0B", "F7FF07", "FBFF03", "FFFF00", "FFFB00",
    "FFF700", "FFF300", "FFEF00", "FFEB00", "FFE700", "FFE300", "FFDF00",
    "FFDB00", "FFD700", "FFD300", "FFCF00", "FFCB00", "FFC700", "FFC300",
    "FFBF00", "FFBB00", "FFB700", "FFB300", "FFAF00", "FFAB00", "FFA700",
    "FFA300", "FF9F00", "FF9B00", "FF9700", "FF9300", "FF8F00", "FF8B00",
    "FF8700", "FF8300", "FF7F00", "FF7B00", "FF7700", "FF7300", "FF6F00",
    "FF6B00", "FF6700", "FF6300", "FF5F00", "FF5B00", "FF5700", "FF5300",
    "FF4F00", "FF4B00", "FF4700", "FF4300", "FF3F00", "FF3B00", "FF3700",
    "FF3300", "FF2F00", "FF2B00", "FF2700", "FF2300", "FF1F00", "FF1B00",
    "FF1700", "FF1300", "FF0F00", "FF0B00", "FF0700", "FF0300", "FF0000",
    "FB0000", "F70000", "F30000", "EF0000", "EB0000", "E70000", "E30000",
    "DF0000", "DB0000", "D70000", "D30000", "CF0000", "CB0000", "C70000",
    "C30000", "BF0000", "BB0000", "B70000", "B30000", "AF0000", "AB0000",
    "A70000", "A30000", "9F0000", "9B0000", "970000", "930000", "8F0000",
    "8B0000", "870000", "830000", "7F0000"]

APP_X, APP_Y = 50, 50 # location of top-left corner of window
CANVAS_LENGTH = 650 # in pixels


class RawImageApp(tk.Frame):
    """ Main app class.
    """

    def __init__(self, master):
        """ Init the GUI components and the Walabot API.
        """
        tk.Frame.__init__(self, master)
        self.canvasPanel = CanvasPanel(self)
        self.wlbtPanel = WalabotPanel(self)
        self.ctrlPanel = ControlPanel(self)
        self.canvasPanel.pack(side=tk.RIGHT, anchor=tk.NE)
        self.wlbtPanel.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH, pady=10)
        self.ctrlPanel.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH, pady=10)
        self.wlbt = Walabot()

    def initAppLoop(self):
        if self.wlbt.isConnected():
            self.ctrlPanel.statusVar.set('STATUS_CONNECTED')
            self.update_idletasks()
            params = self.wlbtPanel.getParams()
            self.wlbt.setParams(*params)
            self.wlbtPanel.setParams(*self.wlbt.getArenaParams())
            if not params[4]: # equals: if not mtiMode
                self.ctrlPanel.statusVar.set('STATUS_CALIBRATING')
                self.update_idletasks()
                self.wlbt.calibrate()
            self.lenOfPhi, self.lenOfR = self.wlbt.getRawImageSliceDimensions()
            self.canvasPanel.setGrid(self.lenOfPhi, self.lenOfR)
            self.wlbtPanel.changeEntriesState('disabled')
            self.loop()
        else:
            self.ctrlPanel.statusVar.set('STATUS_DISCONNECTED')

    def loop(self):
        self.ctrlPanel.statusVar.set('STATUS_SCANNING')
        rawImage = self.wlbt.triggerAndGetRawImageSlice()
        self.canvasPanel.update(rawImage, self.lenOfPhi, self.lenOfR)
        self.ctrlPanel.fpsVar.set(self.wlbt.getFps())
        self.cyclesId = self.after_idle(self.loop)


class WalabotPanel(tk.LabelFrame):

    class WalabotParameter(tk.Frame):
        """ The frame that sets each Walabot parameter line.
        """

        def __init__(self, master, varVal, minVal, maxVal, defaultVal):
            """ Init the Labels (parameter name, min/max value) and entry.
            """
            tk.Frame.__init__(self, master)
            tk.Label(self, text=varVal).pack(side=tk.LEFT, padx=(0, 5), pady=1)
            self.minVal, self.maxVal = minVal, maxVal
            self.var = tk.StringVar()
            self.var.set(defaultVal)
            self.entry = tk.Entry(self, width=7, textvariable=self.var)
            self.entry.pack(side=tk.LEFT)
            self.var.trace("w", lambda a, b, c, var=self.var: self.validate())
            txt = "[{}, {}]".format(minVal, maxVal)
            tk.Label(self, text=txt).pack(side=tk.LEFT, padx=(5, 20), pady=1)

        def validate(self):
            """ Checks that the entered value is a valid number and between
                the min/max values. Change the font color of the value to red
                if False, else to black (normal).
            """
            num = self.var.get()
            try:
                num = float(num)
                if num < self.minVal or num > self.maxVal:
                    self.entry.config(fg='#'+COLORS[235]); return
                self.entry.config(fg='gray1')
            except ValueError:
                self.entry.config(fg='#'+COLORS[235]); return

        def get(self):
            """ Returns the entry value as a float.
            """
            return float(self.var.get())

        def set(self, value):
            """ Sets the entry value according to a given one.
            """
            self.var.set(value)

        def changeState(self, state):
            """ Change the entry state according to a given one.
            """
            self.entry.configure(state=state)

    class WalabotParameterMTI(tk.Frame):
        """ The frame that control the Walabot MTI parameter line.
        """

        def __init__(self, master):
            """ Init the MTI line (label, radiobuttons).
            """
            tk.Frame.__init__(self, master)
            tk.Label(self, text="MTI      ").pack(side=tk.LEFT)
            self.mtiVar = tk.IntVar()
            self.mtiVar.set(0)
            self.true = tk.Radiobutton(self, text="True",
                variable=self.mtiVar, value=2)
            self.false = tk.Radiobutton(self, text="False",
                variable=self.mtiVar, value=0)
            self.true.pack(side=tk.LEFT)
            self.false.pack(side=tk.LEFT)

        def get(self):
            """ Returns the value of the pressed radiobutton.
            """
            return self.mtiVar.get()

        def set(self, value):
            """ Sets the pressed radiobutton according to a given value.
            """
            self.mtiVar.set(value)

        def changeState(self, state):
            """ Change the state of the radiobuttons according to a given one.
            """
            self.true.configure(state=state)
            self.false.configure(state=state)

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Walabot Configuration')
        self.rMin = self.WalabotParameter(self, 'R     Min', 1, 1000, 10.0)
        self.rMax = self.WalabotParameter(self, 'R     Max', 1, 1000, 100.0)
        self.rRes = self.WalabotParameter(self, 'R     Res', 0.1, 10, 2.0)
        self.tMin = self.WalabotParameter(self, 'Theta Min', -90, 90, -20.0)
        self.tMax = self.WalabotParameter(self, 'Theta Max', -90, 90, 20.0)
        self.tRes = self.WalabotParameter(self, 'Theta Res', 0.1, 10, 10.0)
        self.pMin = self.WalabotParameter(self, 'Phi   Min', -90, 90, -45.0)
        self.pMax = self.WalabotParameter(self, 'Phi   Max', -90, 90, 45.0)
        self.pRes = self.WalabotParameter(self, 'Phi   Res', 0.1, 10, 2.0)
        self.thld = self.WalabotParameter(self, 'Threshold', 0.1, 100, 15.0)
        self.mti = self.WalabotParameterMTI(self)
        self.parameters = (self.rMin, self.rMax, self.rRes,
            self.tMin, self.tMax, self.tRes, self.pMin, self.pMax, self.pRes,
            self.thld, self.mti)
        for param in self.parameters:
            param.pack(anchor=tk.W)

    def getParams(self):
        rParams = (self.rMin.get(), self.rMax.get(), self.rRes.get())
        tParams = (self.tMin.get(), self.tMax.get(), self.tRes.get())
        pParams = (self.pMin.get(), self.pMax.get(), self.pRes.get())
        thldParam, mtiParam = self.thld.get(), self.mti.get()
        return rParams, tParams, pParams, thldParam, mtiParam

    def setParams(self, rParams, thetaParams, phiParams, threshold):
        self.rMin.set(rParams[0])
        self.rMax.set(rParams[1])
        self.rRes.set(rParams[2])
        self.tMin.set(thetaParams[0])
        self.tMax.set(thetaParams[1])
        self.tRes.set(thetaParams[2])
        self.pMin.set(phiParams[0])
        self.pMax.set(phiParams[1])
        self.pRes.set(phiParams[2])
        self.thld.set(threshold)

    def changeEntriesState(self, state):
        for param in self.parameters:
            param.changeState(state)


class ControlPanel(tk.LabelFrame):
    """ This class is designed to control the control area of the app.
    """

    def __init__(self, master):
        """ Initialize the buttons and the data labels.
        """
        tk.LabelFrame.__init__(self, master, text='Control Panel')
        self.buttonsFrame = tk.Frame(self)
        self.runButton, self.stopButton = self.setButtons(self.buttonsFrame)
        self.statusFrame = tk.Frame(self)
        self.statusVar = self.setVar(self.statusFrame, 'APP_STATUS', '')
        self.errorFrame = tk.Frame(self)
        self.errorVar = self.setVar(self.errorFrame, 'EXCEPTION', '')
        self.fpsFrame = tk.Frame(self)
        self.fpsVar = self.setVar(self.fpsFrame, 'FRAME_RATE', 'N/A')
        self.buttonsFrame.grid(row=0, column=0, sticky=tk.W)
        self.statusFrame.grid(row=1, columnspan=2, sticky=tk.W)
        self.errorFrame.grid(row=2, columnspan=2, sticky=tk.W)
        self.fpsFrame.grid(row=3, columnspan=2, sticky=tk.W)

    def setButtons(self, frame):
        """ Initialize the 'Start' and 'Stop' buttons.
        """
        runButton = tk.Button(frame, text='Start', command=self.start)
        stopButton = tk.Button(frame, text='Stop', command=self.stop)
        runButton.grid(row=0, column=0)
        stopButton.grid(row=0, column=1)
        return runButton, stopButton

    def setVar(self, frame, varText, default):
        """ Initialize the data frames.
        """
        strVar = tk.StringVar()
        strVar.set(default)
        tk.Label(frame, text=(varText).ljust(12)).grid(row=0, column=0)
        tk.Label(frame, textvariable=strVar).grid(row=0, column=1)
        return strVar

    def start(self):
        """ Applied when 'Start' button is pressed. Starts the Walabot and
            the app cycles.
        """
        self.master.initAppLoop()

    def stop(self):
        """ Applied when 'Stop' button in pressed. Stops the Walabot and the
            app cycles.
        """
        if hasattr(self.master, 'cyclesId'):
            self.master.after_cancel(self.master.cyclesId)
            self.master.wlbtPanel.changeEntriesState('normal')
            self.master.canvasPanel.reset()
            self.statusVar.set('STATUS_IDLE')


class CanvasPanel(tk.LabelFrame):
    """ This class is designed to control the canvas area of the app.
    """

    def __init__(self, master):
        """ Initialize the label-frame and canvas.
        """
        tk.LabelFrame.__init__(self, master, text='Raw Image Slice: R / Phi')
        self.canvas = tk.Canvas(self, width=CANVAS_LENGTH,
                height=CANVAS_LENGTH)
        self.canvas.pack()
        self.canvas.configure(background='#'+COLORS[0])

    def setGrid(self, sizeX, sizeY):
        """ Set the canvas components (rectangles), given the size of the axes.
            Arguments:
                sizeX       Number of cells in Phi axis.
                sizeY       Number of cells in R axis.
        """
        recHeight, recWidth = CANVAS_LENGTH/sizeX, CANVAS_LENGTH/sizeY
        self.cells = [[self.canvas.create_rectangle(recWidth*col,
            recHeight*row, recWidth*(col+1), recHeight*(row+1), width=0)
            for col in range(sizeY)] for row in range(sizeX)]

    def update(self, rawImage, lenOfPhi, lenOfR):
        """ Updates the canvas cells colors acorrding to a given rawImage
            matrix and it's dimensions.
            Arguments:
                rawImage    A 2D matrix contains the current rawImage slice.
                lenOfPhi    Number of cells in Phi axis.
                lenOfR      Number of cells in R axis.
        """
        for i in range(lenOfPhi):
            for j in range(lenOfR):
                self.canvas.itemconfigure(self.cells[lenOfPhi-i-1][j],
                    fill='#'+COLORS[rawImage[i][j]])

    def reset(self):
        """ Deletes all the canvas components (colored rectangles).
        """
        self.canvas.delete('all')


class Walabot:
    """ Control the Walabot using the Walabot API.
    """

    def __init__(self):
        """ Init the Walabot API.
        """
        self.wlbt = wlbt
        self.wlbt.Init()
        self.wlbt.SetSettingsFolder()

    def isConnected(self):
        """ Try to connect the Walabot device. Return True/False accordingly.
        """
        try:
            self.wlbt.ConnectAny()
        except self.wlbt.WalabotError as err:
            if err.code == 19: # "WALABOT_INSTRUMENT_NOT_FOUND"
                return False
            else:
                raise err
        return True

    def setParams(self, r, theta, phi, threshold, mti):
        """ Set the arena Parameters according given ones.
        """
        self.wlbt.SetProfile(self.wlbt.PROF_SENSOR)
        self.wlbt.SetArenaR(*r)
        self.wlbt.SetArenaTheta(*theta)
        self.wlbt.SetArenaPhi(*phi)
        self.wlbt.SetThreshold(threshold)
        self.wlbt.SetDynamicImageFilter(mti)
        self.wlbt.Start()

    def getArenaParams(self):
        """ Returns the Walabot parameters from the Walabot SDK.
            Returns:
                params      rParams, thetaParams, phiParams, threshold as
                            given from the Walabot SDK.
        """
        rParams = self.wlbt.GetArenaR()
        thetaParams = self.wlbt.GetArenaTheta()
        phiParams = self.wlbt.GetArenaPhi()
        threshold = self.wlbt.GetThreshold()
        return rParams, thetaParams, phiParams, threshold

    def calibrate(self):
        """ Calibrates the Walabot.
        """
        self.wlbt.StartCalibration()
        while self.wlbt.GetStatus()[0] == self.wlbt.STATUS_CALIBRATING:
            self.wlbt.Trigger()

    def getRawImageSliceDimensions(self):
        """ Returns the dimensions of the rawImage 2D list given from the
            Walabot SDK.
            Returns:
                lenOfPhi    Num of cells in Phi axis.
                lenOfR      Num of cells in Theta axis.
        """
        return self.wlbt.GetRawImageSlice()[1:3]

    def triggerAndGetRawImageSlice(self):
        """ Returns the rawImage given from the Walabot SDK.
            Returns:
                rawImage    A rawImage list as described in the Walabot docs.
        """
        self.wlbt.Trigger()
        return self.wlbt.GetRawImageSlice()[0]

    def getFps(self):
        """ Returns the Walabot current fps as given from the Walabot SDK.
            Returns:
                fpsVar      Number of frames per seconds.
        """
        return int(self.wlbt.GetAdvancedParameter('FrameRate'))


def rawImage():
    """ Main app function. Init the main app class, configure the window
        and start the mainloop.
    """
    root = tk.Tk()
    root.title('Walabot - Raw Image Slice Example')
    iconFile = tk.PhotoImage(file="walabot-icon.png")
    root.tk.call("wm", "iconphoto", root._w, iconFile) # set app icon
    root.option_add("*Font", "TkFixedFont")
    RawImageApp(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.geometry("+{}+{}".format(APP_X, APP_Y)) # set window location
    root.update()
    root.minsize(width=root.winfo_reqwidth(), height=root.winfo_reqheight())
    root.mainloop()


if __name__ == '__main__':
    rawImage()
