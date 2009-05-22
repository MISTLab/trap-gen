#include <stdio.h>

#define TO_SORT_SIZE 8192

void QS(int[] ,int,int);
void swap(int[],int,int);
int main()
{
 int o;
 int a[TO_SORT_SIZE];
 for (o=0;o<TO_SORT_SIZE;o++)
  a[o]=rand()/128;
 QS(a,0,TO_SORT_SIZE - 1);
 return 0;
}

void QS(int v[], int left, int right)
{
 int i,last;
 if (left>=right) return;
 swap(v,left,(left+right)/2);
 last = left;
 for (i=left+1;i<=right;i++)
  if (v[i]<v[left]) swap(v,++last,i);
 swap(v,left,last);
 QS(v,left,last-1);
 QS(v,last+1,right);
}

void swap(int v[],int i, int j)
{
 int temp;
 temp=v[i];
 v[i]=v[j];
 v[j]=temp;
}
