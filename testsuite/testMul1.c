extern void _exit(int);

int
f1 ()
{
  unsigned long x, y = 1;

  x = ((y * 8192) - 216) % 16;
  return x;
}

int
main ()
{
  if (f1 () != 8)
    _exit (-1);
  _exit (0);
}
