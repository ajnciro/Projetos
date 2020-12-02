# Análise do DB de uma loja simples com Python

Este projeto se refere a uma análise preliminar do banco de dados de uma loja simples utilizando algumas ferramentas de Data Science.

No primeiro momento, foi criado um comércio fictício automatizado com Python para manipular um banco de dados MySQL.

O DER do banco e o script com o design que se julgou necessário e suficiente, estão na pasta Banco de Dados, de acordo com a imagem:

[![DER](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/Banco%20de%20Dados/DER_LojaSimples.png "DER")](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/Banco%20de%20Dados/DER_LojaSimples.pnghttp:// "DER")

A automatização da das transações é feita a partir do script em "fluxo_loja_toCSV.py" que faz o start do DB por meio do programa em  "start_loja_db", como uma importação de módulo, e exporta as tabelas MySQL para CSV dentro da pasta CSVLoja.

```python
import mysql.connector
import numpy as np

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database = "lojasimples"
)
mycursor = mydb.cursor(buffered=True)
```

E atenção aos parâmetros do banco de dados.

Esses dois programas por si só realizam as transações necessárias, inserem os preços dos produtos, as vendas por cliente, departamento, manipulam o orçamento dos clientes etc., mas contam com alguns poucos triggers inseridos no script sql para ajudar na manipulação do banco.

A rotina em "fluxo_loja_toCSV.py" (que depende da importação de "start_loja_db"), realiza, essencialmente, um conjunto compras de 3 produtos distintos por clientes, com no máximo 4 unidades de cada. Essa compra depende de um orçamento preestabelecido de 30% da remuneração do indivíduo, tudo gerado pseudoaleatoriamente. Se o valor da compra não estiver dentro do orçamento, ela não será realizada. A cada 5 ciclos de compras (pode-se entender como 1 compra por semana, 5 semanas seguidas) bem-sucedidas ou malsucedidas, o orçamento é restaurado ao padrão.

Tanto o preço dos produtos, como a remuneração e orçamento, e as quantidades compradas, e a reposição de estoque são inseridos com gerador de pseudoaleatórios em intervalos determinados.

A cada 2000 ciclos de transações de 5 "semanas" cada, com 50 clientes comprando 250 produtos distintos de 15 departamentos diferentes, um arquivo de valores separados por vírgula CSV é gerado e exportado, então ocorre um incremento no valor do lucro percentual dos produtos.

[![DF](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/0.png "DF")](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/0.pnghttp:// "DF")

No princípio, este lucro começa em 10% com relação ao custo que a loja tem para adquirir o produto e varia até 81% de 1 em 1%.

[![PairPlot](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/1.png "PairPlot")](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/1.pnghttp:// "PairPlot")

A rotina em "fluxo_loja_toCSV2.py" (que depende da importação de "start_loja_db"), faz o mesmo trabalho, porém com o lucro percentual variando de 10 em 10% até 300%, a fim de se obter um alcance de dados maior. E exporta os mesmos para CSVLoja2.

Essas duas rotinas correspondem ao notebooks Jupyter "1_Loja_DF.ipynb" e "2_Loja_DF.ipynb"

[![PairPlot](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/2.png "PairPlot")](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/2.png http:// "PairPlot")

Já o script em "fluxo_loja_toCSV_Optm.py" (o qual depende da importação de "start_loja_db_Optm.py"), refere-se ao conjunto de transações na loja quando o lucro estabelecido que um produto deve obter não é constante e igual ao dos demais, mas ajustado de acordos com as otimizações vistas em "3_Loja_DF.ipynb", que, no fim, tratar-se-ia de um modelo de otimização do negócio em si.

Dentro de "3_Loja_DF.ipynb" há referências a procedimentos realizados em Wolfram Mathematica (ajuste de distribuição log-normal e função racional), cujos notebooks foram exportados para PDF para fins de eventual impossibilidade na leitura dos códigos.

[![Fit](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/3.png "Fit")](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/3.pnghttp:// "Fit")

[![Mathematica](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/4.png "Mathematica")](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/4.pnghttp:// "Mathematica")

De modo geral, como conclusão sobre a análise dos dados gerados pela loja fictícia automatizada, estão as observações:

- Lucros excessivos diminuem a quantidade de vendas e lucro absoluto total;

- Também diminuem o custo médio por departamento, provavelmente como consequência da não necessária frequência de reposição do estoque por menos vendas;

- Lucros percentuais demasiado pequenos também não sustem o lucro final de um comércio;

- Ajustes individuais dos lucros por produto, de acordo com o preço de custo, são mais eficientes que uma mesma margem para todos os itens, para a maioria das faixas de lucro percentual observadas (para mais que 75% dos casos).

[![Graph](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/5.png "Graph")](https://github.com/ajnciro/Projetos/blob/main/Análise%20de%20Dados%20com%20MySql%20e%20Python/.ipynb_checkpoints/5.pnghttp:// "Graph")