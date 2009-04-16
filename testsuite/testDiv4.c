extern void _exit(int);

int test1(char x)
{
  return x/100 == 3;
}

int test1u(unsigned char x)
{
  return x/100 == 3;
}

int test2(char x)
{
  return x/100 != 3;
}

int test2u(unsigned char x)
{
  return x/100 != 3;
}

int test3(char x)
{
  return x/100 < 3;
}

int test3u(unsigned char x)
{
  return x/100 < 3;
}

int test4(char x)
{
  return x/100 <= 3;
}

int test4u(unsigned char x)
{
  return x/100 <= 3;
}

int test5(char x)
{
  return x/100 > 3;
}

int test5u(unsigned char x)
{
  return x/100 > 3;
}

int test6(char x)
{
  return x/100 >= 3;
}

int test6u(unsigned char x)
{
  return x/100 >= 3;
}


int main()
{
  int c;

  for (c=-128; c<256; c++)
  {
    if (test1(c) != 0)
      _exit(-1);
    if (test1u(c) != 0)
      _exit(-2);
    if (test2(c) != 1)
      _exit(-3);
    if (test2u(c) != 1)
      _exit(-4);
    if (test3(c) != 1)
      _exit(-5);
    if (test3u(c) != 1)
      _exit(-6);
    if (test4(c) != 1)
      _exit(-7);
    if (test4u(c) != 1)
      _exit(-8);
    if (test5(c) != 0)
      _exit(-9);
    if (test5u(c) != 0)
      _exit(-10);
    if (test6(c) != 0)
      _exit(-11);
    if (test6u(c) != 0)
      _exit(-12);
  }
  _exit(0);
}

