import os
import csv
import platform

addrString = ""
file = open("sysaddr.txt", "r")

content = file.readline()
sysaddrlist = []
kernelAddrList = []
nonKernelAddrList = []
finalAvg_KernelTime = 0
finalAvg_NonKernelTime = 0

while content:
    fileAddr = content.strip()[0:13] + "000"
    if fileAddr == addrString or int(content.strip()[0:16], 16) < 0xffffffff80000000:
        content = file.readline()
        continue
    else:
        sysaddrlist.append(fileAddr)
        content = file.readline()

sysaddrlist = set(sysaddrlist)
sysaddrlist = list(sysaddrlist)
sysaddrlist.sort()

for i in range(0,15):
    filename = "output%s.csv" % str(i)
    new_filename = "parsed output%s.csv" % str(i)
    csvfiler = open(filename, "r")
    if platform.system() == "Windows":
        csvfilew = open(new_filename, "w", newline='')
    elif platform.system() == "Linux":
        csvfilew = open(new_filename, "w")
    csvReader = csv.reader(csvfiler)
    csvWriter = csv.writer(csvfilew)
    index = 0

    for line in csvReader:
        if index < len(sysaddrlist) and line[0] == sysaddrlist[index]:
            kernelAddrList.append(line)
            index += 1
        else:
            nonKernelAddrList.append(line)

    for num in range(0, len(kernelAddrList)):
        for element in kernelAddrList[num]:
            nonKernelAddrList[num].append(element)

    totalTime = 0
    for kernelAddrRow in kernelAddrList:
        totalTime += int(kernelAddrRow[1])
    kernelAvgTime =  totalTime/len(kernelAddrList)

    totalTime = 0
    for nonKernelAddrRow in nonKernelAddrList:
        totalTime += int(nonKernelAddrRow[1])

    nonKernelAvgTime = totalTime/len(nonKernelAddrList)

    message = []
    message.append("Kernel Avg. Time:")
    message.append(kernelAvgTime)
    csvWriter.writerow(message)
    message = []
    message.append("Non Kernel Avg. Time:")
    message.append(nonKernelAvgTime)
    csvWriter.writerow(message)

    for item in nonKernelAddrList:
        csvWriter.writerow(item)

    print("Kernel Avg Time: %s " % kernelAvgTime)
    print("Non Kernel Avg Time: %s " % nonKernelAvgTime)
    kernelAddrList = []
    nonKernelAddrList = []
    csvfiler.close()
    csvfilew.close()
    finalAvg_KernelTime += kernelAvgTime
    finalAvg_NonKernelTime += nonKernelAvgTime
    print(filename + " complete")
finalAvg_KernelTime /= 15
finalAvg_NonKernelTime /= 15
print("Final Avg Kernel Time in 15 samples: %s" % finalAvg_KernelTime)
print("Final Avg Non Kernel Time in 15 samples: %s" % finalAvg_NonKernelTime)