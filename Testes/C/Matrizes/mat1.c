#include <stdio.h>
#include <stdlib.h>
#include "matriz.h"

int main() {
	Matriz A, adjA;
	int ord;
	printf("Entre com a ordem da matriz: ");
	scanf("%d", &ord);
	A = criarMatriz(ord, ord);
	preencherMatriz(A);
	imprimirMatriz(A);
	adjA = adjunta(A);
	printf("Adjunta:\n\n");
	imprimirMatriz(adjA);
	destruirMatriz(A);
	destruirMatriz(adjA);
	return EXIT_SUCCESS;
}
