extern void _exit(int);

int
foo (int x, int y, int i, int j)
{
  double tmp1 = ((double) x / y);
  double tmp2 = ((double) i / j);

  return tmp1 < tmp2;
}

int main ()
{
  if (foo (2, 24, 3, 4) == 0)
    _exit(1);
  _exit(0);
}
