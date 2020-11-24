module aula2Esof

import StdEnv

//Start = 2+3

dobro x = 2*x
quadruplo x = dobro (dobro x)

//Start = quadruplo 9

f x = x
//Start = [f x\\x<-[0..100]|x rem 11==0||x^3==4*x]
//Start = [3*x\\ x<-[0..100]|not(isEven x)]

convListaPVetor :: [Int]->{Int}
convListaPVetor lt = {x\\x<-lt}
//Start = convListaPVetor [1,2,3,4,5]

convVetorPLista :: {Int}->[Int]
convVetorPLista v = [x\\x<-:v]
//Start = convVetorPLista {1,2,3,4,5}

convVetorEstPNaoEst :: {#Char}-> {Char}
convVetorEstPNaoEst v = {x\\x<-:v}
Start = convVetorEstPNaoEst "ciro"
//{'c','i','r','o'}