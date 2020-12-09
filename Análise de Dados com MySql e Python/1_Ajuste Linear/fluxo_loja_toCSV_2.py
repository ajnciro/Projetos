import mysql.connector
import numpy as np
import pandas as pd
import random
import start_loja_db as stl

lucro = 10
for x in range (10,301,10):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="1234",
      database = "lojasimples"
    )
    mycursor = mydb.cursor(buffered=True)


    print("Aguarde um instante...\n\n")
    stl.limpa_base(True)
    stl.configura_loja(lucro/100)
    print("Iniciando vendas... {}\n\n".format(lucro))
    
    
    """Compra se estoque é baixo"""
    #------------------------------
    
    def repoe_estoque(minimo):
    
        query="SELECT idProduto FROM produto WHERE prodEstoque<={}".format(minimo)
        mycursor.execute(query)
    
        df = pd.read_sql(query, mydb)
    
        for prod_id in np.array(df.values).flatten():
            ins_aq = "INSERT INTO aquisicao (Quantidade, Produto_idProduto)\
                VALUES({},{})".format(np.random.randint(minimo,150), \
                  prod_id)
    
            mycursor.execute(ins_aq)
            mydb.commit()
    
    
    """ Insere Venda """    
    #-------------------------------
    
    def insere_vendas():
        
        for rand_cliente in range (1,51):
            sample = random.sample(range(1,251),3)
    
            #rand_cliente = cliente
            rand_prod1 = sample[0]
            rand_quant1 = np.random.randint(1,5)
            rand_prod2 = sample[1]
            rand_quant2 = np.random.randint(1,5)
            rand_prod3 = sample[2]
            rand_quant3 = np.random.randint(1,5)    
            
            #-----------------
            query_salario = "SELECT salarioCliente FROM cliente WHERE idCliente = {}".format(rand_cliente)
            salario_cliente_df = pd.read_sql(query_salario, mydb)
            salario_cliente = np.array(salario_cliente_df.to_numpy()).flatten()[0]
            
            query_gastos = "SELECT gastoCliente FROM cliente WHERE idCliente = {}".format(rand_cliente)
            gasto_cliente_df = pd.read_sql(query_gastos, mydb)
            gasto_cliente = np.array(gasto_cliente_df.to_numpy()).flatten()[0]
            
            cliente_orcamento = salario_cliente*0.3 - gasto_cliente
            #-----------------
            
            #-----------------
            query = "SELECT idProduto,prodValor,Departamento_idDepartamento,prodLucro FROM produto WHERE idProduto = {}".format(rand_prod1)
            valor1_df = pd.read_sql(query, mydb).to_numpy().flatten()
            
            query = "SELECT idProduto,prodValor,Departamento_idDepartamento,prodLucro FROM produto WHERE idProduto = {}".format(rand_prod2)
            valor2_df = pd.read_sql(query, mydb).to_numpy().flatten()
            
            query = "SELECT idProduto,prodValor,Departamento_idDepartamento,prodLucro FROM produto WHERE idProduto = {}".format(rand_prod3)
            valor3_df = pd.read_sql(query, mydb).to_numpy().flatten()
            
            #-----------------
            venda_valor=rand_quant1*valor1_df[1]+rand_quant2*valor2_df[1]+rand_quant3*valor3_df[1]
    
            if(venda_valor<=cliente_orcamento):
                ins = "INSERT INTO venda (Cliente_idCliente, Produto_idProduto, Quantidade, vendaValor,Departamento,prodLucro) \
                    VALUES({},{},{},{},{},{})"\
                    .format(rand_cliente,rand_prod1, rand_quant1,\
                            rand_quant1*valor1_df[1],valor1_df[2],valor1_df[3])
                mycursor.execute(ins)
                #mydb.commit()
    
    
                ins = "INSERT INTO venda (Cliente_idCliente, Produto_idProduto, Quantidade, vendaValor, Departamento,prodLucro) \
                    VALUES({},{},{},{},{},{})"\
                    .format(rand_cliente,rand_prod2, rand_quant2,\
                            rand_quant2*valor2_df[1],valor2_df[2],valor2_df[3])
                mycursor.execute(ins)
                #mydb.commit()
    
                ins = "INSERT INTO venda (Cliente_idCliente, Produto_idProduto, Quantidade, vendaValor, Departamento,prodLucro)\
                    VALUES({},{},{},{},{},{})"\
                    .format(rand_cliente,rand_prod3, rand_quant3,\
                            rand_quant3*valor3_df[1],valor3_df[2],valor3_df[3])
                mycursor.execute(ins)
    
                mydb.commit()
    
          
            
    """Redefine orçamento a cada n ciclos"""
    #------------------------------
    def reset_orcamento():
        query_orc = "UPDATE cliente SET gastoCliente = 0"
        mycursor.execute(query_orc)
        mydb.commit()
        
    
    #------------------------------
        
    #------------------------------
    def atualiza_departamento():
        for depId in range(1,16):
            query_custo = "SELECT prodCustoAcum FROM produto where Departamento_idDepartamento = {}".format(depId)
            df_custo = pd.read_sql(query_custo, mydb).to_numpy().sum()
            query_custo = "UPDATE departamento SET depCusto = {} where idDepartamento = {}".format(df_custo, depId)
            mycursor.execute(query_custo)
            
            query_ganho = "SELECT prodGanhoAcum FROM produto where Departamento_idDepartamento = {}".format(depId)
            df_ganho = pd.read_sql(query_ganho, mydb).to_numpy().sum()
            query_ganho = "UPDATE departamento SET depGanho = {} where idDepartamento = {}".format(df_ganho, depId)
            mycursor.execute(query_ganho)
            
            df_lucro = df_ganho-df_custo
            query_lucro = "UPDATE departamento SET depLucro = {} where idDepartamento = {}".format(df_lucro, depId)
            mycursor.execute(query_lucro)
        
            mydb.commit()
            
    #---------------------------
    n=0
    count = 0
    while count<2000: 
        repoe_estoque(20)
        insere_vendas()
        atualiza_departamento()
        
        if n==5:
            reset_orcamento()
            n=0
        n+=1
        count+=1
        print(count)
        
    query_save="SELECT * FROM venda"
    df_save = pd.read_sql(query_save, mydb)
    df_save.to_csv(r'C:\Users\sucod\OneDrive\Lenovo\Documentos\Sql\CSVLoja2\venda_{}.csv'.format(lucro))
    
    query_save="SELECT * FROM produto"
    df_save = pd.read_sql(query_save, mydb)
    df_save.to_csv(r'C:\Users\sucod\OneDrive\Lenovo\Documentos\Sql\CSVLoja2\produto_{}.csv'.format(lucro))
    
    query_save="SELECT * FROM departamento"
    df_save = pd.read_sql(query_save, mydb)
    df_save.to_csv(r'C:\Users\sucod\OneDrive\Lenovo\Documentos\Sql\CSVLoja2\departamento_{}.csv'.format(lucro))
    
    print("Arquivos Salvos -- {}".format(lucro))
    lucro+=10