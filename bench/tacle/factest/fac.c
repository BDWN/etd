/*
 * Modified by Boudewijn Braams
 *
 * Originaly part of the TACLeBench benchmark suite version 1.x
 *
 * Name: fac
 * Author: unknown
 * Function: Compute sum of factorials from zero to n
 *
 * Source: MRTC
 *         http://www.mrtc.mdh.se/projects/wcet/wcet_bench/fac/fac.c
 */

#include "include/m5op.h"

int fac_fac( int n );
void fac_init();
int fac_return();
void fac_main();
int main( void );

int fac_s;
volatile int fac_n;

/* Initialization file is dynamically generated */
#include "init.c"

int fac_return() {
    return fac_s;
}

int fac_fac ( int n ) {
    if ( n == 0 )
        return 1;
    else
        return (n * fac_fac ( n - 1 ));
}

void fac_main() {
    int i;

    for (i = 0;  i <= fac_n; i++) {
        fac_s += fac_fac (i);
    }
}


int main(void) {

    fac_init();
    m5_reset_stats(0,0);
    fac_main();
    m5_exit(0);
    return ( fac_return() );

}
