"""Este é o app Flask que servirá à geração da página HTML do jogo
aos moldes da aplicação original em hangman.py. Descrições gerais
do funcionamento do jogo já estão contidas em hangman.py"""

import funcoes as f
from flask import Flask, render_template, request, redirect, session
from waitress import serve
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Jogador:
    def __init__(self, letras_tentadas = [], padrao = "_", erros = 0, nome = ""):
        self.letras_tentadas = letras_tentadas
        self.padrao = padrao
        self.erros = erros
        self.nome = nome
        
    def monta_boneco(self):
        return {1: "cabeça",
                2:"braço direito",
                3: "braço esquerdo",
                4: "perna direita",
                5: "perna esquerda",
                0: "forca"
            }[self.erros]
    
    def reset_placar(self):
        self.letras_tentadas = []
        self.padrao = "_"
        self.erros = 0
        self.nome = ""

global bem_vindo
bem_vindo = "Seja bem-vindo(a)!"

app = Flask(__name__, static_url_path='/static')

#-----------------------------------------------------------------------------
#gera a rota para a raiz

@app.route("/", methods = ['POST', 'GET'])
def index():
    humano.reset_placar()
    bot.reset_placar()
    
    global tit
    tit = f.palavra_aleatoria()
    global patt
    patt = f.pattern(len(tit)) 
    
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
    
    global strin
    strin = f.replace_list(ss, '(?=\[).+?(?<=\])', '')
    strin = strin.replace(tit,f.pattern(len(tit)))
    strin = strin.replace(tit.upper(),f.pattern(len(tit)))
    strin = strin.replace(tit.lower(),f.pattern(len(tit)))
    strin = strin.replace(tit.capitalize(),f.pattern(len(tit)))
    print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n\n", strin)
    
    if request.method=='POST':


        humano.nome = request.form['uname']
        session['user'] = humano.nome
        return redirect ('/{}/jogar'.format(session['user']))

    else:    
        return render_template('index.html', boas_vindas = bem_vindo)

#-----------------------------------------------------------------------------
#gera uma rota para a página de jogo

@app.route("/<string:name>/jogar")
def jogar(name):
 
    name = humano.nome
    return render_template('jogar.html', boas_vindas = bem_vindo, name = humano.nome, padrao = patt, descricao = strin,\
                           sua_jogada="__", bot_jogada ="__", \
                               placar_erros = "{}: {} x Bot: {}".\
                                   format(humano.nome, humano.erros, bot.erros))


global bot
bot =  Jogador(letras_tentadas=[], erros=0,nome= "Bot")
bot.erros = 0
bot.nome = "Bot"
global humano
humano = Jogador(letras_tentadas=[], erros=0, nome='')
humano.erros = 0
global competicao
competicao = 'vitoria'

#-----------------------------------------------------------------------------
#gera uma rota para input do usuário e tentativas dos jogadores

@app.route("/<string:name>/enviar", methods = ['POST', 'GET'])
def enviar(name):   
    
    global bem_vindo
    global competicao
    
    humano_vitoria = False
    bot_vitoria = False
    competicao = ''
    name = humano.nome

    humano_jogada= "{} - Acertou!"
    ch = request.form['fname']
    try:
        inp_humano = ch

        hum_res = f.arrisca_letra_2(tit,inp_humano, humano.padrao)
        humano.padrao = hum_res[-2]
        if hum_res[0] is not True:
            humano.erros+=1
            humano_jogada = "{} - Errou... :("
    except: print("\nTente uma letra do alfabeto. Bot não perdeu sua vez!")


    while True:
        letra = f.predict_letra(bot.padrao, bot.letras_tentadas)
        if letra not in bot.letras_tentadas:
            break
    bot_jogada = "Bot Acertou!"
    bot.letras_tentadas.append(letra) 
    bot_res = f.arrisca_letra_2(tit,letra, bot.padrao)
    bot.padrao = bot_res[-2]
    
    print(tit)
    print(bot_res, bot.padrao, bot.erros)
    
    if 'user' in session:
    
        if not bot_res[0]:
            bot.erros+=1
            bot_jogada = "Bot errou..."
    
    
        if bot.erros==5 and humano.erros<5 or ("_" not in humano.padrao):
            humano_vitoria=True
            competicao = "vitoria"
            bem_vindo = "Parabéns! Você venceu!"
            return redirect("/pyfolio")
            
        elif humano.erros == 5 and bot.erros<5 or ("_" not in bot.padrao):
            bot_vitoria = True
            competicao = 'derrota'
            bem_vindo = "Que pena... Você perdeu. Tente novamente."
            return redirect("/")
            
        elif (humano.erros==5 and bot.erros==5) or ("_" not in humano.padrao and "_" not in bot.padrao):
            competicao = "empate"
            bem_vindo = "Empate... =/"
            return redirect("/")
        
        else:   
            return render_template('jogar.html', boas_vindas = bem_vindo, name = session['user'], padrao = humano.padrao, descricao = strin,\
                               sua_jogada=humano_jogada.format(ch), bot_jogada = bot_jogada, \
                                   placar_erros = "{}: {} x Bot: {}".\
                                       format(humano.nome, humano.erros, bot.erros))

#------------------------------------------------------------------------------
#rota para a página com o conteúdo desejado

@app.route("/pyfolio")
def portifolio():
    return render_template("portifolio.html")
    
#-----------------------------------------------------------------------------    
serve(app, host='0.0.0.0', port=80, threads=2)