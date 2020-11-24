#include<stdio.h>

int main()
{
long int fib_1=1,fib_2=1,fib,i,n;
scanf("%d",&n);getchar();

for(i=1;i<n-1;fib=fib_1+fib_2,fib_2=fib_1,fib_1=fib,i++);
printf("\n%d\n, é",fib);

return 0;
}
