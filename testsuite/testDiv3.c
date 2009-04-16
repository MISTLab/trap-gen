/* PR middle-end/17894 */

extern void _exit(int);

int test1(int x)
{
  return x/-10 == 2;
}

int test2(int x)
{
  return x/-10 == 0;
}

int test3(int x)
{
  return x/-10 != 2;
}

int test4(int x)
{
  return x/-10 != 0;
}

int test5(int x)
{
  return x/-10 < 2;
}

int test6(int x)
{
  return x/-10 < 0;
}

int test7(int x)
{
  return x/-10  <= 2;
}

int test8(int x)
{
  return x/-10 <= 0;
}

int test9(int x)
{
  return x/-10 > 2;
}

int test10(int x)
{
  return x/-10 > 0;
}

int test11(int x)
{
  return x/-10 >= 2;
}

int test12(int x)
{
  return x/-10 >= 0;
}


int main()
{
  if (test1(-30) != 0)
    _exit(-1);
  if (test1(-29) != 1)
    _exit(-2);
  if (test1(-20) != 1)
    _exit(-3);
  if (test1(-19) != 0)
    _exit(-4);

  if (test2(0) != 1)
    _exit(-5);
  if (test2(9) != 1)
    _exit(-6);
  if (test2(10) != 0)
    _exit(-7);
  if (test2(-1) != 1)
    _exit(-8);
  if (test2(-9) != 1)
    _exit(-9);
  if (test2(-10) != 0)
    _exit(-10);

  if (test3(-30) != 1)
    _exit(-11);
  if (test3(-29) != 0)
    _exit(-12);
  if (test3(-20) != 0)
    _exit(-13);
  if (test3(-19) != 1)
    _exit(-14);

  if (test4(0) != 0)
    _exit(-15);
  if (test4(9) != 0)
    _exit(-16);
  if (test4(10) != 1)
    _exit(-17);
  if (test4(-1) != 0)
    _exit(-18);
  if (test4(-9) != 0)
    _exit(-19);
  if (test4(-10) != 1)
    _exit(-20);

  if (test5(-30) != 0)
    _exit(-21);
  if (test5(-29) != 0)
    _exit(-22);
  if (test5(-20) != 0)
    _exit(-23);
  if (test5(-19) != 1)
    _exit(-24);

  if (test6(0) != 0)
    _exit(-25);
  if (test6(9) != 0)
    _exit(-26);
  if (test6(10) != 1)
    _exit(-27);
  if (test6(-1) != 0)
    _exit(-28);
  if (test6(-9) != 0)
    _exit(-29);
  if (test6(-10) != 0)
    _exit(-30);

  if (test7(-30) != 0)
    _exit(-31);
  if (test7(-29) != 1)
    _exit(-32);
  if (test7(-20) != 1)
    _exit(-33);
  if (test7(-19) != 1)
    _exit(-34);

  if (test8(0) != 1)
    _exit(-35);
  if (test8(9) != 1)
    _exit(-36);
  if (test8(10) != 1)
    _exit(-37);
  if (test8(-1) != 1)
    _exit(-38);
  if (test8(-9) != 1)
    _exit(-39);
  if (test8(-10) != 0)
    _exit(-40);

  if (test9(-30) != 1)
    _exit(-41);
  if (test9(-29) != 0)
    _exit(-42);
  if (test9(-20) != 0)
    _exit(-43);
  if (test9(-19) != 0)
    _exit(-44);

  if (test10(0) != 0)
    _exit(-45);
  if (test10(9) != 0)
    _exit(-46);
  if (test10(10) != 0)
    _exit(-47);
  if (test10(-1) != 0)
    _exit(-48);
  if (test10(-9) != 0)
    _exit(-49);
  if (test10(-10) != 1)
    _exit(-50);

  if (test11(-30) != 1)
    _exit(-51);
  if (test11(-29) != 1)
    _exit(-52);
  if (test11(-20) != 1)
    _exit(-53);
  if (test11(-19) != 0)
    _exit(-54);

  if (test12(0) != 1)
    _exit(-55);
  if (test12(9) != 1)
    _exit(-56);
  if (test12(10) != 0)
    _exit(-57);
  if (test12(-1) != 1)
    _exit(-58);
  if (test12(-9) != 1)
    _exit(-59);
  if (test12(-10) != 1)
    _exit(-60);

  _exit(0);
}
