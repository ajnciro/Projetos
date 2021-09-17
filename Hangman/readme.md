# Um robô preditor de letras

Este projeto teve como objetivo treinar um robô para jogar o clássico jogo da forca (hangman).

O intuito seria que adivinhasse as letras na palavra sem análise contextual, apenas conhecendo o número de letras e as eventuais posições das mesma dentro do verbete e, ainda, com um sistema implícito de backtracking gerado por aprendizagem com Árvores de Decisão..

Outros algoritmos classificatórios se mostraram acurados, porém sem tanta eficiência dado o desenho do banco de dados.

[![Class Report and Conf Matrix](https://github.com/ajnciro/Projetos/blob/main/Hangman/static/eficiencia_modelo.jpg "Class Report and Conf Matrix")](https://github.com/ajnciro/Projetos/blob/main/Hangman/static/eficiencia_modelo.jpghttp:// "Class Report and Conf Matrix")


## Composição dos scripts
Em dois scripts principalmente pode-se encontar o funcionamento do robô, em *hangman.py* para interação em CLI:


        while True:
            letra = f.predict_letra(bot.padrao, bot.letras_tentadas)
            if letra not in bot.letras_tentadas:
                break
        bot.letras_tentadas.append(letra) 
        bot_res = f.arrisca_letra_2(tit,letra, bot.padrao)
        bot.padrao = bot_res[-2]
        if not bot_res[0]:
            bot.erros+=1

e em *app3.py* com um serviço em Flask:


	class Jogador:
   		 def __init__(self, letras_tentadas = [], padrao = "_", erros = 0, nome = ""):
		 
	(...)
	
	@app.route("/<string:name>/jogar")
	def jogar(name):
	
	(...)
	
	    try:
        inp_humano = ch

        hum_res = f.arrisca_letra_2(tit,inp_humano, humano.padrao)
        humano.padrao = hum_res[-2]
        if hum_res[0] is not True:
	(...)
	
	
Um banco de dados SQLite foi escolhido para armazenar os vebetes coletados da Wikipédia via Web Scraping, script contido em *coleta_verbetes.py*:


    try:
        with f.urllib.request.urlopen("https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria") as url:
            page = url.read()
            soup = f.BeautifulSoup(page, "html.parser")
            try:
                sp = soup.p.get_text()
	
	(...)
	
		 tit = f.re.split(sep, soup.title.string)[0]
        strin = f.replace_list(sp, '(?=\[).+?(?<=\])', '')
	
	(...)
	
E um MongoDB foi selecionado para armazenar os valores que serviriam ao processamento dos DataFrames pela máquina em *mongo_feed.py* e *ajuste_modelo.py*:


	conn = MongoClient('localhost', 27017)
	db = conn.forca_ia
	collection = db.verbetes
	(...)
	df = pd.DataFrame(list(collection.find()))
	df =  df[:500]
	lis = [el for el in flatten(df['fill_word']) if el[-1] not in el[1] if "_" in el[1]]
	df2 = pd.DataFrame(lis, columns = ["isTrue", "bef_pattern", "aft_pattern", "letter_choice"])
	y = df2['isTrue']
	x = [df2['bef_pattern'].iloc[lin]+", "+df2['letter_choice'].iloc[lin] for lin in range(len(y))]
	(...)
	dtree = DecisionTreeClassifier()
	dtree.fit(X_train, Y_train)
	dtree_pred = dtree.predict(X_test)
	
E a função preditiva propriamente dita está definita em *modelo_preditivo.py*:


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
		

por fim no arquivo *funcoes.py* será encontrada um módulo com uma variade de funções auxiliares para o funcionamento do projeto:


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
		
	(...)
	
	def find_pos_2(wor, ls):
    """retorna a posição de um elemento em uma lista. Mais eficiente"""
    
    return  [indx for indx in range(len(ls)) if wor== ls[indx]][0]
