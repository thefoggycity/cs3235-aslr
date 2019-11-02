/* 
 * CS3235 AY1920S1 Project
 * Side-channel Timing Attack ASLR
 * Author: Eldon Ng, Li Yunfan
 * Description: 
 * Header file of AslrAttack.c.
 * Revisions:
 * 02/11/2019    File created from measure.cpp
 */

#ifndef _ASLR_ATTACK_H_
#define _ASLR_ATTACK_H_

#include <inttypes.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <iostream>
#include <fstream>
#include <signal.h>
#include <unistd.h>

#include <sys/mman.h>

#define __USE_GNU

#include "rdtsc.h"

extern int meas[0x80000];
extern int runMeasure(void);

#endif // _ASLR_ATTACK_H_