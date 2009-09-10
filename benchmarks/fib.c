
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

unsigned long fib(long);

unsigned long fib(x)
long x;
{
 if (x > 2)
  return(fib(x-1)+fib(x-2));
 else
  return(1);
}


int main()
{
 register unsigned long IMax,value;

 IMax = 30;//IMax = 40;

 printf("\n");
 printf("Fibonacci Benchmark\n");

 value = fib(IMax);

 printf("\n");
 printf("The %02d'th Fibonacci Number is: %d\n",IMax,value);
  return 0;
}
