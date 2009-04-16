#include <stdlib.h>

extern void _exit(int);

int main(){
    unsigned long long a = 0x123456789abcdef1LL;
    if(a != 0x123456789abcdef1LL){
        _exit(-1);
    }
    _exit(0);
}
