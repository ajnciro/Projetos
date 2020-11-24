module recursividadeEficiente
import StdEnv, StdArq

//Start = 2+3 ... #(Let-Faça) Notacao Zermelo Frankel
retornaListaPalavras 	st = StringtokensLst ['(',')',',','.',':','?','!',' ',';',toChar 13, toChar 10] st
retornaFrases 			st = StringtokensLst ['.','!','?'] st
//função

/*
retornaListaPalavrasPorFraseTexto txt pal = [retornaListaPalavras f\\ f<- (retornaFrases txt)| isMember pal (retornaListaPalavras f)]

contaElList lst = contaElListAux lst 0
contaElListAux lst resultado
|lst == [] = resultado
|otherwise = contaElListAux (tl lst) (resultado+1)

Start = contaElList [1,2,2,3,4,5]
*/

/*
Start comp 


#(conteudo, endereco, comp)		= AbrirArquivoTextoExpl comp
#conteudoTeste =  "   ESOF 2018" +++ conteudo
//retornar todas as palavras do texto sem as pontuações
//#listaPalavras	=StringtokensLst [',','.',':','?','!',' ',';',toChar 13, toChar 10] conteudo
//= (conteudoTeste, '\n',endereco,'\n','\n',comp1)
//#listaPalavras = retornaListaPalavras conteudo

//#listaFrases = retornaFrases conteudo
//#listaPalavrasPorFrase = retornaListaPalavrasPorFraseTexto conteudo "oi"

# (enderecoGravado, comp)	= GravarArqTextoExpl (conteudoTeste, comp)
= (enderecoGravado,'\n',comp)



fat n = if (n==0)
			1
			(n*(fat(n-1)))
			
Start = fat 5



fatG n
|n==0 =1
|n>0 = n*(fatG(n-1))
 
Start = fatG 100
*/

//INTEIRO GRANDE
/*
fatEfic n = fatEficAux n 1

fatEficAux n resultado
|n==0 = resultado // condição de parada (n==0) e a regra de parada ->1
|otherwise = fatEficAux (n-1) (resultado*n)

Start = fatEfic 5

*/

//Ver biblioteca

/*
fatBigInt n = fatBigInteAux (toBigInt n)
fatBigInteAux nBig resultado
|nBig== (toBigInt 0) = toString resultado
|otherwise = fatBigInteAux (nBig-(toBigInt 1)) (resultado*nBig)

Start = fatBigInt 5
*/

PorPFra

|"casa" 	= "maison"
|"lar"		= "lar"
|"carro"	= "voiture"
|"banana"	= "banane"
|"eu"		= "je"
|"fui"		= "suis allé"
|"e"		= "et"
