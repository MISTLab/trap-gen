/* Test front-end conversions, optimizer conversions, and run-time
   conversions between different arithmetic types.

   Constants are specified in a non-obvious way to make them work for
   any word size.  Their value on a 32-bit machine is indicated in the
   comments.

   Note that this code is NOT intended for testing of accuracy of fp
   conversions.  */

extern void _exit(int);

float
u2f(u)
     unsigned int u;
{
  return u;
}

double
u2d(u)
     unsigned int u;
{
  return u;
}

long double
u2ld(u)
     unsigned int u;
{
  return u;
}

float
s2f(s)
     int s;
{
  return s;
}

double
s2d(s)
     int s;
{
  return s;
}

long double
s2ld(s)
     int s;
{
  return s;
}

int
fnear (float x, float y)
{
  float t = x - y;
  return t == 0 || x / t > 1000000.0;
}

int
dnear (double x, double y)
{
  double t = x - y;
  return t == 0 || x / t > 100000000000000.0;
}

int
ldnear (long double x, long double y)
{
  long double t = x - y;
  return t == 0 || x / t > 100000000000000000000000000000000.0;
}

test_integer_to_float()
{
  if (u2f(0U) != (float) 0U)                /* 0 */
    _exit(-1);
  if (!fnear (u2f(~0U), (float) ~0U))           /* 0xffffffff */
    _exit(-2);
  if (!fnear (u2f((~0U) >> 1), (float) ((~0U) >> 1)))   /* 0x7fffffff */
    _exit(-3);
  if (u2f(~((~0U) >> 1)) != (float) ~((~0U) >> 1))  /* 0x80000000 */
    _exit(-4);

  if (u2d(0U) != (double) 0U)               /* 0 */
    _exit(-5);
  if (!dnear (u2d(~0U), (double) ~0U))          /* 0xffffffff */
    _exit(-6);
  if (!dnear (u2d((~0U) >> 1),(double) ((~0U) >> 1)))   /* 0x7fffffff */
    _exit(-7);
  if (u2d(~((~0U) >> 1)) != (double) ~((~0U) >> 1)) /* 0x80000000 */
    _exit(-8);

  if (u2ld(0U) != (long double) 0U)         /* 0 */
    _exit(-9);
  if (!ldnear (u2ld(~0U), (long double) ~0U))       /* 0xffffffff */
    _exit(-10);
  if (!ldnear (u2ld((~0U) >> 1),(long double) ((~0U) >> 1)))    /* 0x7fffffff */
    _exit(-11);
  if (u2ld(~((~0U) >> 1)) != (long double) ~((~0U) >> 1))   /* 0x80000000 */
    _exit(-12);

  if (s2f(0) != (float) 0)              /* 0 */
    _exit(-13);
  if (!fnear (s2f(~0), (float) ~0))         /* 0xffffffff */
    _exit(-14);
  if (!fnear (s2f((int)((~0U) >> 1)), (float)(int)((~0U) >> 1))) /* 0x7fffffff */
    _exit(-15);
  if (s2f((int)(~((~0U) >> 1))) != (float)(int)~((~0U) >> 1)) /* 0x80000000 */
    _exit(-16);

  if (s2d(0) != (double) 0)             /* 0 */
    _exit(-17);
  if (!dnear (s2d(~0), (double) ~0))            /* 0xffffffff */
    _exit(-18);
  if (!dnear (s2d((int)((~0U) >> 1)), (double)(int)((~0U) >> 1))) /* 0x7fffffff */
    _exit(-19);
  if (s2d((int)~((~0U) >> 1)) != (double)(int)~((~0U) >> 1)) /* 0x80000000 */
    _exit(-20);

  if (s2ld(0) != (long double) 0)           /* 0 */
    _exit(-21);
  if (!ldnear (s2ld(~0), (long double) ~0))     /* 0xffffffff */
    _exit(-22);
  if (!ldnear (s2ld((int)((~0U) >> 1)), (long double)(int)((~0U) >> 1))) /* 0x7fffffff */
    _exit(-23);
  if (s2ld((int)~((~0U) >> 1)) != (long double)(int)~((~0U) >> 1)) /* 0x80000000 */
    _exit(-24);
}

#if __GNUC__
float
ull2f(u)
     unsigned long long int u;
{
  return u;
}

double
ull2d(u)
     unsigned long long int u;
{
  return u;
}

long double
ull2ld(u)
     unsigned long long int u;
{
  return u;
}

float
sll2f(s)
     long long int s;
{
  return s;
}

double
sll2d(s)
     long long int s;
{
  return s;
}

long double
sll2ld(s)
     long long int s;
{
  return s;
}

test_longlong_integer_to_float()
{
  if (ull2f(0ULL) != (float) 0ULL)          /* 0 */
    _exit(-25);
  if (ull2f(~0ULL) != (float) ~0ULL)            /* 0xffffffff */
    _exit(-26);
  if (ull2f((~0ULL) >> 1) != (float) ((~0ULL) >> 1))    /* 0x7fffffff */
    _exit(-27);
  if (ull2f(~((~0ULL) >> 1)) != (float) ~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-28);

  if (ull2d(0ULL) != (double) 0ULL)         /* 0 */
    _exit(-29);
#if __HAVE_68881__
  /* Some 68881 targets return values in fp0, with excess precision.
     But the compile-time conversion to double works correctly.  */
  if (! dnear (ull2d(~0ULL), (double) ~0ULL))       /* 0xffffffff */
    _exit(-30);
  if (! dnear (ull2d((~0ULL) >> 1), (double) ((~0ULL) >> 1))) /* 0x7fffffff */
    _exit(-31);
#else
  if (ull2d(~0ULL) != (double) ~0ULL)           /* 0xffffffff */
    _exit(-32);
  if (ull2d((~0ULL) >> 1) != (double) ((~0ULL) >> 1))   /* 0x7fffffff */
    _exit(-33);
#endif
  if (ull2d(~((~0ULL) >> 1)) != (double) ~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-34);

  if (ull2ld(0ULL) != (long double) 0ULL)       /* 0 */
    _exit(-35);
  if (ull2ld(~0ULL) != (long double) ~0ULL)     /* 0xffffffff */
    _exit(-36);
  if (ull2ld((~0ULL) >> 1) != (long double) ((~0ULL) >> 1)) /* 0x7fffffff */
    _exit(-37);
  if (ull2ld(~((~0ULL) >> 1)) != (long double) ~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-38);

  if (sll2f(0LL) != (float) 0LL)            /* 0 */
    _exit(-39);
  if (sll2f(~0LL) != (float) ~0LL)          /* 0xffffffff */
    _exit(-40);
  if (! fnear (sll2f((long long int)((~0ULL) >> 1)), (float)(long long int)((~0ULL) >> 1))) /* 0x7fffffff */
    _exit(-41);
  if (sll2f((long long int)(~((~0ULL) >> 1))) != (float)(long long int)~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-42);

  if (sll2d(0LL) != (double) 0LL)           /* 0 */
    _exit(-43);
  if (sll2d(~0LL) != (double) ~0LL)         /* 0xffffffff */
    _exit(-44);
  if (!dnear (sll2d((long long int)((~0ULL) >> 1)), (double)(long long int)((~0ULL) >> 1))) /* 0x7fffffff */
    _exit(-45);
  if (! dnear (sll2d((long long int)~((~0ULL) >> 1)), (double)(long long int)~((~0ULL) >> 1))) /* 0x80000000 */
    _exit(-46);

  if (sll2ld(0LL) != (long double) 0LL)         /* 0 */
    _exit(-47);
  if (sll2ld(~0LL) != (long double) ~0LL)       /* 0xffffffff */
    _exit(-48);
  if (!ldnear (sll2ld((long long int)((~0ULL) >> 1)), (long double)(long long int)((~0ULL) >> 1))) /* 0x7fffffff */
    _exit(-49);
  if (! ldnear (sll2ld((long long int)~((~0ULL) >> 1)), (long double)(long long int)~((~0ULL) >> 1))) /* 0x80000000 */
    _exit(-50);
}
#endif

unsigned int
f2u(float f)
{
  return (unsigned) f;
}

unsigned int
d2u(double d)
{
  return (unsigned) d;
}

unsigned int
ld2u(long double d)
{
  return (unsigned) d;
}

int
f2s(float f)
{
  return (int) f;
}

int
d2s(double d)
{
  return (int) d;
}

int
ld2s(long double d)
{
  return (int) d;
}

test_float_to_integer()
{
  if (f2u(0.0) != 0)
    _exit(-51);
  if (f2u(0.999) != 0)
    _exit(-52);
  if (f2u(1.0) != 1)
    _exit(-53);
  if (f2u(1.99) != 1)
    _exit(-54);
  if (f2u((float) ((~0U) >> 1)) != (~0U) >> 1 &&    /* 0x7fffffff */
      f2u((float) ((~0U) >> 1)) != ((~0U) >> 1) + 1)
    _exit(-55);
  if (f2u((float) ~((~0U) >> 1)) != ~((~0U) >> 1))  /* 0x80000000 */
    _exit(-56);

 /* These tests require double precision, so for hosts that don't offer
    that much precision, just ignore these test.  */
 if (sizeof (double) >= 8) {
  if (d2u(0.0) != 0)
    _exit(-57);
  if (d2u(0.999) != 0)
    _exit(-58);
  if (d2u(1.0) != 1)
    _exit(-59);
  if (d2u(1.99) != 1)
    _exit(-60);
  if (d2u((double) (~0U)) != ~0U)           /* 0xffffffff */
    _exit(-61);
  if (d2u((double) ((~0U) >> 1)) != (~0U) >> 1)     /* 0x7fffffff */
    _exit(-62);
  if (d2u((double) ~((~0U) >> 1)) != ~((~0U) >> 1)) /* 0x80000000 */
    _exit(-63);
 }

 /* These tests require long double precision, so for hosts that don't offer
    that much precision, just ignore these test.  */
 if (sizeof (long double) >= 8) {
  if (ld2u(0.0) != 0)
    _exit(-64);
  if (ld2u(0.999) != 0)
    _exit(-65);
  if (ld2u(1.0) != 1)
    _exit(-66);
  if (ld2u(1.99) != 1)
    _exit(-67);
  if (ld2u((long double) (~0U)) != ~0U)         /* 0xffffffff */
    _exit(-68);
  if (ld2u((long double) ((~0U) >> 1)) != (~0U) >> 1)   /* 0x7fffffff */
    _exit(-69);
  if (ld2u((long double) ~((~0U) >> 1)) != ~((~0U) >> 1))   /* 0x80000000 */
    _exit(-70);
 }

  if (f2s(0.0) != 0)
    _exit(-71);
  if (f2s(0.999) != 0)
    _exit(-72);
  if (f2s(1.0) != 1)
    _exit(-73);
  if (f2s(1.99) != 1)
    _exit(-74);
  if (f2s(-0.999) != 0)
    _exit(-75);
  if (f2s(-1.0) != -1)
    _exit(-76);
  if (f2s(-1.99) != -1)
    _exit(-77);
  if (f2s((float)(int)~((~0U) >> 1)) != (int)~((~0U) >> 1)) /* 0x80000000 */
    _exit(-78);

 /* These tests require double precision, so for hosts that don't offer
    that much precision, just ignore these test.  */
 if (sizeof (double) >= 8) {
  if (d2s(0.0) != 0)
    _exit(-79);
  if (d2s(0.999) != 0)
    _exit(-80);
  if (d2s(1.0) != 1)
    _exit(-81);
  if (d2s(1.99) != 1)
    _exit(-82);
  if (d2s(-0.999) != 0)
    _exit(-83);
  if (d2s(-1.0) != -1)
    _exit(-84);
  if (d2s(-1.99) != -1)
    _exit(-85);
  if (d2s((double) ((~0U) >> 1)) != (~0U) >> 1)     /* 0x7fffffff */
    _exit(-86);
  if (d2s((double)(int)~((~0U) >> 1)) != (int)~((~0U) >> 1)) /* 0x80000000 */
    _exit(-87);
 }

 /* These tests require long double precision, so for hosts that don't offer
    that much precision, just ignore these test.  */
 if (sizeof (long double) >= 8) {
  if (ld2s(0.0) != 0)
    _exit(-88);
  if (ld2s(0.999) != 0)
    _exit(-89);
  if (ld2s(1.0) != 1)
    _exit(-90);
  if (ld2s(1.99) != 1)
    _exit(-91);
  if (ld2s(-0.999) != 0)
    _exit(-92);
  if (ld2s(-1.0) != -1)
    _exit(-93);
  if (ld2s(-1.99) != -1)
    _exit(-94);
  if (ld2s((long double) ((~0U) >> 1)) != (~0U) >> 1)       /* 0x7fffffff */
    _exit(-95);
  if (ld2s((long double)(int)~((~0U) >> 1)) != (int)~((~0U) >> 1)) /* 0x80000000 */
    _exit(-96);
 }
}

#if __GNUC__
unsigned long long int
f2ull(float f)
{
  return (unsigned long long int) f;
}

unsigned long long int
d2ull(double d)
{
  return (unsigned long long int) d;
}

unsigned long long int
ld2ull(long double d)
{
  return (unsigned long long int) d;
}

long long int
f2sll(float f)
{
  return (long long int) f;
}

long long int
d2sll(double d)
{
  return (long long int) d;
}

long long int
ld2sll(long double d)
{
  return (long long int) d;
}

test_float_to_longlong_integer()
{
  if (f2ull(0.0) != 0LL)
    _exit(-97);
  if (f2ull(0.999) != 0LL)
    _exit(-98);
  if (f2ull(1.0) != 1LL)
    _exit(-99);
  if (f2ull(1.99) != 1LL)
    _exit(-100);
  if (f2ull((float) ((~0ULL) >> 1)) != (~0ULL) >> 1 &&  /* 0x7fffffff */
      f2ull((float) ((~0ULL) >> 1)) != ((~0ULL) >> 1) + 1)
    _exit(-101);
  if (f2ull((float) ~((~0ULL) >> 1)) != ~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-102);

  if (d2ull(0.0) != 0LL)
    _exit(-103);
  if (d2ull(0.999) != 0LL)
    _exit(-104);
  if (d2ull(1.0) != 1LL)
    _exit(-105);
  if (d2ull(1.99) != 1LL)
    _exit(-106);
  if (d2ull((double) ((~0ULL) >> 1)) != (~0ULL) >> 1 && /* 0x7fffffff */
      d2ull((double) ((~0ULL) >> 1)) != ((~0ULL) >> 1) + 1)
    _exit(-107);
  if (d2ull((double) ~((~0ULL) >> 1)) != ~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-108);

  if (ld2ull(0.0) != 0LL)
    _exit(-109);
  if (ld2ull(0.999) != 0LL)
    _exit(-110);
  if (ld2ull(1.0) != 1LL)
    _exit(-111);
  if (ld2ull(1.99) != 1LL)
    _exit(-112);
  if (ld2ull((long double) ((~0ULL) >> 1)) != (~0ULL) >> 1 &&   /* 0x7fffffff */
      ld2ull((long double) ((~0ULL) >> 1)) != ((~0ULL) >> 1) + 1)
    _exit(-113);
  if (ld2ull((long double) ~((~0ULL) >> 1)) != ~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-114);


  if (f2sll(0.0) != 0LL)
    _exit(-115);
  if (f2sll(0.999) != 0LL)
    _exit(-116);
  if (f2sll(1.0) != 1LL)
    _exit(-117);
  if (f2sll(1.99) != 1LL)
    _exit(-118);
  if (f2sll(-0.999) != 0LL)
    _exit(-119);
  if (f2sll(-1.0) != -1LL)
    _exit(-120);
  if (f2sll(-1.99) != -1LL)
    _exit(-121);
  if (f2sll((float)(long long int)~((~0ULL) >> 1)) != (long long int)~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-122);

  if (d2sll(0.0) != 0LL)
    _exit(-123);
  if (d2sll(0.999) != 0LL)
    _exit(-124);
  if (d2sll(1.0) != 1LL)
    _exit(-125);
  if (d2sll(1.99) != 1LL)
    _exit(-126);
  if (d2sll(-0.999) != 0LL)
    _exit(-127);
  if (d2sll(-1.0) != -1LL)
    _exit(-128);
  if (d2sll(-1.99) != -1LL)
    _exit(-129);
  if (d2sll((double)(long long int)~((~0ULL) >> 1)) != (long long int)~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-130);

  if (ld2sll(0.0) != 0LL)
    _exit(-131);
  if (ld2sll(0.999) != 0LL)
    _exit(-132);
  if (ld2sll(1.0) != 1LL)
    _exit(-133);
  if (ld2sll(1.99) != 1LL)
    _exit(-134);
  if (ld2sll(-0.999) != 0LL)
    _exit(-135);
  if (ld2sll(-1.0) != -1LL)
    _exit(-136);
  if (ld2sll(-1.99) != -1LL)
    _exit(-137);
  if (ld2sll((long double)(long long int)~((~0ULL) >> 1)) != (long long int)~((~0ULL) >> 1)) /* 0x80000000 */
    _exit(-138);
}
#endif

main()
{
  test_integer_to_float();
  test_float_to_integer();
#if __GNUC__
  test_longlong_integer_to_float();
  test_float_to_longlong_integer();
#endif
  _exit(0);
}
