#include <inttypes.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <unistd.h>

#include <sys/mman.h>

#define __USE_GNU

#include "rdtsc.h"
#include "rtm.h"

#define ITERATION 10


// TSX RTM routine that measures one probe on the address
uint64_t tsxMeasure(void *addr) {
  uint64_t beg = rdtsc_beg();

  if (_xbegin() == _XBEGIN_STARTED) {
    ((int(*)())addr)();
    _xend();
  } else {
    // TSX abort triggered!
    return rdtsc_end() - beg;
  }
}

// Iteratively probe the address with TSX RTM, and get the minimum timing
uint64_t measure(void *addr, FILE *fp) {
  int i;
  uint64_t clk, min = (uint64_t) -1;
  
  for(i=0; i<ITERATION; i++) {
    clk = tsxMeasure(addr);
    if (clk < min)
      min = clk;
  }
  fprintf(fp, "%llx, %d\n", addr, min);
  
  return  min;
}

int main(int argc, char **argv)
{
  FILE *fp;
  int addr = 0xffffffff80000000;
  fp = fopen("tsx_output.csv", "w");
  
  while(addr > 0) {
      measure((void *)addr, fp);
      addr += 0x1000;
  }
  
  fclose(fp);
  
  return 0;
}