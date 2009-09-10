#include <stdlib.h>

extern void _exit(int);

int main(){
    #ifndef BIG_TARGET
    unsigned int a[] = {0x9abcdeff, 0x12345678};
    #else
    unsigned int a[] = {0x12345678, 0x9abcdeff};
    #endif
    if(*((unsigned long long *)&a) != 0x123456789abcdeffLL){
        _exit(-1);
    }
    _exit(0);
}
