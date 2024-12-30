# Otimização de Portfólio com Computação Quântica

## TL;DR
```
(env) python app.py --returns "A=0.4,B=0.55,C=0.45,D=0.6" --correlations "B-C=0.2,A-D=0.3" --budget 3 --max_investments 3
```
Este projeto utiliza a biblioteca Qiskit para resolver problemas de otimização de portfólio utilizando o algoritmo quântico **QAOA** (Quantum Approximate Optimization Algorithm). A execução do script recebe parâmetros da linha de comando, calcula o portfólio ótimo e exibe os resultados.

## Execução
1. Instale as dependências:

    ```Python 3.10.12```

    Em ambiente Conda, pode ser instalado com:

    ```bash
    conda create --name env python=3.10.12
    conda activate env
    ```

   ```bash
   pip install -r requirements.txt
   ```

2. Execução Básica:
```
(env) python app.py --returns "A=0.4,B=0.55,C=0.45,D=0.6" --correlations "B-C=0.2,A-D=0.3" --budget 3 --max_investments 3
```

### Entradas
O script ```app.py``` aceita os seguintes argumentos de linha de comando:

```--returns```: Retornos esperados dos ativos. Deve ser fornecido no formato ativo=valor, separado por vírgulas. Por exemplo, A=0.4,B=0.55,C=0.45 indica que os ativos A, B e C têm retornos esperados de 40%, 55% e 45%, respectivamente.

```--correlations```: Correlações entre pares de ativos. Deve ser fornecido no formato ativo1-ativo2=valor, separado por vírgulas. Por exemplo, B-C=0.2,A-D=-0.3 indica que os ativos B e C têm uma correlação de 0.2, enquanto A e D têm uma correlação de -0.3.

```--budget```: O número máximo de ações (ativos) que podem ser escolhidas no portfólio. Por exemplo, se budget=3, no máximo 3 ativos serão incluídos.

```--max_investments```: O número máximo de investimentos simultâneos permitidos. Por exemplo, se max_investments=3, no máximo 3 ativos podem ser investidos ao mesmo tempo.

### Saída

O script retorna uma solução no formato ```{'x_A': 1, 'x_B': 0, ...}```, onde:

```x_A = 1``` indica que o ativo A foi incluído no portfólio.
```x_B = 0``` indica que o ativo B não foi incluído no portfólio.

## Resumo da Teoria

### Otimização de Portfólio

A otimização de portfólio busca alocar recursos entre diferentes ativos de forma a maximizar os retornos esperados e minimizar os riscos, considerando restrições como orçamento e limite de investimentos simultâneos.

### Computação Quântica e QAOA

O QAOA é um algoritmo híbrido que combina computação clássica e quântica para resolver problemas de otimização combinatória. Ele é especialmente útil em problemas que podem ser formulados como um QUBO (Quadratic Unconstrained Binary Optimization).