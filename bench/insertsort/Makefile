CC=aarch64-linux-gnu-gcc
CFLAGS=-march=armv8-a -static
OBJS=../m5op_arm_A64.o

all: insertsort

insertsort: insertsort.o
	$(CC) $(CFLAGS) -o a.out insertsort.o $(OBJS)

insertsort.o: insertsort.c
	$(CC) $(CFLAGS) -c insertsort.c

clean:
	-rm -f *.o
	-rm -f a.out
