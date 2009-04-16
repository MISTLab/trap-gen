#include <stdlib.h>

extern void _exit(int);

int main(){
    char * a = "abcd";
    if(a[0] != 'a'){
        _exit(-1);
    }
    if(a[1] != 'b'){
        _exit(-2);
    }
    if(a[2] != 'c'){
        _exit(-3);
    }
    if(a[3] != 'd'){
        _exit(-4);
    }
    _exit(0);
}
