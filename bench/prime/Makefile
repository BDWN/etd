CC=aarch64-linux-gnu-gcc
CFLAGS=-march=armv8-a -static
OBJS=../m5op_arm_A64.o

all: prime

prime: prime.o
	$(CC) $(CFLAGS) -o a.out prime.o $(OBJS)

prime.o: prime.c
	$(CC) $(CFLAGS) -c prime.c

clean:
	-rm -f *.o
	-rm -f a.out
