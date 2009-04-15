#include <stdlib.h>

extern void _exit(int);

int main(){
    unsigned int a = 0x12fe34dc;
    #ifndef BIG_TARGET
    if(((unsigned short *)&a)[0] != 0x34dc){
        _exit(-1);
    }
    if(((unsigned short *)&a)[1] != 0x12fe){
        _exit(-2);
    }
    #else
    if(((unsigned short *)&a)[1] != 0xdc34){
        _exit(-1);
    }
    if(((unsigned short *)&a)[0] != 0xfe12){
        _exit(-2);
    }
    #endif
    _exit(0);
}
