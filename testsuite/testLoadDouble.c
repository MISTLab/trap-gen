#include <stdlib.h>

extern void _exit(int);

int main(){
    unsigned int a[] = {0x12345678, 0x9abcdeff};
    if(*((unsigned long long *)&a) != 0x123456789abcdeffLL){
        _exit(-1);
    }
    _exit(0);
}
