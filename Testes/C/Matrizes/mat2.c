#include <stdio.h>
#include <stdlib.h>
#include "matriz.h"

int main() {
	Matriz A;
	double det;
	int ord;
	printf("Entre com a ordem da matriz: ");
	scanf("%d", &ord);
	A = criarMatriz(ord, ord);
	preencherMatriz(A);
	imprimirMatriz(A);
	det = determinante(A);
	printf("Determinante: %.00f\n\n",det);
	destruirMatriz(A);
	return EXIT_SUCCESS;
}
