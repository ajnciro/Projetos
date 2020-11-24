#include<stdio.h>
#include<time.h>
#include<math.h>

void RandomIni(unsigned len)
{
    int ini[1000],k;
    for(k=0; k<len; k++)
    {
        ini[k]=rand()%2;
        printf("%d",ini[k]);
    }
}

int AdMod(int a,int b, int c)
{
    int d=a+b;
    if(d>=c)
        d=d-c;
    if(d<0)
        d=d+c;

    return d;
}

void DecToBin(int dec, int vec[])//Melhorar, está errado
{
    int r, i=0,j=0;
    while(dec>0)
    {
        r=dec%2;
        vec[i]=r;
        dec=dec/2;
        i++;
    }
    while(j<=i/2)
    {
        r=vec[j];
        vec[j]=vec[i-1-j];
        vec[i-1-j]=r;
        j++;
    }
}

void RevDecToBin(int dec, int vec[])
{
    int r, i=0;
    while(dec>0)
    {
        r=dec%2;
        vec[i]=r;
        dec=dec/2;
        i++;
    }
}

int Length(int vec[])
{
    int k=0;
    while(vec[k]<=9)
    {
        k++;
    }
    return k;
}

//void Automato(int regra, int ini[], int tem)
//{
//    int regrabin[8]=RevDecToBin(regra);
//    int,k,l,m;
//
//    for(k=0,k<);
//
//
//
//}


int main()
{
    int len, a, b, c,i=0,j;

    int v[1000]= {0},v2[1000];


    srand(time(0));

    printf("%d%\n\n",rand()%10);

    scanf("%d",&a);
    getchar();
    scanf("%d",&b);
    getchar();
    scanf("%d",&c);
    getchar();
    printf("\n\n%d\n\n",AdMod(a,b,c));

    DecToBin(43,v);
    while(i<6)
    {
        printf("%d",v[i]);
        i++;
    }

    printf("\n\n");
    j=0;

    RevDecToBin(43,v2);
    while(j<6)
    {
        printf("%d",v2[j]);
        j++;
    }

    printf("\n\n");


j=0;
while(j<8)
{
    int v3[3]={0};i=0;

    RevDecToBin(j,v3);
    while(i<3)
    {
        printf("%d",v3[i]);
        i++;
    }

    printf("\n\n");
j++;
}

int a[1000]={0,1,1};
int b;
b=Length(a);

 printf("\n\n%d",b);

    return 0;
}
