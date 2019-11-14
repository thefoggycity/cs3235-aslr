import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker

def fmtShow():
    axes = plt.gca()
    # axes.get_xaxis().set_major_locator(ticker.MultipleLocator(0x80000))
    axes.get_xaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: "0x%x" % int(x)))
    axes.set_ylim([5000,7000])
    plt.show()

if __name__ == "__main__":
    numRes = 4
    addrIntv = 0x10000
    numAddr = 0x80000000 // addrIntv

    resArr = np.zeros((numRes, numAddr))
    for fid in range(0, numRes) :
        resFile = open("result%d.txt" % (fid + 1), 'r')
        for n in range(numAddr) :
            resArr[fid][n] = int(resFile.readline())
    
    xArr = np.linspace(0x80000000, 0x100000000 - addrIntv, numAddr)

    plt.scatter(np.tile(xArr, numRes), resArr.flatten(), marker='.')
    fmtShow()