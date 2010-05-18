#include <stdlib.h>
#include <stdio.h>

int main(int argc, char * argv[]){
    register int i = 0, j = 0;

    /*Now I can disable BOTH caches*/
    asm("sethi %hi(0xfd800000), %g1");
    asm("or %g1,%lo(0xfd800000),%g1");
    asm("sethi %hi(0x80000014), %g2");
    asm("or %g2,%lo(0x80000014),%g2");
    asm("st %g1, [%g2]");

    //Increment var: argc++
    //Increment reg: j++ with j register variable (and making return j at the end, otherwise we optimize out)
    //just load: asm("ld [%sp], %g0");
    //just store: asm("st %g0, [%fp + 0x4c]");
    //sum vars: argc = argc + j; (j is volatile and not register)
    //mult: j *= (i + 1); with j register variable (and making return j at the end, otherwise we optimize out)
    //mult_const: j *= 11; with j register variable (and making return j at the end, otherwise we optimize out)
    //div: j /= (i + 1); with j register variable (and making return j at the end, otherwise we optimize out)
    //call: j = foo(); with j register variable (and making return j at the end, otherwise we optimize out)
    
    for(i = 0; i < 10000; i++){
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
         j /= (i + 1);
    }
    
    return j;
}