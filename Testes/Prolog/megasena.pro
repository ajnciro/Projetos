

predicates

nondeterm menu()
nondeterm s_n(Char,string)

clauses

menu():-

	write("1 - Entre com um nome:"," Nome:-> "),nl,
	readln(Nome),
	write("Deseja sortear um jogo da Mega Sena?:\n","s/n :-> "),
	readchar(SimOuNao),nl,
	s_n(SimOuNao,Nome).
s_n('s',Nome):-!, random(60,Sorteio1),
	  random(60,Sorteio2),
	  random(60,Sorteio3),
	  random(60,Sorteio4),
	  random(60,Sorteio5),
	  random(60,Sorteio6),
	  
	  write("------------------------------"),nl,
	  write(Nome," o seu palpite da sorte é: "),
	  write("Seu palpite da sorte é: ",Sorteio1,"-",Sorteio2,"-",Sorteio3,"-",
	  Sorteio4,"-",Sorteio5,"-",Sorteio6,"-"),nl,
	  write("BOA SORTE!!!\n").
s_n(_,Nome):-!, write("\nQUE PENA...\n").

goal

menu().