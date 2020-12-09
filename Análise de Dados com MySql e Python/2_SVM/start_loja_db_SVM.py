import mysql.connector
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

folder = "C:/Users/sucod/OneDrive/Lenovo/Documentos/Sql/"

#-----------------------------------------
df = pd.DataFrame(columns = [], index = [])

for percent in range (10,301,10):
    df_aux = pd.read_csv(r"{}".format(folder)+"/CSVLoja2/produto_{}.csv".format(percent))
    df_aux["lucroPercent"] = percent
    df = pd.concat([df, df_aux],ignore_index=True)    
del df['Unnamed: 0']
del df['idProduto'] 
del df['prodEstoque']
del df['Departamento_idDepartamento']

df["isLucro"]=df["prodLucro"]>5000

X = df.drop(['isLucro','prodGanhoAcum','prodVendas','prodCustoAcum','prodValor','prodGanhoAcum','prodLucro'], axis = 1)
Y = df['isLucro']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
model = SVC(C= 1, gamma= 0.01, kernel= 'rbf')
model.fit(X_train, Y_train)

def max_lucro(varcusto):
    """" Determina o máximo lucro predefino apenas como sendo maior que 5000 sem
    considerar os custos com reosição do estoque, variando o lucro percentual, de
    1 a 300%. """
    
    luc = 1
    while luc<301:
        cond = model.predict(pd.DataFrame(data={'prodCusto': [varcusto], 'lucroPercent': [luc]}))[0]
        if cond:
            return luc
            break
        luc+=1
        if luc == 300:
            return 300


#--------------------------------------------------
#--- Inicia loja ---
            
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database = "lojasimples"
)
mycursor = mydb.cursor(buffered=True)
np.random.seed(101)

def lucro(var_val):
    """ Função antiga de determinação do lucro de acordo com o ajuste da curva"""
    return 5280.186/(var_val + 2.076)-100.932

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

def configura_loja():
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
        valor = custo*(1+max_lucro(custo)/100)
        ins = "INSERT INTO produto (prodCusto, prodValor, prodEstoque, Departamento_idDepartamento)\
            VALUES({:.2f},{:.2f},{},{})".format(custo, valor, np.random.randint(20,70), np.random.randint(1,16))
        mycursor.execute(ins)
        mydb.commit()
    
    #--------------------------------------------
