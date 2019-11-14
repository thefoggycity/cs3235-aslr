# Side-channel Timing Attack ASLR

CS3235 AY1920S1 Project

## Note

The python scripts require `python 3.6` and above to run. Make sure you have `Tkinter` and `Matplotlib` libraries installed.

## Demonstration on Linux

To use the attack demonstration code, download all the sources in the demo_linux folder, then run `make` to build the attack library `libASLRTimingAtk.so`. After successfully building the dynamic library, run `python3 GUI.py` to show the attack plot interface. Click the "Attack" button to initiate the timing attack and the plot can be observed after a short while. The x-limit and y-limit of the plot may need to be adjusted to fit the data range.

To compare with the real system addresses, run
`# sudo cat /proc/kallsyms > sysaddr.txt`
to obtain a table of these addresses. After that, click the "Plot System Addresses" button to read the file and plot them at the bottom of the figure.

## Attack on Linux

Instead of demostrating in GUI, the attack can also be run in Linux, outputting to CSV files. The `measure.cpp` can be compiled and run, which generates 15 result files, each for a trial round, in CSV format. The `addrParse.py` script will survey the statistics of the results and give average timing for both kernel and non-kernel addresses.

## Attack on Windows

The `windows/ASLRtiming.cpp` can be compiled with MSVC compiler. For each run, the program will attempt 5 trials and take the minimum access timing for each address. The program should be run multiple time, each time piping the result to `result<n>.txt`, where `<n>` is to be substituted by indices.

After obtaining the results, the Python script `plot.py` can be utilised to visualize the results.
