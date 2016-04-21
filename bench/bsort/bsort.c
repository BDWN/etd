/*
 * Modified by Boudewijn Braams
 *
 * Originaly part of the TACLeBench benchmark suite version 2.0
 *
 * Name: bsort
 * Author: unknown
 * Function: Bubblesort on arrays using integer comparisons
 *
 * Source: MRTC
 *         http://www.mrtc.mdh.se/projects/wcet/wcet_bench/bsort100/bsort100.c
 */

#include "../m5op.h"

void bsort_init( void );
void bsort_main( void );
int bsort_return( void );
int bsort_BubbleSort( int Array[] );

/* Initialization file is dynamically generated */
#include "init.c"

int bsort_return( void ) {
    return 0;
}

/* Sort array of integers in ascending order with bubble sort */
int bsort_BubbleSort( int Array[] ) {

    int Sorted = 0;
    int Temp, Index, i;

    for ( i = 0; i < bsort_SIZE - 1; i ++ ) {
        Sorted = 1;
        for ( Index = 0; Index < bsort_SIZE - 1; Index ++ ) {
            if ( Index > bsort_SIZE - i )
                break;
            if ( Array[ Index ] > Array[Index + 1] ) {
                Temp = Array[ Index ];
                Array[ Index ] = Array[ Index + 1 ];
                Array[ Index + 1 ] = Temp;
                Sorted = 0;
            }
        }

        if ( Sorted )
            break;
    }

    return 0;

}


void bsort_main(void) {

    bsort_BubbleSort( bsort_Array );

}

int main(void) {

    bsort_init();
    m5_reset_stats(0,0);
    bsort_main();
    m5_exit(0);
    return bsort_return();

}
