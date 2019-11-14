CC = g++
CCOPTS = -Wall -fPIC -std=gnu11

Objects = MainAgent.o AslrAttack.o

ExtHdrs = rdtsc.h

all: 
	g++ -c -Wall -fPIC -o MainAgent.o MainAgent.cpp
	g++ -c -Wall -fPIC -o AslrAttack.o AslrAttack.cpp
	g++ -shared -o libASLRTimingAtk.so MainAgent.o AslrAttack.o

%.o: %.c %.h $(ExtHdrs)
	$(CC) -c -Wall -fPIC -std=gnu11 -o $@ $<

libASLRTimingAtk.so: $(Objects)
	$(CC) -shared -o libASLRTimingAtk.so $^

clean:
	rm -rf *.o
	rm -rf *.so

.PHONY: clean
