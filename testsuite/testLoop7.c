#include <limits.h>

extern void _exit(int);

int n = 0;

g (i)
{
  n++;
}

f (m)
{
  int i;
  i = m;
  do
    {
      g (i * INT_MAX / 2);
    }
  while (--i > 0);
}

main ()
{
  f (4);
  if (n != 4)
    _exit (-1);
  _exit (0);
}
