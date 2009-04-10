#include <stdlib.h>

extern void _exit(int);

int main(){
    unsigned int a;
    ((unsigned char *)&a)[0] = 0x12;
    ((unsigned char *)&a)[1] = 0x34;
    ((unsigned char *)&a)[2] = 0x56;
    ((unsigned char *)&a)[3] = 0x78;
    if(a != 0x78563412){
        _exit(-1);
    }
    _exit(0);
}
