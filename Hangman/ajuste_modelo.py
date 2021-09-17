import pandas as pd
from pymongo import MongoClient
from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer()
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
#import warnings; warnings.simplefilter('ignore')
import pickle

def flatten (lst):
    """achata ou reduz a profundidade de aninhamento de uma matriz"""
    
    return [el for sub in lst for el in sub]

#Conexão ao DB NoSQL
conn = MongoClient('localhost', 27017)
db = conn.forca_ia
collection = db.verbetes

#Tratamento do DB em um DataFrame
df = pd.DataFrame(list(collection.find()))
df =  df[:500]
lis = [el for el in flatten(df['fill_word']) if el[-1] not in el[1] if "_" in el[1]]
df2 = pd.DataFrame(lis, columns = ["isTrue", "bef_pattern", "aft_pattern", "letter_choice"])
#df2 = df2[:150000]

#y é a variável que se deseja prever, ou seja, o acerto ou erro de um 'chute'
#com base em x, que é o padrão de mesmo tamanho da palavra com letras ocultas
y = df2['isTrue']
x = [df2['bef_pattern'].iloc[lin]+", "+df2['letter_choice'].iloc[lin] for lin in range(len(y))]

with open("x_list2", "wb") as file:
    pickle.dump(x, file)
    file.close()

#tokeninzando a variável dependente para não necessitar trabalhar com dummies
tokenizer = Tokenizer(lower = False, filters=' ', char_level=False, split=',')
tokenizer.fit_on_texts(x)
tok1 = tokenizer.texts_to_sequences(x)
tok_df = pd.DataFrame(data = tok1).fillna(0.0)

y.to_pickle('Y2.pkl')
tok_df.to_pickle('X2.pkl')

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size = 0.3)

#Árvores de Decisão se mostrou o modelo de ML mais adequado para o problema
dtree = DecisionTreeClassifier()
dtree.fit(X_train, Y_train)
dtree_pred = dtree.predict(X_test)
print(classification_report(Y_test, dtree_pred))
print('\n')
print(confusion_matrix(Y_test, dtree_pred))

#salvando o modelo altamente eficiente
with open("dtree2b.pickle", "wb") as file:
    pickle.dump(dtree, file)
    file.close()
print ("Modelo salvo.")