/* +++Date last modified: 05-Jul-1997 */

/*
** rounding macros by Dave Knapp, Thad Smith, Jon Strayer, & Bob Stout
*/

#ifndef ROUND__H
#define ROUND__H

#include <math.h>

#if defined(__cplusplus) && __cplusplus

/*
** Safe C++ inline versions
*/

/* round to integer */

inline int iround(double x)
{
      return (int)floor(x + 0.5);
}

/* round number n to d decimal points */

inline double fround(double n, unsigned d)
{
      return floor(n * pow(10., d) + .5) / pow(10., d);
}

#else

/*
** NOTE: These C macro versions are unsafe since arguments are referenced
**       more than once.
**
**       Avoid using these with expression arguments to be safe.
*/

/*
** round to integer
*/

#define iround(x) floor((x) + 0.5)

/*
** round number n to d decimal points
*/

#define fround(n,d) (floor((n)*pow(10.,(d))+.5)/pow(10.,(d)))

#endif

#endif /* ROUND__H */
/* +++Date last modified: 05-Jul-1997 */

/*
**  SNIPTYPE.H - Include file for SNIPPETS data types and commonly used macros
*/

#ifndef SNIPTYPE__H
#define SNIPTYPE__H

#include <stdlib.h>                             /* For free()           */
#include <string.h>                             /* For NULL & strlen()  */

typedef enum {Error_ = -1, Success_, False_ = 0, True_} Boolean_T;

/*#if !defined(WIN32) && !defined(_WIN32) && !defined(__NT__) \
      && !defined(_WINDOWS)
      #if !defined(OS2)*/
  typedef unsigned char  BYTE;
  typedef unsigned long  DWORD;
/* #endif*/
 typedef unsigned short WORD;
/*#else
 #define WIN32_LEAN_AND_MEAN
 #define NOGDI
 #define NOSERVICE
 #undef INC_OLE1
 #undef INC_OLE2
 #include <windows.h>
 #define HUGE
 #endif*/

#define NUL '\0'
#define LAST_CHAR(s) (((char *)s)[strlen(s) - 1])
#define TOBOOL(x) (!(!(x)))
#define FREE(p) (free(p),(p)=NULL)

#endif /* SNIPTYPE__H */
/* +++Date last modified: 05-Jul-1997 */

/*
**  SNIPMATH.H - Header file for SNIPPETS math functions and macros
*/

#ifndef SNIPMATH__H
#define SNIPMATH__H

#include <math.h>

/*
**  Callable library functions begin here
*/

void    SetBCDLen(int n);                             /* Bcdl.C         */
long    BCDtoLong(char *BCDNum);                      /* Bcdl.C         */
void    LongtoBCD(long num, char BCDNum[]);           /* Bcdl.C         */
double  bcd_to_double(void *buf, size_t len,          /* Bcdd.C         */
                      int digits);
int     double_to_bcd(double arg, char *buf,          /* Bcdd.C         */
                      size_t length, size_t digits );
DWORD   ncomb1 (int n, int m);                        /* Combin.C       */
DWORD   ncomb2 (int n, int m);                        /* Combin.C       */
void    SolveCubic(double a, double b, double c,      /* Cubic.C        */
                  double d, int *solutions,
                  double *x);
DWORD   dbl2ulong(double t);                          /* Dbl2Long.C     */
long    dbl2long(double t);                           /* Dbl2Long.C     */
double  dround(double x);                             /* Dblround.C     */

/* Use #defines for Permutations and Combinations     -- Factoryl.C     */

#define log10P(n,r) (log10factorial(n)-log10factorial((n)-(r)))
#define log10C(n,r) (log10P((n),(r))-log10factorial(r))

double  log10factorial(double N);                     /* Factoryl.C     */

double  fibo(unsigned short term);                    /* Fibo.C         */
double  frandom(int n);                               /* Frand.C        */
double  ipow(double x, int n);                        /* Ipow.C         */
int     ispow2(int x);                                /* Ispow2.C       */
long    double ldfloor(long double a);                /* Ldfloor.C      */
int     initlogscale(long dmax, long rmax);           /* Logscale.C     */
long    logscale(long d);                             /* Logscale.C     */

float   MSBINToIEEE(float f);                         /* Msb2Ieee.C     */
float   IEEEToMSBIN(float f);                         /* Msb2Ieee.C     */
int     perm_index (char pit[], int size);            /* Perm_Idx.C     */
int     round_div(int n, int d);                      /* Rnd_Div.C      */
long    round_ldiv(long n, long d);                   /* Rnd_Div.C      */
double  rad2deg(double rad);                          /* Rad2Deg.C      */
double  deg2rad(double deg);                          /* Rad2Deg.C      */

/* +++Date last modified: 05-Jul-1997 */

#ifndef PI__H
#define PI__H

#ifndef PI
 #define PI         (4*atan(1))
#endif

#define deg2rad(d) ((d)*PI/180)
#define rad2deg(r) ((r)*180/PI)

#endif /* PI__H */

#ifndef PHI
 #define PHI      ((1.0+sqrt(5.0))/2.0)         /* the golden number    */
 #define INV_PHI  (1.0/PHI)                     /* the golden ratio     */
#endif

/*
**  File: ISQRT.C
*/

struct int_sqrt {
      unsigned sqrt,
               frac;
};

void usqrt(unsigned long x, struct int_sqrt *q);


#endif /* SNIPMATH__H */

#include <math.h>
#include <stdlib.h>

void SolveCubic(double  a,
                double  b,
                double  c,
                double  d,
                int    *solutions,
                double *x)
{
      long double    a1 = b/a, a2 = c/a, a3 = d/a;
      long double    Q = (a1*a1 - 3.0*a2)/9.0;
      long double R = (2.0*a1*a1*a1 - 9.0*a1*a2 + 27.0*a3)/54.0;
      double    R2_Q3 = R*R - Q*Q*Q;

      double    theta;

      if (R2_Q3 <= 0)
      {
            *solutions = 3;
            theta = acos(R/sqrt(Q*Q*Q));
            x[0] = -2.0*sqrt(Q)*cos(theta/3.0) - a1/3.0;
            x[1] = -2.0*sqrt(Q)*cos((theta+2.0*PI)/3.0) - a1/3.0;
            x[2] = -2.0*sqrt(Q)*cos((theta+4.0*PI)/3.0) - a1/3.0;
      }
      else
      {
            *solutions = 1;
            x[0] = pow(sqrt(R2_Q3)+fabs(R), 1/3.0);
            x[0] += Q/x[0];
            x[0] *= (R < 0.0) ? 1 : -1;
            x[0] -= a1/3.0;
      }
}

/* +++Date last modified: 05-Jul-1997 */

#include <string.h>

#define BITSPERLONG 32

#define TOP2BITS(x) ((x & (3L << (BITSPERLONG-2))) >> (BITSPERLONG-2))


/* usqrt:
    ENTRY x: unsigned long
    EXIT  returns floor(sqrt(x) * pow(2, BITSPERLONG/2))

    Since the square root never uses more than half the bits
    of the input, we use the other half of the bits to contain
    extra bits of precision after the binary point.

    EXAMPLE
        suppose BITSPERLONG = 32
        then    usqrt(144) = 786432 = 12 * 65536
                usqrt(32) = 370727 = 5.66 * 65536

    NOTES
        (1) change BITSPERLONG to BITSPERLONG/2 if you do not want
            the answer scaled.  Indeed, if you want n bits of
            precision after the binary point, use BITSPERLONG/2+n.
            The code assumes that BITSPERLONG is even.
        (2) This is really better off being written in assembly.
            The line marked below is really a "arithmetic shift left"
            on the double-long value with r in the upper half
            and x in the lower half.  This operation is typically
            expressible in only one or two assembly instructions.
        (3) Unrolling this loop is probably not a bad idea.

    ALGORITHM
        The calculations are the base-two analogue of the square
        root algorithm we all learned in grammar school.  Since we're
        in base 2, there is only one nontrivial trial multiplier.

        Notice that absolutely no multiplications or divisions are performed.
        This means it'll be fast on a wide range of processors.
*/

void usqrt(unsigned long x, struct int_sqrt *q)
{
      unsigned long a = 0L;                   /* accumulator      */
      unsigned long r = 0L;                   /* remainder        */
      unsigned long e = 0L;                   /* trial product    */

      int i;

      for (i = 0; i < BITSPERLONG; i++)   /* NOTE 1 */
      {
            r = (r << 2) + TOP2BITS(x); x <<= 2; /* NOTE 2 */
            a <<= 1;
            e = (a << 1) + 1;
            if (r >= e)
            {
                  r -= e;
                  a++;
            }
      }
      memcpy(q, &a, sizeof(long));
}

#include <math.h>

/* The printf's may be removed to isolate just the math calculations */

int main(void)
{
  double  a1 = 1.0, b1 = -10.5, c1 = 32.0, d1 = -30.0;
  double  x[3];
  double X;
  int     solutions;
  int i;
  unsigned long l = 0x3fed0169L;
  struct int_sqrt q;
  long n = 0;

  /* solve soem cubic functions */
  printf("********* CUBIC FUNCTIONS ***********\n");
  /* should get 3 solutions: 2, 6 & 2.5   */
  SolveCubic(a1, b1, c1, d1, &solutions, x);  
  printf("Solutions:");
  for(i=0;i<solutions;i++)
    printf(" %f",x[i]);
  printf("\n");

  a1 = 1.0; b1 = -4.5; c1 = 17.0; d1 = -30.0;
  /* should get 1 solution: 2.5           */
  SolveCubic(a1, b1, c1, d1, &solutions, x);  
  printf("Solutions:");
  for(i=0;i<solutions;i++)
    printf(" %f",x[i]);
  printf("\n");

  a1 = 1.0; b1 = -3.5; c1 = 22.0; d1 = -31.0;
  SolveCubic(a1, b1, c1, d1, &solutions, x);
  printf("Solutions:");
  for(i=0;i<solutions;i++)
    printf(" %f",x[i]);
  printf("\n");

  a1 = 1.0; b1 = -13.7; c1 = 1.0; d1 = -35.0;
  SolveCubic(a1, b1, c1, d1, &solutions, x);
  printf("Solutions:");
  for(i=0;i<solutions;i++)
    printf(" %f",x[i]);
  printf("\n");

  a1 = 3.0; b1 = 12.34; c1 = 5.0; d1 = 12.0;
  SolveCubic(a1, b1, c1, d1, &solutions, x);
  printf("Solutions:");
  for(i=0;i<solutions;i++)
    printf(" %f",x[i]);
  printf("\n");

  a1 = -8.0; b1 = -67.89; c1 = 6.0; d1 = -23.6;
  SolveCubic(a1, b1, c1, d1, &solutions, x);
  printf("Solutions:");
  for(i=0;i<solutions;i++)
    printf(" %f",x[i]);
  printf("\n");

  a1 = 45.0; b1 = 8.67; c1 = 7.5; d1 = 34.0;
  SolveCubic(a1, b1, c1, d1, &solutions, x);
  printf("Solutions:");
  for(i=0;i<solutions;i++)
    printf(" %f",x[i]);
  printf("\n");

  a1 = -12.0; b1 = -1.7; c1 = 5.3; d1 = 16.0;
  SolveCubic(a1, b1, c1, d1, &solutions, x);
  printf("Solutions:");
  for(i=0;i<solutions;i++)
    printf(" %f",x[i]);
  printf("\n");

  /* Now solve some random equations */
  for(a1=1;a1<10;a1+=1) {
    for(b1=10;b1>0;b1-=.25) {
      for(c1=5;c1<15;c1+=0.61) {
	   for(d1=-1;d1>-5;d1-=.451) {
		SolveCubic(a1, b1, c1, d1, &solutions, x);  
		printf("Solutions:");
		for(i=0;i<solutions;i++)
		  printf(" %f",x[i]);
		printf("\n");
	   }
      }
    }
  }


  printf("********* INTEGER SQR ROOTS ***********\n");
  /* perform some integer square roots */
  for (i = 0; i < 100000; i+=2)
    {
      usqrt(i, &q);
			// remainder differs on some machines
     // printf("sqrt(%3d) = %2d, remainder = %2d\n",
     printf("sqrt(%3d) = %2d\n",
	     i, q.sqrt);
    }
  printf("\n");
  for (l = 0x3fed0169L; l < 0x3fed4169L; l++)
    {
	 usqrt(l, &q);
	 //printf("\nsqrt(%lX) = %X, remainder = %X\n", l, q.sqrt, q.frac);
	 printf("sqrt(%lX) = %X\n", l, q.sqrt);
    }


  printf("********* ANGLE CONVERSION ***********\n");
  /* convert some rads to degrees */
/*   for (X = 0.0; X <= 360.0; X += 1.0) */
  for (X = 0.0; X <= 360.0; X += .001)
    printf("%3.0f degrees = %.12f radians\n", X, deg2rad(X));
  puts("");
/*   for (X = 0.0; X <= (2 * PI + 1e-6); X += (PI / 180)) */
  for (X = 0.0; X <= (2 * PI + 1e-6); X += (PI / 5760))
    printf("%.12f radians = %3.0f degrees\n", X, rad2deg(X));
  
  
  return 0;
}

