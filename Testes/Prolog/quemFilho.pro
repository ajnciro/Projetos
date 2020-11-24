domains

nome=symbol.
pai=symbol.
filho=symbol.
cpf=integer.
salario=integer.
estado_civil=symbol.

predicates

nondeterm pai(symbol, symbol).
nondeterm pai(nome).
nondeterm cliente(symbol, integer, integer, integer, symbol).






clauses

%submeta: nao eh a meta, eh algo que deve ser provado para que a meta eja verdadeira (uma das condicoes do predicado)
% meta - o que se deseja prova
%corte: mecanismo de controle do backtracking, ou mecanismo de controle do fluxo de programa. Símb cut = :-!



pai(luciano, thales).
pai(luciano, tatiana).
%pai(luciano, tatiana):-!. corte
pai(lucas, maria_laura).

pai(joaquim, daniel).

pai(lucas).
pai(joaquim).

cliente(luciano, 11111, 57, 12000, casado).

goal

pai(luciano, Filho).
