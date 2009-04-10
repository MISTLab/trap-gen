#include <stdlib.h>
#include <stdio.h>

#define CORRECT_SUM 561

int totalSum = 0;

int f33(){
    totalSum += 33;
    return 33;
}

int f32(){
    totalSum += 32;
    return f33() + 32;
}

int f31(){
    totalSum += 31;
    return f32() + 31;
}

int f30(){
    totalSum += 30;
    return f31() + 30;
}

int f29(){
    totalSum += 29;
    return f30() + 29;
}

int f28(){
    totalSum += 28;
    return f29() + 28;
}

int f27(){
    totalSum += 27;
    return f28() + 27;
}

int f26(){
    totalSum += 26;
    return f27() + 26;
}

int f25(){
    totalSum += 25;
    return f26() + 25;
}

int f24(){
    totalSum += 24;
    return f25() + 24;
}

int f23(){
    totalSum += 23;
    return f24() + 23;
}

int f22(){
    totalSum += 22;
    return f23() + 22;
}

int f21(){
    totalSum += 21;
    return f22() + 21;
}

int f20(){
    totalSum += 20;
    return f21() + 20;
}

int f19(){
    totalSum += 19;
    return f20() + 19;
}

int f18(){
    totalSum += 18;
    return f19() + 18;
}

int f17(){
    totalSum += 17;
    return f18() + 17;
}

int f16(){
    totalSum += 16;
    return f17() + 16;
}

int f15(){
    totalSum += 15;
    return f16() + 15;
}

int f14(){
    totalSum += 14;
    return f15() + 14;
}

int f13(){
    totalSum += 13;
    return f14() + 13;
}

int f12(){
    totalSum += 12;
    return f13() + 12;
}

int f11(){
    totalSum += 11;
    return f12() + 11;
}

int f10(){
    totalSum += 10;
    return f11() + 10;
}

int f9(){
    totalSum += 9;
    return f10() + 9;
}

int f8(){
    totalSum += 8;
    return f9() + 8;
}

int f7(){
    totalSum += 7;
    return f8() + 7;
}

int f6(){
    totalSum += 6;
    return f7() + 6;
}

int f5(){
    totalSum += 5;
    return f6() + 5;
}

int f4(){
    totalSum += 4;
    return f5() + 4;
}

int f3(){
    totalSum += 3;
    return f4() + 3;
}

int f2(){
    totalSum += 2;
    return f3() + 2;
}

int f1(){
    totalSum += 1;
    return f2() + 1;
}

int main(){
    int retVals = 0;

    retVals = f1();

    if(totalSum != CORRECT_SUM){
        fprintf(stderr, "Wrong totalSum value, %d\n", totalSum);
        return -1;
    }
    if(totalSum != retVals){
        fprintf(stderr, "Wrong return values: totalSum = %d -- retVals = %d\n", totalSum, retVals);
        return -1;
    }

    fprintf(stderr, "Test Correctly executed\n");

    return 0;
}
