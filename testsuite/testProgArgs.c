#include <stdlib.h>
#include <stdio.h>

int main(int argc, char * argv[]){
    if(argc != 1)
        return -1;
    if(argv[0][0] != 't')
        return -2;
    if(argv[0][1] != 'e')
        return -3;
    if(argv[0][2] != 's')
        return -4;
    if(argv[0][3] != 't')
        return -5;
    if(argv[0][4] != 'P')
        return -6;
    if(argv[0][5] != 'r')
        return -7;
    if(argv[0][6] != 'o')
        return -8;
    if(argv[0][7] != 'g')
        return -9;
    if(argv[0][8] != 'A')
        return -10;
    if(argv[0][9] != 'r')
        return -11;
    if(argv[0][10] != 'g')
        return -12;
    if(argv[0][11] != 's')
        return -13;
    return 0;
}