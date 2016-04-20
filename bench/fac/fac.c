/*
 * Modifications:
 * - Init function in separate file
 * - Reset gem5 stats before entering main benchmark body
 * - Removed iteration count annotations, do no longer apply with generated
 *   input
*/

#include "../m5op.h"

/*

  This program is part of the TACLeBench benchmark suite.
  Version V 1.x

  Name: fac

  Author: unknown

  Function: fac is a program to calculate factorials.
    This program computes the sum of the factorials
    from zero to n.

  Source: MRTC
          http://www.mrtc.mdh.se/projects/wcet/wcet_bench/fac/fac.c

  Changes: CS 2006/05/19: Changed loop bound from constant to variable.

  License: public domain

*/


/*
  Forward declaration of functions
*/

int fac_fac( int n );
void fac_init();
int fac_return();
void fac_main();
int main( void );

/*
  Declaration of global variables
*/

int fac_s;
volatile int fac_n;

/*
  Initialization- and return-value-related functions
*/


#include "init.c"


int fac_return()
{
  return fac_s;
}


/*
  Arithmetic math functions
*/


int fac_fac ( int n )
{
  if ( n == 0 )
    return 1;
  else
    return ( n * fac_fac ( n - 1 ) );
}


/*
  Main functions
*/


void _Pragma( "entrypoint" ) fac_main ()
{
  int i;

  /* _Pragma( "loopbound min 6 max 6" ) */
  for ( i = 0;  i <= fac_n; i++ ) {
    _Pragma( "marker recursivecall" )
    fac_s += fac_fac ( i );
    /* _Pragma( "flowrestriction 1*fac_fac <= 6*recursivecall" ) */
  }
}


int main ( void )
{

  fac_init();
  m5_reset_stats(0,0);
  fac_main();

  return ( fac_return() );
}
