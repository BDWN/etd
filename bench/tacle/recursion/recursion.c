/*
 * Modified by Boudewijn Braams
 *
 * Originaly part of the TACLeBench benchmark suite version 1.x
 *
 * Name: recursion
 * Author: unknown
 * Function: Computes nth Fibonacci number recursively
 *
 * Source: MRTC
 *         http://www.mrtc.mdh.se/projects/wcet/wcet_bench/recursion/recursion.c
 */

#include "include/m5op.h"

int recursion_result;
int recursion_input;

int recursion_fib( int i );
void recursion_main( void );
void recursion_init( void );
int recursion_return( void );
int main ( void );

/* Initialization file is dynamically generated */
#include "init.c"

int recursion_fib( int i ) {
    if ( i == 0 ) return 1;
    if ( i == 1 ) return 1;
    return recursion_fib( i - 1 ) + recursion_fib( i - 2 );
}

int recursion_return() {
    return 0;
}

void recursion_main( void ) {
    recursion_result = recursion_fib( recursion_input );
}

int main( void ) {
    recursion_init();
    m5_reset_stats(0,0);
    recursion_main();
    m5_exit(0);
    return ( recursion_return() );
}
