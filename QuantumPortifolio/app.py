# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:30:32 2024

@author:    Ciro
            ciro@mail.org        
"""

import argparse
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA
from qiskit import Aer

def optimize_portfolio(returns:dict, correlations:dict, budget:int, max_investments:int)->dict:
    """
    Otimiza um portfólio de investimentos usando QAOA.

    Parâmetros:
        returns (dict): Retornos esperados das ações, e.g., {'A': 0.4, 'B': 0.55, 'C': 0.45}.
        correlations (dict): Correlações entre pares de ações, e.g., {('B', 'C'): 0.2}.
        budget (int): Número máximo de ações que podem ser escolhidas.
        max_investments (int): Número máximo de investimentos simultâneos permitidos.

    Retorna:
        dict: Decisões de investimento otimizadas.
    """
    qp = QuadraticProgram()

    # Definir variáveis binárias para cada ativo
    variables = {}
    for stock in returns:
        variables[stock] = qp.binary_var(name=f"x_{stock}")

    qp.minimize(linear={f"x_{k}": -v for k, v in returns.items()},
                quadratic={(f"x_{k1}", f"x_{k2}"): v for (k1, k2), v in correlations.items()})

    qp.linear_constraint({f"x_{k}": 1 for k in returns}, "<=", budget, "budget_constraint")
    qp.linear_constraint({f"x_{k}": 1 for k in returns}, "<=", max_investments, "max_investments_constraint")

    backend = Aer.get_backend('aer_simulator')
    qaoa = QAOA(reps=1, quantum_instance=backend)
    optimizer = MinimumEigenOptimizer(qaoa)

    result = optimizer.solve(qp)

    return result.variables_dict

def main():
    parser = argparse.ArgumentParser(description="Otimização de Portfólio com Computação Quântica")
    parser.add_argument("--returns", type=str, required=True,
                        help="Retornos esperados no formato: A=0.4,B=0.55,C=0.45")
    parser.add_argument("--correlations", type=str, required=True,
                        help="Correlações no formato: A-B=0.3,B-C=0.2")
    parser.add_argument("--budget", type=int, required=True, help="Orçamento máximo (número de ações).")
    parser.add_argument("--max_investments", type=int, required=True, help="Número máximo de investimentos.")

    args = parser.parse_args()

    returns = {item.split('=')[0]: float(item.split('=')[1]) for item in args.returns.split(',')}

    # Processar correlações
    correlations = {}
    for pair in args.correlations.split(','):
        stocks, value = pair.split('=')
        stock1, stock2 = stocks.split('-')
        correlations[(stock1, stock2)] = float(value)

    solution = optimize_portfolio(returns, correlations, args.budget, args.max_investments)

    print("Solução encontrada:", solution)

if __name__ == "__main__":
    main()