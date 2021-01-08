import mysql.connector
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

diret = "C:/Users/sucod/OneDrive/Lenovo/Documentos/Sql/"

#-----------------------------------------------
#--------- Configura máquina SVM ---------------

df = pd.DataFrame(columns = [], index = [])
df2 = pd.DataFrame(columns = [], index = [])

#--Para os dados coletados com lucros variando de 0 a 390%
for percent in range (0,391,10):
    df_aux = pd.read_csv(r"{}".format(diret)+"/CSVLoja3/produto_{}.csv".format(percent))
    df_aux["lucroPercent"] = percent
    df = pd.concat([df, df_aux],ignore_index=True)

for percent in range (0,391,10):           
    df_aux = pd.read_csv(r"{}".format(diret)+"/CSVLoja3/aquisicao_{}.csv".format(percent))
    for ID in range (1,251):
        count = 0
        for prodID in df_aux["Produto_idProduto"]:
            if prodID == ID:
                count+=1
        if count == 0:
            nova_linha = {'Produto_idProduto':ID, 'Quantidade':0} 
            df_aux = df_aux.append(nova_linha,ignore_index=True)

    df_aux = df_aux.groupby("Produto_idProduto").mean()       
    df2 = pd.concat([df2, df_aux["Quantidade"]],ignore_index=True)
    
del df['Unnamed: 0']
del df['idProduto'] 
del df['prodEstoque']
del df['Departamento_idDepartamento']

df["aquiMed"] = df2.to_numpy()
df_produto = df

# A variável alvo da aprendizagem será uma intersecção entre um lucro maior que 5000 com vendas
# maiores que 500. Portanto, as duas condições simultaneamente serão o alvo:
df_produto["isLucro"]=(df_produto["prodLucro"]>5000)&(df_produto["prodVendas"]>500)

X = df.drop(['isLucro','prodGanhoAcum','prodVendas','prodCustoAcum','prodValor','prodGanhoAcum','prodLucro'], axis = 1)
Y = df['isLucro']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
model = SVC(C = 1000, gamma = 0.001, kernel = 'rbf')    #parâmetros otimizados
model.fit(X_train, Y_train)

def max_lucro_min_aq(varcusto):
    """" Determina o máximo lucro predefino com o mínimo custo acumulado por
    estoque de produto. O argumento será o custo de aquisição do produto.
    Como ambas as condições devem ser satisfeitas simultaneamente, pode-se
    começar a busca pela condição a partir do maior lucro e o mínimo custo
    estará contido"""
        
    x = 390
    while x>1:
        aqui = 1
        while aqui<150:
            cond = model.predict(pd.DataFrame(data={'prodCusto': [varcusto], 'lucroPercent': [x], 'aquiMed': [aqui]}))[0]
            if cond!=False:     #A precisão do modelo foi maior para detectar falsos (não-lucros) do que verdadeiros
                return [x,aqui]
                break
            aqui+=1
        x-=1
        if x == 1:
                return [1,1]


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
list_aq = []
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
    
    for x in range(1,251):#251
        custo = np.round(np.random.rand()*50+1,2)
        valor = custo*(1+(max_lucro_min_aq(custo))[0]/100)
        estoque = (max_lucro_min_aq(custo))[1]
        list_aq.append([x,estoque])
        ins = "INSERT INTO produto (prodCusto, prodValor, prodEstoque, Departamento_idDepartamento)\
            VALUES({:.2f},{:.2f},{},{})".format(custo, valor, estoque+20, np.random.randint(1,16))
        mycursor.execute(ins)
        mydb.commit()
    
    #--------------------------------------------
    #Exporta a lista com os lucros percentuais que devem ser colocados em cada produto
    #Preferível para melhor o desempenho das transações.
        
    pd.DataFrame(list_aq).to_csv(r'C:\Users\sucod\OneDrive\Lenovo\Documentos\Sql\CSVLojaSVM3\list_aq.csv')