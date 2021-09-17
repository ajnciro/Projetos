import pandas as pd
from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer()
import warnings; warnings.simplefilter('ignore')
import pickle
import random
from funcoes import Alphabet, find_pos_2, fst_letter

#importação do modelo ajustado
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
