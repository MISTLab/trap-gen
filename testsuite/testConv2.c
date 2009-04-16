extern void _exit(int);

void f(long i)
{
  if ((signed char)i < 0 || (signed char)i == 0)
    _exit (-1);
  else
    _exit (0);
}

int main()
{
  f(0xffffff01);
}

