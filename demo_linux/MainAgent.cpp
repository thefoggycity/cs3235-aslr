/* 
 * CS3235 AY1920S1 Project
 * Side-channel Timing Attack ASLR
 * Author: Li Yunfan
 * Description: 
 * Main routine for side-channel attack library. Invokes 
 * necessary functions and pass the final result to the 
 * caller Python script.
 * Revisions:
 * 24/10/2019    File created.
 */

#include "MainAgent.h"

// libAgent: Entry point of the library.
// retBuff  Int buffer allocated in Python, for returning result.
// buffSize Number of element of retBuff.
void libAgent(int retBuff[], size_t buffSize)
{
    // srand(time(NULL));
    runMeasure();
    for (size_t i = 0; i < buffSize; i++)
        // retBuff[i] = rand() % 10;
        retBuff[i] = (int)(meas[i]);
}
