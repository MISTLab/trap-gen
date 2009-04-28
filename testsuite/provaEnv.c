#include <stdlib.h>
#include <stdio.h>

// This simple program tests the correctness of the command line
// arguments manchanisms

int main(int argc, char * argv[]){
    int i = 0;

    printf("The env ONE is -%s-\n", getenv("ONE"));
    printf("The env TWO is -%s-\n", getenv("TWO"));
    if(getenv("THREE") == NULL){
        printf("Not found THREE");
    }
    else{
        printf("Found THREE");
    }

    return 0;
}
