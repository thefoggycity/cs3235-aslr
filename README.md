# Side-channel Timing Attack ASLR

CS3235 AY1920S1 Project

## Demonstration on Linux

To use the attack demonstration code, download all the sources in the demo_linux folder, then run `make` to build the attack library `libASLRTimingAtk.so`. After successfully building the dynamic library, run `python3 GUI.py` to show the attack plot interface. Click the "Attack" button to initiate the timing attack and the plot can be observed after a short while. The x-limit and y-limit of the plot may need to be adjusted to fit the data range.

To compare with the real system addresses, run
`# cat /proc/kallsyms > sysaddr.txt`
to obtain a table of these addresses. After that, click the "Plot System Addresses" button to read the file and plot them at the bottom of the figure.
