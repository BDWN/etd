CC=aarch64-linux-gnu-gcc
CFLAGS=-march=armv8-a -static
OBJS=include/m5op_arm_A64.o

all: recursion

recursion: recursion.o
	$(CC) $(CFLAGS) -o a.out recursion.o $(OBJS)

recursion.o: recursion.c
	$(CC) $(CFLAGS) -c recursion.c

clean:
	-rm -f *.o
	-rm -f a.out
