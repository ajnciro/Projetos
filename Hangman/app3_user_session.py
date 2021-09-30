"""Este é o app Flask que servirá à geração da página HTML do jogo
aos moldes da aplicação original em hangman.py. Descrições gerais
do funcionamento do jogo já estão contidas em hangman.py"""
import funcoes as f
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
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



app = Flask(__name__, static_url_path="/static")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#-----------------------------------------------------------------------------
#gera a rota para a raiz

@app.route("/", methods = ['POST', 'GET'])
def index():
    
    if request.method == "POST":
        try:
            session['username'] = request.form['uname']
            if 'username' in session:
                globals()['wellc_{}'.format(session['username'])] = "Seja bem-vindo(a)!"
                globals()['compet_{}'.format(session['username'])] = 'vitoria'
                globals()['tit_{}'.format(session['username'])] = f.palavra_aleatoria()
                
                globals()['patt_{}'.format(session['username'])] = f.pattern(len(globals()['tit_{}'.format(session['username'])])) 
                
                with f.urllib.request.urlopen("https://pt.wikipedia.org/wiki/{}".format(globals()['tit_{}'.format(session['username'])])) as url:
                        page = url.read()
                        soup = f.BeautifulSoup(page, "html.parser")
                        
                ss = soup.find_all('p')
                if len(ss)>1:
                    ss = ss[1].get_text()
                elif len(ss)==1:
                    ss = ss[0].get_text()
                else:
                    ss = ''
                               
                globals()['strin_{}'.format(session['username'])] = f.replace_list(ss, '(?=\[).+?(?<=\])', '')
                globals()['strin_{}'.format(session['username'])] = globals()['strin_{}'.format(session['username'])].replace(globals()['tit_{}'.format(session['username'])],f.pattern(len(globals()['tit_{}'.format(session['username'])])))
                globals()['strin_{}'.format(session['username'])] = globals()['strin_{}'.format(session['username'])].replace(globals()['tit_{}'.format(session['username'])].upper(),f.pattern(len(globals()['tit_{}'.format(session['username'])])))
                globals()['strin_{}'.format(session['username'])] = globals()['strin_{}'.format(session['username'])].replace(globals()['tit_{}'.format(session['username'])].lower(),f.pattern(len(globals()['tit_{}'.format(session['username'])])))
                globals()['strin_{}'.format(session['username'])] = globals()['strin_{}'.format(session['username'])].replace(globals()['tit_{}'.format(session['username'])].capitalize(),f.pattern(len(globals()['tit_{}'.format(session['username'])])))
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n\n", globals()['strin_{}'.format(session['username'])])
                globals()['{}'.format(session['username'])] = Jogador(letras_tentadas=[], erros=0, nome = session['username'])
                globals()['bot_{}'.format(session['username'])] = Jogador(letras_tentadas=[], erros=0, nome = 'Bot')
                return redirect ('/{}/jogar'.format(session['username']))
        except: 
            print(session)
            
    if request.method == 'GET':
        if 'username' in session:
            session.pop('username', None)
        return render_template('index.html', boas_vindas = "Bem-vindo(a)!")

#-----------------------------------------------------------------------------
#gera uma rota para a página de jogo

@app.route("/<string:name>/jogar")
def jogar(name):
    
    if 'username' in session:
        
        name = globals()['{}'.format(session['username'])].nome
        return render_template('jogar.html', boas_vindas = globals()['wellc_{}'.format(session['username'])], name = session['username'], padrao = globals()['patt_{}'.format(session['username'])], descricao = globals()['strin_{}'.format(session['username'])],\
                               sua_jogada="__", bot_jogada ="__", \
                                   placar_erros = "{}: {} x Bot: {}".\
                                       format(session['username'], globals()['{}'.format(session['username'])].erros, globals()['bot_{}'.format(session['username'])].erros))

#-----------------------------------------------------------------------------
#gera uma rota para input do usuário e tentativas dos jogadores

@app.route("/<string:name>/enviar", methods = ['POST', 'GET'])
def enviar(name):   
    if 'username' in session:    
        
        humano_vitoria = False
        bot_vitoria = False
        competicao = ''
        name = globals()['{}'.format(session['username'])].nome
    
        humano_jogada= "{} - Acertou!"
        ch = request.form['fname']
        try:
            inp_humano = ch
    
            hum_res = f.arrisca_letra_2(globals()['tit_{}'.format(session['username'])],inp_humano, globals()['{}'.format(session['username'])].padrao)
            globals()['{}'.format(session['username'])].padrao = hum_res[-2]
            if hum_res[0] is not True:
                globals()['{}'.format(session['username'])].erros+=1
                humano_jogada = "{} - Errou... :("
        except: print("\nTente uma letra do alfabeto. Bot não perdeu sua vez!")
    
    
        while True:
            letra = f.predict_letra(globals()['bot_{}'.format(session['username'])].padrao, globals()['bot_{}'.format(session['username'])].letras_tentadas)
            if letra not in globals()['bot_{}'.format(session['username'])].letras_tentadas:
                break
        bot_jogada = "Bot Acertou!"
        globals()['bot_{}'.format(session['username'])].letras_tentadas.append(letra) 
        bot_res = f.arrisca_letra_2(globals()['tit_{}'.format(session['username'])],letra, globals()['bot_{}'.format(session['username'])].padrao)
        globals()['bot_{}'.format(session['username'])].padrao = bot_res[-2]
        
        print(globals()['tit_{}'.format(session['username'])])
        print(bot_res, globals()['bot_{}'.format(session['username'])].padrao, globals()['bot_{}'.format(session['username'])].erros)
        
        if not bot_res[0]:
            globals()['bot_{}'.format(session['username'])].erros+=1
            bot_jogada = "Bot errou..."
    
        if globals()['bot_{}'.format(session['username'])].erros==5 and globals()['{}'.format(session['username'])].erros<5 or ("_" not in globals()['{}'.format(session['username'])].padrao):
            humano_vitoria=True
            competicao = "vitoria"
            globals()['wellc_{}'.format(session['username'])] = "Parabéns! Você venceu!"
            return redirect("/pyfolio")
            
        elif globals()['{}'.format(session['username'])].erros == 5 and globals()['bot_{}'.format(session['username'])].erros<5 or ("_" not in globals()['bot_{}'.format(session['username'])].padrao):
            bot_vitoria = True
            competicao = 'derrota'
            globals()['wellc_{}'.format(session['username'])] = "Que pena... Você perdeu. Tente novamente."
            return render_template('index.html', boas_vindas=globals()['wellc_{}'.format(session['username'])])
            
        elif (globals()['{}'.format(session['username'])].erros==5 and globals()['bot_{}'.format(session['username'])].erros==5) or ("_" not in globals()['{}'.format(session['username'])].padrao and "_" not in globals()['bot_{}'.format(session['username'])].padrao):
            competicao = "empate"
            globals()['wellc_{}'.format(session['username'])] = "Empate... =/"
            return render_template('index.html', boas_vindas=globals()['wellc_{}'.format(session['username'])])
        
        else:   
            return render_template('jogar.html', boas_vindas = globals()['wellc_{}'.format(session['username'])], name = session['username'], padrao = globals()['{}'.format(session['username'])].padrao, descricao = globals()['strin_{}'.format(session['username'])],\
                               sua_jogada=humano_jogada.format(ch), bot_jogada = bot_jogada, \
                                   placar_erros = "{}: {} x Bot: {}".\
                                       format(session['username'], globals()['{}'.format(session['username'])].erros, globals()['bot_{}'.format(session['username'])].erros))

#------------------------------------------------------------------------------
#rota para a página com o conteúdo desejado

@app.route("/pyfolio")
def portifolio():
    return render_template("portifolio.html")
    
#-----------------------------------------------------------------------------    
if __name__ == "__main__":
    app.run()