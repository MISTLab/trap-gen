#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

// This simple program tests the correctness of the command line
// arguments manchanisms

int main(int argc, char * argv[]){
    int i = 0;

    printf("The _SC_NPROCESSORS_ONLN value is %ld\n", sysconf(_SC_NPROCESSORS_ONLN));
    printf("The PIPPO value is %ld\n", sysconf(1234556));

    return 0;
}
