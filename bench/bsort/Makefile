CC=aarch64-linux-gnu-gcc
CFLAGS=-march=armv8-a -static
OBJS=../m5op_arm_A64.o

all: bsort

bsort: bsort.o
	$(CC) $(CFLAGS) -o a.out bsort.o $(OBJS)

bsort.o: bsort.c
	$(CC) $(CFLAGS) -c bsort.c

clean:
	-rm -f *.o
	-rm -f a.out
