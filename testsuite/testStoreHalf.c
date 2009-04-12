#include <stdlib.h>

#include "endianess.h"

extern void _exit(int);

int main(){
    unsigned int a;
    ((unsigned short *)&a)[0] = 0x3412;
    ((unsigned short *)&a)[1] = 0x7856;
    #ifndef BIG_TARGET
    if(a != 0x78563412){
        _exit(-1);
    }
    #else
    if(a != 0x34127856){
        _exit(-1);
    }
    #endif
    _exit(0);
}
