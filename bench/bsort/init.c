
#define bsort_SIZE 3

static int bsort_Array[ bsort_SIZE ];

static int bsort_Values[ bsort_SIZE ] = { 2,1,0 };

void bsort_init( void ) {
    for (int i = 0; i < bsort_SIZE; i++) {
        bsort_Array[i] = bsort_Values[i];
    }
}
