#include <stdlib.h>

const unsigned int a = 0x12fe34dc;

extern void _exit(int);

int main(){
    #ifndef BIG_TARGET
    if(((unsigned char *)&a)[0] != 0xdc){
        _exit(-1);
    }
    if(((unsigned char *)&a)[1] != 0x34){
        _exit(-2);
    }
    if(((unsigned char *)&a)[2] != 0xfe){
        _exit(-3);
    }
    if(((unsigned char *)&a)[3] != 0x12){
        _exit(-4);
    }
    #else
    if(((unsigned char *)&a)[3] != 0xdc){
        _exit(-1);
    }
    if(((unsigned char *)&a)[2] != 0x34){
        _exit(-2);
    }
    if(((unsigned char *)&a)[1] != 0xfe){
        _exit(-3);
    }
    if(((unsigned char *)&a)[0] != 0x12){
        _exit(-4);
    }
    #endif
    _exit(0);
}
