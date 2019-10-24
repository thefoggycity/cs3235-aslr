CC = gcc
CCOPTS = -Wall -fpic

Objects = MainAgent.o

%.o: %.c %.h
	$(CC) -c $(CCOPTS) -o $@ $<

dynlib: $(Objects)
	$(CC) -shared -o libASLRTimingAtk.so $^

all: dynlib

clean:
	rm -rf *.o

.PHONY: clean
