#include <stdlib.h>

#include "endianess.h"

extern void _exit(int);

int main(){
    char a[4];
    a[0] = 'a';
    a[1] = 'b';
    a[2] = 'c';
    a[3] = 'd';
    #ifndef BIG_TARGET
    if(*((unsigned int *)a) != 0x64636261){
        _exit(-1);
    }
    #else
    if(*((unsigned int *)a) != 0x61626364){
        _exit(-1);
    }
    #endif
    _exit(0);
}
