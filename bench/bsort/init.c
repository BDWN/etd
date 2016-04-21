
#define bsort_SIZE 6

static int bsort_Array[ bsort_SIZE ];

static int bsort_Values[ bsort_SIZE ] = { 5,4,3,2,1,0 };

void bsort_init( void ) {
    for (int i = 0; i < bsort_SIZE; i++) {
        bsort_Array[i] = bsort_Values[i];
    }
}
