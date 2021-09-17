import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import random
from unidecode import unidecode
import csv
from keras.preprocessing.text import Tokenizer
from sklearn.tree import DecisionTreeClassifier
import pickle
import warnings; warnings.simplefilter('ignore')


#Funções de manipulação de listas e strings

def pattern(leng):
    """retorna um padrão de __ quantas forem as letras em uma palavra"""
    
    string = ""
    for _ in range(leng):
        string+="__ "
    return string[:-1]

def lenn (patte):
    """comprimento de um padrão de __"""
    
    return len(patte.split(" "))

def simple_pattern(leng):
    """uma função auxiliar de padrão"""
    
    string = ""
    for _ in range(leng):
        string+="#"
    return string

def char_range(c1, c2):
    """um range de caracteres entre c1 e c2"""
    
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)
        
class Alphabet():
    """classe útil com atributos de um alfabeto"""
        
    def char_range (c1, c2):
        for c in range(ord(c1), ord(c2)+1):
            yield chr(c)
        
    def letra():
        lista_char = []
        for letra in char_range("A","Z"):
            if letra not in ['[', '\\', ']', '^', '_', '`']:
                lista_char.append(letra)
        return lista_char
    
    def vogais():
        return ['A','E','I','O','U']

def fst_letter():
    """primeira letra arriscada com mais de 50% de chances de retornar vogal"""
    
    if random.random()<0.5:
        return random.choice(Alphabet.vogais())
    else:
        return random.choice(Alphabet.letra())
    
def find_pos(carac,lis):
    """retorna a posição de um elemento em uma lista"""
    
    lis_pos=[]
    pos = 0
    for el in lis:
        if el == carac:
            lis_pos.append(pos)
        pos+=1
    return lis_pos

def find_pos_2(wor, ls):
    """retorna a posição de um elemento em uma lista. Mais eficiente"""
    
    return  [indx for indx in range(len(ls)) if wor== ls[indx]][0]

def list_replace(lis, lis_pos, item):
    """substitui um item em uma lista em determinada posição"""
    
    if len(lis)>=1:
        lis[lis_pos] = item
        return lis
    else:
        return []

def list_replace_all(lis, lis_pos, item):
    """substitui vários elementos em uma lista de acordo com suas posições"""
    
    if len(lis)>=1:
        return list(map(lambda v: list_replace(lis, v, item), lis_pos))[0]
    else:
        return []

def verifica_conj_let(strin):
    """retorna quais letras do alfabeto compõem determinada string"""
    
    ll = list(map(lambda v: v in strin.upper(), Alphabet.letra()))
    return ll

def arrisca_letra_2(palavra, letra, patt = "_"):
    """retorna se uma letra tentada está em uma palavra, e um padrão
    no tamanho da palavra com a posição substituida pela letra: 
        HOJE-> [TRUE, '__ __ __ __', '__ __ J __', J]"""
    
    acerto = False
    palavra = palavra.upper()
    letra = letra.upper()

    if patt == "_":
        patt = pattern(len(palavra))
    pat = patt
    split_pat = pat.split(" ")
    
    if True not in verifica_conj_let(pattern(len(palavra))):
           
        if letra in palavra:
            split_pat = list_replace_all(split_pat,find_pos(letra,palavra),letra)
            
            acerto = True
            pat = ' '.join(split_pat)
            

    #return[acerto, ' '.join(split_pat), conj_let]
    return [acerto, patt, pat, letra]

def unique(lis):
    """retorna elementos únicos em uma lista"""
    uni_lis = []
    for sub in lis:
        if sub not in uni_lis:
            uni_lis.append(sub)
    return uni_lis

def fill_word(palavra):
    """retorna uma lista com todas as combinações de tentativas de letras arriscadas
    e seus padrões"""
    
    alfabeto = Alphabet.letra()
    lst = list(map(lambda t: arrisca_letra_2(palavra, t, patt = "_"), alfabeto))
    lst2 = []
    n = 0
    while n<2:
        for elem in lst:
            for letra in alfabeto:
                arr = arrisca_letra_2(palavra, letra, patt = elem[-2])
                if(arr not in lst2):
                    lst2.append(arr)
        #lst2 = unique(lst2)
        lst = lst2
        
        n=n+1
    
    return lst2

def flatten (lst):
    """achata ou reduz a profundidade de aninhamento de uma matriz"""
    
    return [el for sub in lst for el in sub]

def replace_list(strin, pat, sub):
    """substitui um padrão regex por um padrão determinado"""
    for el in re.findall(pat, strin):
        strin = strin.replace(el, sub)
        
    return strin

def palavra_aleatoria():
    """escolhe uma palavra pseudoaleatoriamente em um banco de dados"""
    
    verb_df = pd.read_sql("SELECT palavra FROM verbetes", conn)[:500]
    return random.choice(verb_df['palavra'])

#------------------------------------------------------
#funções úteis para tratar um db SQLite

import sqlite3
#conn = sqlite3.connect('forca.db', check_same_thread=False)
conn = sqlite3.connect('hangman.db', check_same_thread=False) 
c = conn.cursor()

def create_table(tabela):
    c.execute('CREATE TABLE IF NOT EXISTS {}(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '\
              'palavra TEXT, comprimento INTEGER, descricao TEXT)'.format(tabela))
    
def data_insert(tab, word, comp, desc):
    c.execute("INSERT INTO {tab} (palavra, comprimento, descricao) VALUES(?, ?, ?)".format(tab = tab), (word, comp, desc))
    conn.commit()

    
def leitura_tabela(tab):
    c.execute("SELECT * FROM {}".format(tab))
    for linha in c.fetchall():
        print(linha) 

def limpa_tabela(tab):
    c.execute("DROP TABLE {}".format(tab))
    create_table(tab)
    
    
def close():
    c.close()
    conn.close()
    
#------------------------------------------------------
#importação do modelo preditivo

with open(r'pred_src/dtree2b.pickle', "rb") as file:
    dtree = pickle.load(file)
    file.close()
with open(r'pred_src/x_list2', "rb") as file:
    x_lst = pickle.load(file)
    file.close()
    
x = pd.read_pickle(r'pred_src/X2.pkl')

tokenizer = Tokenizer(lower = False, filters=' ', char_level=False, split=',')
tokenizer.fit_on_texts(x_lst)
tok1 = tokenizer.texts_to_sequences(x_lst)

def predict_letra(pat, preditas = []):
    """prediz a letra com base em um padrão existente, e.g '__ __ J __', 
    e num conjunto de tentativas anteriores [A, J]"""
    
    alp = Alphabet.letra()
    ls_return = []
    for letra in alp:
        array_test = pat+' {}'.format(letra)
        tok_pat = tokenizer.texts_to_sequences([array_test])
        try:
            if dtree.predict([x.loc[find_pos_2(tok_pat[0], tok1)]])[0] and letra not in preditas:
                ls_return.append(letra)
        except:
            continue
    if len(ls_return)==0:
        while True:
            letr = fst_letter()
            if letr not in pat:
                return fst_letter()
                break
    else:        
        return random.choice(ls_return) 
#-------------------------------------------------------