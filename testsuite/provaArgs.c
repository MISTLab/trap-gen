#include <stdlib.h>
#include <stdio.h>

// This simple program tests the correctness of the command line
// arguments manchanisms

int main(int argc, char * argv[]){
    int i = 0;
    printf("There are %d arguments\n", argc);
    for(i = 0; i < argc; i++){
        printf("The %d-th argument is %s\n", i, argv[i]);
    }
    return 0;
}
