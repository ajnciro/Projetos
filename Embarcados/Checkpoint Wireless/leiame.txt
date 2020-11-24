	Os rascunhos presentes neste diretório dizem respeito a um conjunto de sensores de presença
que se comunicam sem fio.

	Possíveis aplicações incluem cronômetros de prova de robôs seguidores de linha, linhas de 
produção com estágios, detecção de rotas diversas etc.

	O objeto de atenção deste projeto é permitir que sensores standalone sejam posicionados a
distância, fornecendo maior capacidade modularidade, reparo, portabilidade e design do processo que
possa se desejar.

	A comunicação entre os sensores clientes e o servidor é feita via UDP entre módulos ESP8266. Tal protocolo, 
apesar da concepção não orientada à conexão, se mostrou confiável dentro do alcance do sinal WiFi além de exibir
comunicação desejavelmente rápida, com atrasos de propagação, transmissão e fila desprezíveis, e de processamento
aceitáveis em projetos que exigem dimensionamento sobre os clocks vigentes.

	Pelo próprio objetivo de ser um sistema portátil, a leitura e eventual arquisição dos dados gerados
é recomendada a um dispositivo móvel dotado de bluetooth, este servindo apenas para a transferência
de dados adquiridos pelo módulo servidor.


--
Ciro
(ciro@mail.org)