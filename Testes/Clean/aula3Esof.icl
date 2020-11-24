module aula3Esof
import StdEnv, StdArq

//Start = 2+3 ... #(Let-Faça) Notacao Zermelo Frankel
retornaListaPalavras 	st = StringtokensLst ['(',')',',','.',':','?','!',' ',';',toChar 13, toChar 10] st
retornaFrases 			st = StringtokensLst ['.','!','?'] st

Start comp 


#(conteudo, endereco, comp1)		= AbrirArquivoTextoExpl comp
//#conteudoTeste = conteudo +++ "   ESOF 2018"
//retornar todas as palavras do texto sem as pontuações
//#listaPalavras	=StringtokensLst [',','.',':','?','!',' ',';',toChar 13, toChar 10] conteudo
//= (conteudoTeste, '\n',endereco,'\n','\n',comp1)
//#listaPalavras = retornaListaPalavras conteudo

#listaFrases = retornaFrases conteudo
#listaPalavrasPorFrase = [retornaListaPalavras f\\ f<- listaFrases| (isMember "oi" (retornaListaPalavras f))&&(isMember "Cirao" (retornaListaPalavras f))]

= (listaPalavrasPorFrase,'\n',comp1)