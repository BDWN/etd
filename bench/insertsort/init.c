
#define ARRAY_SIZE 6

unsigned int insertsort_a[ARRAY_SIZE];

void insertsort_initialize(unsigned int* array) {
    register int i;
    for ( int i = 0; i < ARRAY_SIZE; i++ )
        insertsort_a[i] = array[i];
}

void insertsort_init() {
    unsigned int a[ARRAY_SIZE] = { 5,4,3,2,1,0 };
    insertsort_initialize(a);
}
