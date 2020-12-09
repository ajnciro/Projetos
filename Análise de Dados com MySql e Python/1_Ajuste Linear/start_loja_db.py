import mysql.connector
import numpy as np

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database = "lojasimples"
)
mycursor = mydb.cursor(buffered=True)
np.random.seed(101)

def limpa_base(true_or_false = False):
    """Redefine a Base de Dados"""
    
    if true_or_false:
    
        sql = "DELETE FROM venda"
        mycursor.execute(sql)
        sql = "DELETE FROM cliente"
        mycursor.execute(sql)
        sql = "DELETE FROM aquisicao"
        mycursor.execute(sql)
        sql = "DELETE FROM produto"
        mycursor.execute(sql)
        sql = "DELETE FROM departamento"
        mycursor.execute(sql)
        
        sql = "ALTER TABLE aquisicao AUTO_INCREMENT = 1"
        mycursor.execute(sql)
        sql = "ALTER TABLE cliente AUTO_INCREMENT = 1"
        mycursor.execute(sql)
        sql = "ALTER TABLE venda AUTO_INCREMENT = 1"
        mycursor.execute(sql)
        sql = "ALTER TABLE departamento AUTO_INCREMENT = 1"
        mycursor.execute(sql)
        sql = "ALTER TABLE produto AUTO_INCREMENT = 1"
        mycursor.execute(sql)

def configura_loja(margem_de_lucro):
    """Define os parâmetros da loja"""
   
    #-------------------------------------------
    # 1 - Insere os Clintes na base de dados
    
    while(1):
        ins = "INSERT INTO cliente (salarioCliente) VALUES({})".format(np.round(np.random.rand()*1000+500,2))
        val = ("")
        mycursor.execute(ins, val)
        mydb.commit()
        mycursor.execute("SELECT * FROM cliente")
    
        res = mycursor.fetchall()
    
        if len(res)>=50:
            break
    
    #-------------------------------------------
    #2 - Insere os departamentos da loja
            
    for x in range(1,16):
        ins = "INSERT INTO departamento () VALUES()"
        val = ("")
        mycursor.execute(ins, val)
        mydb.commit()
    
    #-------------------------------------------
    #3 - Insere os produtos no esstoque
    
    for x in range(0,250):
        custo = np.round(np.random.rand()*50+1,2)
        valor = custo*(1+margem_de_lucro)
        ins = "INSERT INTO produto (prodCusto, prodValor, prodEstoque, Departamento_idDepartamento)\
            VALUES({:.2f},{:.2f},{},{})".format(custo, valor, np.random.randint(20,70), np.random.randint(1,16))
        mycursor.execute(ins)
        mydb.commit()
    
    #--------------------------------------------
