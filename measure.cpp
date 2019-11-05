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
uint64_t beg;
int loop_count = 0;
FILE *fp;

void handler(int nSignum, siginfo_t* si, void* vcontext) {
  uint64_t x, time_taken;
  char filename[16];
  ucontext_t* context = (ucontext_t*)vcontext;
  x = context->uc_mcontext.gregs[REG_RIP];
  time_taken = rdtsc_end() - beg;
  if(x >= 0xffffffff80000000 && loop_count < 16) {
    if(loop_count > 0) {
      fprintf(fp, "%llx, %d\n", x, time_taken);
    }
    context->uc_mcontext.gregs[REG_RIP]+=0x1000;
  } else if (loop_count < 16) {
      printf("Loop Count: %d\n", loop_count);
      context->uc_mcontext.gregs[REG_RIP] = 0xffffffff80000000;
      snprintf(filename, sizeof(filename), "output%d.csv", loop_count);
      printf("%s\n", filename);
      fclose(fp);
      if(loop_count != 15) {
        fp = fopen(filename, "w");
      }
      loop_count++;
  } else {
    exit(0);
  }
  beg = rdtsc_beg();
}

int main(void)
{
  void *addr = (void *)0xffffffff80000000;
  fp = fopen("output0.csv", "w");
  struct sigaction action;
  memset(&action, 0, sizeof(struct sigaction));
  action.sa_flags = SA_SIGINFO;
  action.sa_sigaction = handler;
  sigaction(SIGSEGV, &action, NULL);
  beg = rdtsc_beg();
  ((int(*)())addr)();

  return 0;
}
