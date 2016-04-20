CC=aarch64-linux-gnu-gcc
CFLAGS=-march=armv8-a -static
OBJS=../m5op_arm_A64.o

all: fac

fac: fac.o
	$(CC) $(CFLAGS) -o a.out fac.o $(OBJS)

fac.o: fac.c
	$(CC) $(CFLAGS) -c fac.c

clean:
	-rm -f *.o
	-rm -f a.out
