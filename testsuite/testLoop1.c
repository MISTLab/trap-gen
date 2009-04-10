/* Source: Neil Booth, from PR # 115.  */

int false()
{
  return 0;
}

extern void _exit(int);

int main (int argc,char *argv[])
{
  int count = 0;

  while (false() || count < -123)
    ++count;

  if (count)
    _exit(-1);

  _exit(0);
}
