/*
 * Modified by Boudewijn Braams
 *
 * Originaly part of the TACLeBench benchmark suite version 1.0
 *
 * Name: insertsort
 * Author: Sung-Soo Lim
 * Function: Insertion sort for integer numbers
 *
 * Source: MRTC
 *         http://www.mrtc.mdh.se/projects/wcet/wcet_bench/insertsort/insertsort.c
 * Derived from: SNU-RT Benchmark Suite for WCET analysis by Sung-Soo Lim
 */

#include "../m5op.h"

void insertsort_initialize(unsigned int* array);
void insertsort_init(void);
int insertsort_return(void);
void insertsort_main(void);
int main( void );

/* Initialization file is dynamically generated */
#include "init.c"

int insertsort_return() {
    return 0;
}

void insertsort_main() {

    int  i,j, temp;
    i = 1;

    while(i <= ARRAY_SIZE) {
        j = i;
        while (insertsort_a[j] < insertsort_a[j-1]) {
            temp = insertsort_a[j];
            insertsort_a[j] = insertsort_a[j-1];
            insertsort_a[j-1] = temp;
            j--;
        }
        i++;
    }

}

int main( void ) {

    insertsort_init();
    m5_reset_stats(0,0);
    insertsort_main();
    m5_exit(0);
    return (insertsort_return());

}
