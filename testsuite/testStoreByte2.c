#include <stdlib.h>

extern void _exit(int);

int main(){
    unsigned int a;
    ((unsigned char *)&a)[0] = 0x12;
    ((unsigned char *)&a)[1] = 0x34;
    ((unsigned char *)&a)[2] = 0x56;
    ((unsigned char *)&a)[3] = 0x78;
    #ifndef BIG_TARGET
    if(a != 0x78563412){
        _exit(-1);
    }
    #else
    if(a != 0x12345678){
        _exit(-1);
    }
    #endif
    _exit(0);
}
