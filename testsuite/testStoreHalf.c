#include <stdlib.h>

extern void _exit(int);

int main(){
    unsigned int a;
    ((unsigned short *)&a)[0] = 0x3412;
    ((unsigned short *)&a)[1] = 0x7856;
    if(a != 0x78563412){
        _exit(-1);
    }
    _exit(0);
}
