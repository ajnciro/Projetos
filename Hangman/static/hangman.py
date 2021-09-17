import funcoes as f
import os

class Jogador:
    def __init__(self, letras_tentadas, padrao, erros):
        self.letras_tentadas = letras_tentadas
        self.padrao = padrao
        self.erros = erros
        
    def monta_boneco(self):
        return {1: "cabeça",
                2:"braço direito",
                3: "braço esquerdo",
                4: "perna direita",
                5: "perna esquerda",
                0: "forca"
            }[self.erros]

super_controle = 'continua'
while super_controle == 'continua':
    #-----------------------------------------------------------------------------
    #Faz uma consulta na Wikipédia de um verbete aleatório, retorna sua descrição
    #e oculta a palavra no texto
    
    tit = f.palavra_aleatoria()
    with f.urllib.request.urlopen("https://pt.wikipedia.org/wiki/{}".format(tit)) as url:
            page = url.read()
            soup = f.BeautifulSoup(page, "html.parser")
            
    ss = soup.find_all('p')
    if len(ss)>1:
        ss = ss[1].get_text()
    elif len(ss)==1:
        ss = ss[0].get_text()
    else:
        ss = ''
        
    str = f.replace_list(ss, '(?=\[).+?(?<=\])', '')
    str = str.replace(tit,f.pattern(len(tit)))
    print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n\n", str)
    
    
    #-----------------------------------------------------------------------------
    #Define dois jogadores, o Bot e o Humano
    
    patt = f.pattern(len(tit))
    bot = Jogador([], patt, 0)
    humano = Jogador([], patt, 0)
    
    controle = ""
    while controle !='parar':
        
        print("\n== Bot está pensando... ==\n")
        
        #Aqui o Bot faz a jogada com base no modelo preditivo e aguarda a jogada
        #do humano até uma condição de 5 erros ou empate
        
        while True:
            letra = f.predict_letra(bot.padrao, bot.letras_tentadas)
            if letra not in bot.letras_tentadas:
                break
        bot.letras_tentadas.append(letra) 
        bot_res = f.arrisca_letra_2(tit,letra, bot.padrao)
        bot.padrao = bot_res[-2]
        if not bot_res[0]:
            bot.erros+=1
        try:
            inp_humano = input('Escreva "parar" para interromper o jogo ou escolha uma letra:\n')
            if inp_humano.upper() == 'PARAR':
                super_controle = 'parar'
                break
    
            hum_res = f.arrisca_letra_2(tit,inp_humano, humano.padrao)
            humano.padrao = hum_res[-2]
            if hum_res[0] is not True:
                humano.erros+=1
        except: print("\nTente uma letra do alfabeto. Bot não perdeu sua vez!")
        
        print("\nResposta Bot: ","Bot Acertou! - Erros = {}\n".format(bot.erros) if bot_res[0] \
              else "Bot errou... - Erros = {}\n".format(bot.erros))
        #print(bot.monta_boneco())
        
        print("\nSua Resposta: - ", hum_res[-1], ": Correto!" if hum_res[0] else "Incorreto...", hum_res[-2],\
              " - Erros: {}".format(humano.erros),"\n")
        #print(humano.monta_boneco())
        
        if bot.erros ==5 and bot.erros > humano.erros or ('_' not in humano.padrao and '_' in bot.padrao):
            print('Você ganhou!\nSua palavra: {}. A reposta correta é: {})'.format(hum_res[-2], tit))
            break
        elif humano.erros == 5 and humano.erros > bot.erros or ('_' in humano.padrao and '_' not in bot.padrao):
            print('Você perdeu...\nSua palavra: {}. A reposta correta é: {}\n'.format(hum_res[-2], tit))
            break
        elif humano.erros == 5 and bot.erros == 5 or ('_' not in humano.padrao and '_' not in bot.padrao):
            print('Empate.\nSua palavra: {}. A reposta correta é: {}\n)'.format(hum_res[-2], tit))
            break
        
        if inp_humano == 'parar':
            controle = 'parar'
            
            os.system('cls')
    
       # os.system('cls' if os.name == 'nt' else 'clear')