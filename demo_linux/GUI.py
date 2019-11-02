# CS3235 AY1920S1 Project
# Side-channel Timing Attack ASLR
# Author: Li Yunfan
# Description: 
# Main GUI for demonstration, load and call the attack program
# written in C and compiled into dynamic library.
# Revisions:
# 24/10/2019    File created.

import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import numpy as np 
import ctypes
import ctypes.util
import time

#####################
## LOAD ATTACK DLL ##
#####################

x = ctypes.CDLL('./demo_linux/libASLRTimingAtk.so')
cFunc = x.libAgent
cFunc.argtypes = ctypes.POINTER(ctypes.c_int), ctypes.c_size_t
cFunc.restype = None

def runAttack() :
    ptrRetBuff = (ctypes.c_int * 5)()
    cFunc(ptrRetBuff, len(ptrRetBuff))
    return list(ptrRetBuff)

#####################
## INTERFACE SETUP ##
#####################

def axesSetup(a):
    a.get_xaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: "0x%x" % int(x)))
    a.set_xlim([0,6])
    a.set_ylim([-1,10])

root = tkinter.Tk()
root.wm_title("ASLR Attack Demo")

fig = Figure(figsize=(5,4), dpi=120)
subp = fig.add_subplot(111)
axesSetup(subp)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

#####################
## BUTTONS HANDLER ##
#####################

# Quit Button

def quitWindow():
    root.quit()
    root.destroy()

btnQuit = tkinter.Button(master=root, text="Quit", command=quitWindow)
btnQuit.pack(side=tkinter.BOTTOM)

# Reset Button

def resetPlot():
    subp.clear()
    axesSetup(subp)
    canvas.draw()

btnReset = tkinter.Button(master=root, text="Reset", command=resetPlot)
btnReset.pack(side=tkinter.BOTTOM)

# Plot Button

btnPlotText = tkinter.StringVar()
btnPlotText.set("Plot")
frmCounter = 0

def updPlot():
    global frmCounter
    xData = np.linspace(1, 5, 5)
    yData = runAttack()
    subp.scatter(xData, yData, c='b', marker='.')
    canvas.draw()
    btnPlotText.set("Plot again")
    frmCounter += 1

def updPlotMulti():
    for _ in range(3):
        updPlot()
        time.sleep(1)

btnPlot = tkinter.Button(master=root, textvariable=btnPlotText, command=updPlotMulti)
btnPlot.pack(side=tkinter.BOTTOM)


tkinter.mainloop()