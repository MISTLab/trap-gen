#include <stdlib.h>

extern void _exit(int);

int main(){
    unsigned int a[2];
    *((unsigned long long *)a) = 0x123456789abcdef1LL;
    if(a[0] != 0x9abcdef1){
        _exit(-1);
    }
    if(a[1] != 0x12345678){
        _exit(-1);
    }
    _exit(0);
}
