#include<stdio.h>

#define N 64

int menu()
{
    printf("=====\n\n");
    int opc;
    do
    {
        fprintf(stdout, "1 - Informar\n");
        fprintf(stdout, "2 - Resgatar\n");
        fprintf(stdout, "3 - Sair\n\n");

        fscanf(stdin, "%d",&opc);
    }while(opc!=1&&opc!=2&&opc!=3);
    return opc;
}
void informar()
{
    FILE * arquivo;
    char nome[N]; int idade; float altura;
    arquivo =fopen("info.txt", "w");
    printf("Entre com o primeiro nome: ");
    scanf("%s", nome);
    printf("Entre com a idade [somente anos]: ");
    scanf("%d",&idade);
    printf("Entre com a altura [em metros]: ");
    scanf("%f",&altura);

    arquivo=fopen("info.txt","a");

    fprintf(arquivo, "%s\n%d\t%f\n", nome, idade, altura);
    fclose(arquivo);
}

void resgatar()
{
    FILE * arquivo;
    char nome[N]; int idade; float altura;
    arquivo =fopen ("info.txt", "r");

    fscanf(arquivo, "%s\n%d\t%f\n", nome, &idade, &altura);//é necessário fazer o scan da maneira como foi formatado
    fclose(arquivo);
    fprintf(stdout,"\n===\n%s\n%d anos\n%g metros\n",nome, idade, altura);
}

int main()
{
    int opc;
    do{
        opc=menu();
        if(opc==1) informar();
        if(opc==2) resgatar();
    }while(opc!=3);
}
