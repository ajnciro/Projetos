

predicates

nondeterm menu()
clauses

menu():-

	write("1 - Entre com um nome:"," Nome:-> "),nl,
	readln(Nome),
	write("2 - Entre com um valor de 0 a 1000:\n","    Valor:->"),
	readint(Numero),
	random(Numero,NR),
	write(Nome,", seu numero da sorte é: ", NR,"!"),nl.

goal

menu().