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
cFunc = x._Z8libAgentPim
cFunc.argtypes = ctypes.POINTER(ctypes.c_int), ctypes.c_size_t
cFunc.restype = None

def runAttack() :
    ptrRetBuff = (ctypes.c_int * 0x80000)()
    cFunc(ptrRetBuff, len(ptrRetBuff))
    return list(ptrRetBuff)

#####################
## INTERFACE SETUP ##
#####################

def axesSetup(a):
    a.get_xaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: "0x%x" % int(x)))
    a.set_xlim([0x80000, 0xfffff])
    a.set_ylim([4500,4800])

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

# Plot System Addresses Button

def readSysAddr():
    # Copied from the first half of addrParse.py
    # As reading /proc/kallsyms requires root priviledges (otherwise 
    # addresses will be all zeros), the program reads a txt file 
    # obtained by user (with sudo or root identity).

    addrString = ""
    f = open("sysaddr.txt", "r")
    content = f.readline()

    sysaddrlist = []
    while content:
        fileAddr = content.strip()[0:13] + "000"
        if fileAddr == addrString or int(content.strip()[0:16], 16) < 0xffffffff80000000:
            content = f.readline()
            continue
        else:
            sysaddrlist.append(fileAddr)
            content = f.readline()

    sysaddrlist = set(sysaddrlist)
    sysaddrlist = list(sysaddrlist)
    sysaddrlist.sort()

    return [int(a[8:], 16) >> 12 for a in sysaddrlist]

def pltSysAddr() :
    xData = readSysAddr()
    yData = [4501 for _ in range(len(xData))]
    subp.scatter(xData, yData, c='r', marker='.')
    canvas.draw()

btnPlot = tkinter.Button(master=root, text="Plot System Addresses", command=pltSysAddr)
btnPlot.pack(side=tkinter.BOTTOM)

# Plot Button

btnPlotText = tkinter.StringVar()
btnPlotText.set("Attack")
frmCounter = 0

def updPlot(xData, yData):
    global frmCounter
    subp.clear()
    axesSetup(subp)
    subp.scatter(xData, yData, c='b', marker='.')
    canvas.draw()
    frmCounter += 1

def updPlotMin():
    numRounds = 3
    xData = np.linspace(0x80000, 0xfffff, 0x80000)
    yData = runAttack()
    updPlot(xData, yData)
    for _ in range(numRounds - 1):
        yTmp = runAttack()
        for i in range(len(yData)) :
            if yData[i] > yTmp[i] : 
                yData[i] = yTmp[i]
        del yTmp
        updPlot(xData, yData)
    btnPlotText.set("Attack Again")

btnPlot = tkinter.Button(master=root, textvariable=btnPlotText, command=updPlotMin)
btnPlot.pack(side=tkinter.BOTTOM)


tkinter.mainloop()