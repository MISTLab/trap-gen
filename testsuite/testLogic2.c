extern void _exit(int);

void func(int, int);

int main()
{
        int x = 7;
        func(!x, !7);
    _exit (0);
}

void func(int x, int y)
{
        if (x == y)
                return;
        else
                _exit(-1);
}
