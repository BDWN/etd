/*
 * Modified by Boudewijn Braams
 *
 * Originaly part of the TACLeBench benchmark suite version 2.0
 *
 * Name: prime
 * Author: unknown
 * Function: Calculates whether number is prime, uses trial division
 *
 * Source: MRTC
 *         http://www.mrtc.mdh.se/projects/wcet/wcet_bench/prime/prime.c
 */

#include "../m5op.h"

unsigned char prime_divides ( unsigned int n, unsigned int m );
unsigned char prime_even ( unsigned int n );
unsigned char prime_prime ( unsigned int n );
void prime_init ();
int prime_return ();
void prime_main ();
int main( void );

int prime_result;
unsigned int x;

/* Initialization file is dynamically generated */
#include "init.c"

int prime_return () {
    return prime_result;
}

unsigned char prime_divides ( unsigned int n, unsigned int m ) {
    return ( m % n == 0 );
}

unsigned char prime_even ( unsigned int n ) {
    return ( prime_divides ( 2, n ) );
}

unsigned char prime_prime ( unsigned int n ) {
    unsigned int i;
    if ( prime_even ( n ) )
        return ( n == 2 );
        for ( i = 3; i * i <= n; i += 2 ) {
            if ( prime_divides ( i, n ) )
                return 0;
        }
    return ( n > 1 );
}

void prime_main() {
    prime_result = prime_prime( x );
}

int main( void ) {
    prime_init();
    m5_reset_stats(0,0);
    prime_main();
    m5_exit(0);
    return ( prime_return() );
}
